# Role: Break the user's high-level request into a concrete file list.

import os
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List

from src.state import AgentState

# the model
llm = ChatOllama(model="llama3.2:3b", temperature=0)

# the schema
class ProjectPlan(BaseModel):
    files: List[str] = Field(
        description="List of file names to build. Always include main.py and requirements.txt."
    )

# the prompt
architect_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Software Architect.
    
    YOUR GOAL:
    Given a user request, plan the EXACT file structure needed to build it.
    
    RULES:
    1. Return ONLY a list of file names.
    2. Always include 'main.py' as the entry point.
    3. Always include 'requirements.txt' for dependencies.
    4. Keep it simple: Max 3-5 files.
    5. Do not write code.
    
    Example Output:
    ["main.py", "game_logic.py", "requirements.txt"]
    """),
    ("user", "{task}")
])

# the node
def architect_node(state: AgentState):
    print(f"\n--- [ARCHITECT] Analyzing request: {state['task']} ---")

    chain = architect_prompt | llm.with_structured_output(ProjectPlan)

    result = chain.invoke({"task" : state["task"]})
    print(f"--- [ARCHITECT] Plan created: {result.files} ---")
    
    # Update State: Save the plan and initialize the file index
    return {
        "plan": result.files,
        "current_file": result.files[0] if result.files else None,
        "file_history": {}  # Reset history
    }
