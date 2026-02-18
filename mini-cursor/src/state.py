import operator
from typing import Annotated, List, TypedDict, Union, Dict

class AgentState(TypedDict):
    # The mission
    task: str

    # The Plan
    plan: List[str]
    current_file: str

    # The work product
    file_content: str

    # The Memory (Context)
    file_history: Annotated[Dict[str,str], "Merge dictionaries"]

    # The Feedback loop  (Self healing)
    shell_results: List[str]
    error_context: str
    retry_count: int
