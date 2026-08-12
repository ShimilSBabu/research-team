from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import os
from time import sleep
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from langgraph.prebuilt import ToolNode
from typing import Annotated, Sequence
from langgraph.graph.message import add_messages
from logging import getLogger

logger=getLogger(__name__)

load_dotenv()

MODELS=[
        "mistral-small-latest",
        "mistral-medium-latest",
        "mistral-large-latest",
        ]
API_KEYS=[
    os.environ["MISTRAL_API_KEY_EJ"],
    os.environ["MISTRAL_AUTONOMOUS_API_KEY"],
    os.environ["MISTRAL_API_KEY"],
    # os.environ["MISTRAL_API_KEY_PM"],
]

def get_specialized_llm(temperature, model=MODELS[0], api_key=API_KEYS[0], max_tokens=64000):
    return ChatMistralAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=max_tokens
        )

decomposer_llm=get_specialized_llm(temperature=0.1)
researcher_llm=get_specialized_llm(temperature=0.3)
fact_checker_llm=get_specialized_llm(temperature=0.0)
writer_llm=get_specialized_llm(temperature=0.5)
critic_llm=get_specialized_llm(temperature=0.2)
reviewer_llm=get_specialized_llm(temperature=0.0)


# --------------------------------------------------------------------------------------------------------------------------------------
async def _get_llm_responce(messages, api_key, model, temperature, structured_output=""):
    logger.debug(msg="Connecting to the LLM.")
    try:
        llm = ChatMistralAI(
            model=model,
            temperature=temperature,
            api_key=api_key,
            max_tokens=64000
        )
        if structured_output:
            logger.debug(msg="Equpping the LLM with the required schema.")
            llm = llm.with_structured_output(structured_output)
            logger.debug(msg="Attempting to generate the response with schema.")
            response = await llm.ainvoke(messages)
            logger.debug(msg=f"Response ({type(response)}) generated with schema.\n{response}")
            return {"status":1,"content":response}

        logger.debug(msg="Attempting to generate the response.")
        response = await llm.ainvoke(messages)
        logger.debug(msg=f"Response ({type(response)}) generated.\n{response}")
        return {"status":1,"content":response.content}
    except Exception as e:
        logger.exception(msg="Response generation failed.")
        return {"status":0,"content":str(e)}
        

async def call_llm(messages, temperature=0.3, max_retries=15, llm_purpose="", structured_output=""):
    logger.info(msg=f"\nGetting LLM response for {llm_purpose}.")

    retry_count=0
    response=0
    
    if not messages:
        logger.warning(msg="Missing 'messages' for the LLM.")
        return {"status":0, "content":"Cannot process empty message."}
    for model in MODELS:
        for api_key in API_KEYS:
            if retry_count==max_retries:
                if response:
                    logger.warning(msg=f"Max number of trial attempts reached. Issue;\n{response['content']}")
                    return {"status":0, "content":f"Max number of trial attempts reached. Error\n{response['content']}"}
                logger.info(msg=f"LLM reached Max number of trial attempts for {llm_purpose}.")
                return {"status":0, "content":"Max number of trial attempts reached."}
            
            logger.debug(f"{llm_purpose} LLM Trial Count: {retry_count+1}")
            response=await _get_llm_responce(messages, 
                                      api_key, 
                                      model=model, 
                                      temperature=temperature,
                                      structured_output=structured_output
                                      )
            
            if response["status"]:
                logger.info(msg="LLM returing the response")
                return response
            
            logger.debug(msg="LLM sleeping for 5 seconds.")
            sleep(5)
            retry_count += 1



# def get_specialized_llm(temperature=0.1, max_retries=3, llm_purpose="Decomposer"):
#     def modifier(messages, structured_output, temperature, max_retries, llm_purpose):
#         return call_llm(messages, temperature=temperature, max_retries=max_retries, llm_purpose=llm_purpose, structured_output=structured_output)
#     return modifier

# decomposer_llm=get_specialized_llm()

class MessagesState(BaseModel):
    messages:Annotated[Sequence[BaseMessage], add_messages]
    intermediate_output:str=""
    final_output:str=""


llm = ChatMistralAI(
            model="mistral-small-latest",
            temperature=0.1,
            api_key=os.environ["MISTRAL_AUTONOMOUS_API_KEY"],
            max_tokens=32000
        )

def should_continue(state: MessagesState):
    last = state.messages[-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END

def get_react_agent(system_message:str, human_message:str, tools:object):
    llm_with_tools = llm.bind_tools(tools)
    def call_llm(state: MessagesState):
        response = "Unable to reach the ReAct LLM."
        for trial_count in range(3):
            try:
                response = llm_with_tools.invoke(state.messages)
                return {"messages": [response]}
            except Exception as e:
                print(f"\nTrial {trial_count+1}/3:Retrying the ReAct agent due to the below mentioned error.\n{str(e)}\n")
                sleep(10)
        return {"messages": [response]}

    tool_node = ToolNode(tools, handle_tool_errors=True)

    graph = (
        StateGraph(MessagesState)
        .add_node("agent", call_llm)
        .add_node("tools", tool_node)
        .add_edge(START, "agent")
        .add_conditional_edges("agent", should_continue)
        .add_edge("tools", "agent")   # always loop back for self-correction
        .compile()
    )

    result = graph.invoke(
        {
        "messages": [
            SystemMessage(content=system_message),
            HumanMessage(content=human_message)
            ]
    }
    )
    content = result["messages"][-1].content
    if "```" in content:
        json_start = content.find("```")
        json_end = content.rfind("```") + 1
        result["messages"][-1].content = content[json_start:json_end]
    return result