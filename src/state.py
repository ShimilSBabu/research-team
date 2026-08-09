from pydantic import BaseModel, Field
from typing import Annotated, Literal
import operator

# def merge_dicts(left:dict, right:dict) -> dict:
#     """Reducer:shallow-merge two dicts. Used so N parallel researchers can
#     each contribute `{topic:findings}` without wiping each other out."""
#     merged = dict(left or {})
#     merged.update(right or {})
#     return merged

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
    fetch_status:Literal["FETCHED", "FAIL"]=Field(description="'FETCHED' or 'FAIL'", default="FAIL")

class ResearchResult(BaseModel):
    task:str=Field(description="Task under research", default="")
    citations:list[Citation]=Field(description="List of individual sources of data for the current task fetched from various URLs.", default_factory=[Citation])
    research_status:Literal["COMPLETE", "FAIL"]=Field(description="'COMPLETE' or 'FAIL'", default="FAIL")
    research_result:str=Field(description="Response formed by combining the data fetched from all citations.")
    visited_urls:Annotated[list[str], operator.add]=Field(description="List of URLs visited for this task.", default=[])
    failed_urls:Annotated[list[str], operator.add]=Field(description="List of failed URLs.", default=[]) 

class ResearcherState(BaseModel):
    completed_tasks:list[str]=Field(description="Tasks researched.", default=[])
    pending_tasks:list[str]=Field(description="Remaining tasks to be researched.", default=[])
    research_results:Annotated[list[ResearchResult], operator.add]=Field(description="Topics researched", default_factory=[ResearchResult])

    # research_results:Annotated[dict, merge_dicts]=Field(description="Topics researched", default=)    # topic -> findings text
    # visited_urls:Annotated[list[str], operator.add]=Field(description="", default=)     # dedup memory
    # citations:Annotated[list[Citation], operator.add]=Field(description="", default=)   # topic/title/url triples
    # failed_urls:Annotated[list[str], operator.add]=Field(description="", default=) 

class FactCheckReport(BaseModel):
    claim:str=Field(description="The claim under investigation", default="")
    source:str=Field(description="The source of the claim.", default="")
    status:Literal["verified", "unvarified", "contradicted"]
    confidence:float=Field(description="A float representation of how much the claim is true.", default=0.0, ge=0.0)
    feedback:str=Field(description="An honest opinion on this claim.", default="")
    reason:str=Field(description="The reason for the confidence score.", default="")

class FactCheckerState(BaseModel):
    fact_check_results:list=Field(description="List of fact check reports of each claim", default_factory=list[FactCheckReport])
    fact_check_log:str=Field(description="Single line report on all fact checks.", default="")

class CriticState(BaseModel):
    critic_feedback:list[str]=Field(description="List of logical feedback on each claim", default=[])
    critic_score:float=Field(description="Score within the range of 0.0-1.0 to represent the overall quality of the report.", default=0.0, ge=0.0, le=1.0, decimal_places=2)
    critic_iteration_count:int=Field(description="Number of times the critic was called for the current report.", default=0)
    critic_max_iteration:int=Field(description="Max allowed count for which the critic could be called for this report.", default=3)

class WriterState(BaseModel):
    draft_research_report:str=Field(description="Draft report of the current research.", default="")

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
    researcher:ResearcherState=Field(default_factory=ResearcherState)
    fact_checker:FactCheckerState=Field(default_factory=FactCheckerState)
    critic:CriticState=Field(default_factory=CriticState)
    writer:WriterState=Field(default_factory=WriterState)
    reviewer:WriterState=Field(default_factory=ReviewerState)

    human_feedback:list=Field(description="The human feedback.", default="")
    response:dict=Field(description="Final response to the user.", default_factory=ResponseState)