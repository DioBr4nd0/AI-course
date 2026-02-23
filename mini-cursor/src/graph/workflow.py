from typing import Literal
from langgraph.graph import StateGraph, END
from src.state import AgentState

# Import Nodes
from src.agents.architect import architect_node
from src.agents.engineer import engineer_node
from src.agents.reviewer import reviewer_node

# --- DECISION LOGIC (The Brain) ---

def decide_next_step(state: AgentState) -> Literal["engineer", END]:
    """
    This single function handles all routing logic.
    Run after the Reviewer.
    """
    # 1. Check for Errors (Self-Healing)
    error = state.get("error_context")
    rev_count = state.get("retry_count", 0)
    
    if error:
        if rev_count > 3:
            print("--- [DECISION] ⚠️ Too many retries. Giving up on this file. ---")
            # If we give up, we clear the error and try to move to the next file
            # (Or you could return END to abort the whole project)
            pass 
        else:
            return "engineer" # LOOP BACK TO FIX

    # 2. If no errors (or we gave up), check if there are more files to build
    plan = state.get("plan", [])
    history = state.get("file_history", {})
    
    # Identify files that haven't been written yet
    remaining = [f for f in plan if f not in history]
    
    if remaining:
        next_file = remaining[0]
        print(f"--- [DECISION] Next file to build: {next_file} ---")
        return "engineer" # LOOP BACK TO BUILD NEXT FILE
    
    # 3. If no errors and no files left -> DONE
    print("--- [DECISION] All files written. Job Complete. ---")
    return END

# --- NODE WRAPPER ---
def engineer_wrapper(state: AgentState):
    """
    Prepares the state for the Engineer.
    """
    # Only pick a NEW file if we are NOT fixing an error
    if not state.get("error_context"):
        plan = state.get("plan", [])
        history = state.get("file_history", {})
        remaining = [f for f in plan if f not in history]
        
        if remaining:
            state["current_file"] = remaining[0]
            
    return engineer_node(state)

# --- THE GRAPH ---
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("architect", architect_node)
workflow.add_node("engineer", engineer_wrapper)
workflow.add_node("reviewer", reviewer_node)

# Set Entry Point
workflow.set_entry_point("architect")

# Edges
# 1. Architect -> Engineer (Start the build)
workflow.add_edge("architect", "engineer")

# 2. Engineer -> Reviewer (Always check work)
workflow.add_edge("engineer", "reviewer")

# 3. Reviewer -> Decision (The Logic Hub)
workflow.add_conditional_edges(
    "reviewer",         # Start from Reviewer
    decide_next_step,   # Run this logic function
    {
        "engineer": "engineer", # Go back to Engineer
        END: END                # Or finish
    }
)

app = workflow.compile()