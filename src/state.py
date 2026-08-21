from pydantic import BaseModel, Field
from typing import Annotated, Literal
import operator

from src.utils.config import CRITIC_MAX_ITERATION

# def merge_dicts(left:dict, right:dict) -> dict:
#     """Reducer:shallow-merge two dicts. Used so N parallel researchers can
#     each contribute `{topic:findings}` without wiping each other out."""
#     print(f"left\n{left}\nright\n{right}")
#     merged = dict(left or {})
#     if "completed_tasks" in merged.keys():
#         pass
#     merged.update(right or {})
#     return merged

def researcherstate_merge(researcherstate_1:ResearcherState, researcherstate_2:dict):
    merged_researcherstate=researcherstate_1.model_copy(deep=True)
    if "completed_tasks" in researcherstate_2.keys():
        merged_researcherstate.completed_tasks=operator.add(merged_researcherstate.completed_tasks, researcherstate_2["completed_tasks"])
    if "research_results" in researcherstate_2.keys():
        merged_researcherstate.research_results=operator.add(merged_researcherstate.research_results, researcherstate_2["research_results"])
    if "failed_tasks" in researcherstate_2.keys():
        merged_researcherstate.failed_tasks=operator.add(merged_researcherstate.failed_tasks, researcherstate_2["failed_tasks"])    
    return merged_researcherstate

def streaming_display_merge(input_1:str|list, input_2:str|list):
    if isinstance(input_2, str):
        return input_2
    if isinstance(input_1, str):
        return input_2
    input_1.extend(input_2)
    return input_1

class QueryState(BaseModel):
    query:str=Field(description="User query", default="")
    time:str=Field(description="Time of query", default="")
    user:str=Field(description="User Id", default="")

class DecomposerState(BaseModel):
    tasks:list[str]=Field(description="List of indipendent sub tasks necessary for the completion of the main task.", default=[])

class Citation(BaseModel):
    url:str=Field(description="URL of research", default="")
    title:str=Field(description="Title of research", default="")
    content:str=Field(description="Content fetched from the URL.", default="")

class ResearchResult(BaseModel):
    task:str=Field(description="Task under research", default="")
    citations:list[Citation]=Field(description="List of individual sources of data for the current task fetched from various URLs.", default=[Citation])
    research_status:Literal["COMPLETE", "FAIL"]=Field(description="'COMPLETE' or 'FAIL'", default="FAIL")
    websearch_result:str=Field(description="Response formed by combining the data fetched from all citations.", default="")
    visited_urls:Annotated[list[str], operator.add]=Field(description="List of URLs visited for this task.", default=[])
    # failed_urls:Annotated[list[str], operator.add]=Field(description="List of failed URLs.", default=[]) 

class ResearcherState(BaseModel):
    completed_tasks:Annotated[list[str], operator.add]=Field(description="Tasks researched.", default=[])
    failed_tasks:Annotated[list[str], operator.add]=Field(description="Remaining tasks to be researched.", default=[])
    research_results:Annotated[list[ResearchResult], operator.add]=Field(description="Topics researched", default=[])

    # research_results:Annotated[dict, merge_dicts]=Field(description="Topics researched", default=)    # topic -> findings text
    # visited_urls:Annotated[list[str], operator.add]=Field(description="", default=)     # dedup memory
    # citations:Annotated[list[Citation], operator.add]=Field(description="", default=)   # topic/title/url triples
    # failed_urls:Annotated[list[str], operator.add]=Field(description="", default=) 

class FactCheckReport(BaseModel):
    claim:str=Field(description="The claim under investigation", default="")
    source:str=Field(description="The source of the claim.", default="")
    status:Literal["VERIFIED", "REJECTED", "UNVERIFIED", "CONTRADICTED" ]=Field(description="'VERIFIED' or 'REJECTED' or 'UNVERIFIED' or 'CONTRADICTED'", default="UNVERIFIED")
    confidence:float=Field(description="A float score between 0.00 and 1.00 representing how much the claim is true.", default=0.00, ge=0.00, le=1.00)
    feedback:str=Field(description="An honest opinion on this claim.", default="")
    reason:str=Field(description="The reason for the confidence score.", default="")

class FactCheckLog(BaseModel):
    total_claims_checked:int=Field(description="Total number of claims fact checked.", default=0)
    total_verified_claims:int=Field(description="Total number of VERIFIED claims found.", default=0)
    total_rejected_claims:int=Field(description="Total number of REJECTED claims found.", default=0)
    total_unverified_claims:int=Field(description="Total number of UNVERIFIED claims found.", default=0)
    total_contradicted_claims:int=Field(description="Total number of CONTRADICTED claims found.", default=0)
    single_line_log:str=Field(description="Single line report on all fact checks.", default="")

class FactCheckerState(BaseModel):
    fact_check_results:list[FactCheckReport]=Field(description="List of fact check reports of each claim", default=[])
    fact_check_log:FactCheckLog=Field(description="Log report of the entire fact check.", default_factory=FactCheckLog)

class WriterState(BaseModel):
    draft_research_report:str=Field(description="Draft report of the current research.", default="")

class CriticReport(BaseModel):
    critic_feedback:str=Field(description="List of logical feedback on each claim", default="")
    critic_score:float=Field(description="Score within the range of 0.00-1.00 to represent the overall quality of the report.", default=0.00, ge=0.00, le=1.00)

class CriticState(BaseModel):
    critic_report:CriticReport=Field(description="Report from critic on the quality of draft research report.", default_factory=CriticReport)
    critic_iteration_count:int=Field(description="Number of times the critic was called for the current report.", default=0)
    critic_max_iteration:int=Field(description="Max allowed count for which the critic could be called for this report.", default=CRITIC_MAX_ITERATION)

class ReviewerState(BaseModel):
    review_result:Literal["PASS", "FAIL"]=Field(description="'PASS' or 'FAIL'", default="FAIL")
    review_notes:list[str]=Field(description="Issues found, if any. Empty list if PASS.", default=[])

class ResponseState(BaseModel):
    status:bool=Field(description="Tells whether the final response is prepared or not.", default=False)
    content:str=Field(description="Final response to the user.", default="Execution Incomplete")
    response_time:str=Field(description="Time of response preparation", default="")

class AgentState(BaseModel):
    query:QueryState=Field(description="Query from user.", default_factory=QueryState)

    decomposer:DecomposerState=Field(default_factory=DecomposerState)
    researcher:Annotated[ResearcherState, researcherstate_merge]=Field(default_factory=ResearcherState)
    fact_checker:FactCheckerState=Field(default_factory=FactCheckerState)
    critic:CriticState=Field(default_factory=CriticState)
    writer:WriterState=Field(default_factory=WriterState)
    reviewer:WriterState=Field(default_factory=ReviewerState)

    human_feedback:list=Field(description="The human feedback.", default="")
    response:ResponseState=Field(description="Final response to the user.", default_factory=ResponseState)

    streaming_display:Annotated[list|str, streaming_display_merge]=Field(description="The value of this fied will be streamed as state updates to the frontend.", default="")