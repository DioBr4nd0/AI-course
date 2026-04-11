from typing import Annotated, List, TypedDict, Union, Dict

class AgentState(TypedDict):
    task: str
    plan: List[str]
    current_file: Union[str, None]
    file_content: str
    file_history: Annotated[Dict[str,str], "Merge dictionaries"]
    shell_results: List[str]
    error_context: Union[str, None]
    retry_count: int
    file_context: Annotated[Dict[str, str], "Merge file contents"]
