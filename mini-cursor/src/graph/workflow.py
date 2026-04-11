from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import AgentState

from src.agents.architect import architect_node
from src.agents.engineer import engineer_node
from src.agents.reviewer import reviewer_node

def decide_next_step(state: AgentState):
    error = state.get("error_context")
    rev_count = state.get("retry_count", 0)
    plan = state.get("plan", [])
    history = state.get("file_history", {})
    
    if error and rev_count > 3:
        current = state.get("current_file")
        return "engineer"
    
    if error:
        return "engineer"
    
    remaining = [f for f in plan if f not in history]
    if remaining:
        return "engineer"
    return END

def engineer_wrapper(state: AgentState):
    error = state.get("error_context")
    rev_count = state.get("retry_count", 0)
    plan = state.get("plan", [])
    history = state.get("file_history", {}).copy()
    current_file = state.get("current_file")
    
    if error and rev_count > 3:
        print(f"--- [WRAPPER] ⚠️ Giving up on {current_file} after 3 retries ---")
        if current_file:
            history[current_file] = "FAILED"
        state["file_history"] = history
        state["current_file"] = None
        state["error_context"] = None
        state["retry_count"] = 0
        remaining = [f for f in plan if f not in history]
        if remaining:
            state["current_file"] = remaining[0]
            return engineer_node(state)
        else:
            return {"file_history": history}
    
    if not error:
        remaining = [f for f in plan if f not in history]
        if remaining:
            state["current_file"] = remaining[0]
    
    result = engineer_node(state)
    
    if "file_content" in result and "current_file" in result:
        file_name = result["current_file"]
        content = result["file_content"]
        current_context = state.get("file_context", {})
        current_context[file_name] = content
        result["file_context"] = current_context
    
    return result

workflow = StateGraph(AgentState)

workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_wrapper)
workflow.add_node("reviewer", reviewer_node)

workflow.set_entry_point("architect")
workflow.add_edge("architect", "engineer")
workflow.add_edge("engineer", "reviewer")

workflow.add_conditional_edges(
    "reviewer",
    decide_next_step,
    {"engineer": "engineer", END: END}
)

app = workflow.compile()
