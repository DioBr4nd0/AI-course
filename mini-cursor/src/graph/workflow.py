from typing import Literal
from langgraph.graph import StateGraph, END

# Import our components
from src.state import AgentState
from src.agents.architect import architect_node
from src.agents.engineer import engineer_node

# --- The Manager ---
def check_next_step(state: AgentState):
    """
    Decides what to do next.
    Compares the 'plan' vs 'file_history'
    """
    plan = state.get("plan", [])
    history = state.get("file_history", {})

    # fine the first file that hasnt been written yet
    remaining_files = [ f for f in plan if f not in history]

    if remaining_files:
        # we have work to do!
        next_file = remaining_files[0]
        print(f"--- [ROUTER] Next file to build: {next_file} ---")
        return "engineer"
    else:
        print("--- [ROUTER] All files written, Job Complete. ---")
        return END

# --- 2. THE NODE WRAPPERS ---
# We need small wrappers to ensure state updates happen correctly
# The Architect is already set up to return a dict, so we can use it directly.

def engineer_wrapper(state: AgentState):
    """
    Before running the engineer, we must update 'current_file' in the state
    so the engineer knows what to write.
    """
    plan = state.get("plan", [])
    history = state.get("file_history",{})
    remaining_files = [f for f in plan if f not in history]

    state["current_file"] = remaining_files[0]
    return engineer_node(state)

