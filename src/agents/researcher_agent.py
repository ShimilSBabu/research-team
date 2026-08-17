from src.prompt_factory.prompt_manager import get_prompt
from src.model import call_llm
from src.tools import web_search

from time import perf_counter
from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger
import json

logger=getLogger(__name__)

async def researcher_node(state:dict):
    logger.info(msg="Initializing researcher node.")
    start_time=perf_counter()
    try:
        researcher_id=state["researcher_id"]
        research_topic=state["research_topic"]
        research_sub_topic=state["research_sub_topic"]
        logger.info(msg=f"Researcher [{researcher_id}] => Research topic : {research_topic}\nResearch sub-topic: {research_sub_topic}")

        web_results=await web_search.run(query=f"{research_sub_topic} with respect to {research_topic}")
        logger.debug(msg=f"Researcher [{researcher_id}] => Received web results for sub-topic: {research_sub_topic!a}.")

        visited_urls_list=[]
        citations_list=[]
        for result in web_results["content"]["results"]:
            citation={
                "url":result["url"],
                "title":result["title"],
                "content":result["content"][:6000],
            }
            citations_list.append(citation)
            visited_urls_list.append(result["url"])
        logger.debug(msg=f"Researcher [{researcher_id}] => Citations generated for sub-topic: {research_sub_topic!a}.")

        researcher_system_prompt=get_prompt(module_type="agent", module_name="researcher")
        messages=[
                    SystemMessage(content=researcher_system_prompt["content"].format(
                        research_sub_topic=research_sub_topic, 
                        research_topic=research_topic
                        )
                    ),
                    HumanMessage(content=f"Findings\n {json.dumps(citations_list)}")
                ]
        logger.info(msg=f"Researcher [{researcher_id}] => Researching: {research_sub_topic}")
        concise_web_results=await call_llm(messages, llm_purpose="Researcher Agent", temperature=0.2)
        if not concise_web_results["status"]:
            logger.error(msg=f"Researcher [{researcher_id}] => LLM failed to provide concise web results for sub-topic: {research_sub_topic!a}.")
            raise ValueError(f"Researcher [{researcher_id}] => LLM failed to provide concise web results for sub-topic: {research_sub_topic!a}.")
        logger.info(msg=f"Researcher [{researcher_id}] => consise web results created for sub-topic: {research_sub_topic!a}.")
        research_result={
            "task":web_results["content"]["query"],
            "citations":citations_list,
            "visited_urls":visited_urls_list,
            "websearch_result":concise_web_results["content"]
        }

        latency = perf_counter() - start_time
        logger.info(msg=f"Researcher [{researcher_id}] => Research successful for sub-topic: {research_sub_topic!a}. Latency: {latency:.6f} seconds.\nresearch_result\n{research_result}")
        return {
            "researcher":{
                "completed_tasks":[research_sub_topic],
                "research_results":[research_result]
            }
        }
    except:
        logger.exception(msg=f"Researcher [{researcher_id}] => Research failed for sub-topic: {research_sub_topic!a}. Latency: {latency:.6f} seconds.")
        return {
                "researcher":{
                    "failed_tasks":[research_sub_topic]
                }
            }