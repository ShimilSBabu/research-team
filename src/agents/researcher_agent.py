from src.prompt_factory.prompt_manager import get_prompt
from src.model import call_llm
from src.tools import web_search

from langchain_core.messages import SystemMessage, HumanMessage
from logging import getLogger
import json

logger=getLogger(__name__)

def researcher_node(state:dict):
    logger.info(msg="Initializing researcher node.")
    try:
        research_topic=state["research_topic"]
        research_sub_topic=state["research_sub_topic"]
        logger.info(msg=f"Research topic: {research_topic}\nResearch sub-topic: {research_sub_topic}")

        web_results=web_search.run(query=f"{research_sub_topic} with respect to {research_topic}")
        logger.debug(msg=f"Received web results for sub-topic: {research_sub_topic!a}.")

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
        logger.debug(msg=f"Citations generated for sub-topic: {research_sub_topic!a}.")

        researcher_system_prompt=get_prompt(module_type="agent", module_name="researcher")
        messages=[
                    SystemMessage(content=researcher_system_prompt["content"].format(
                        research_sub_topic=research_sub_topic, 
                        research_topic=research_topic
                        )
                    ),
                    HumanMessage(content=f"Findings\n {json.dumps(citations_list)}")
                ]
        concise_web_results=call_llm(messages, llm_purpose="Researcher Agent")
        if not concise_web_results["status"]:
            logger.error(msg="LLM failed to provide concise web results.")
            raise ValueError("LLM failed to provide concise web results.")
        logger.info(msg=f"consise web results created for sub-topic: {research_sub_topic!a}.")
        research_result={
            "task":web_results["content"]["query"],
            "citations":citations_list,
            "visited_urls":visited_urls_list,
            "websearch_result":concise_web_results["content"]
        }

        logger.info(msg=f"Research successful for sub-topic: {research_sub_topic!a}.\nresearch_result\n{research_result}")
        return {
            "researcher":{
                "completed_tasks":[research_sub_topic],
                "research_results":[research_result]
            }
        }
    except:
        logger.exception(msg=f"Research failed for sub-topic: {research_sub_topic!a}.")
        return {
                "researcher":{
                    "failed_tasks":[research_sub_topic]
                }
            }