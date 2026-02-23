import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.tools.file_ops import write_file, read_file

# --- 1. THE MODEL ---
llm = ChatOllama(model="llama3.2:3b", temperature=0.1)

# --- 2. THE PROMPTS ---

# A. Standard Python Coding Prompt
python_code_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Python Developer.
    THE GOAL: "{task}"
    WRITING FILE: '{current_file}'
    EXISTING FILES: {file_context}
    
    RULES:
    1. Output ONLY the raw Python code.
    2. No Markdown blocks (no ```python).
    3. Include all necessary imports.
    """),
    ("user", "Write the code for {current_file}.")
])

# B. Requirements (Dependency) Prompt
requirements_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Python Dependency Manager.
    
    YOUR JOB: Write the 'requirements.txt' file.
    
    RULES:
    1. Output ONLY the list of library names (one per line).
    2. DO NOT write python code (no `open()`, no `write()`).
    3. DO NOT use markdown.
    4. Just the package names.
    
    Example Output:
    pandas
    numpy
    qrcode
    """),
    ("user", "Write the requirements for task: {task}")
])

# C. Python Fix Prompt (For .py files)
python_fix_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Python Debugger.
    THE ERROR: {error_context}
    THE BROKEN CODE:
    {current_code}
    
    RULES:
    1. Output ONLY the fixed Python code.
    2. Fix the specific SyntaxError or ImportError.
    """),
    ("user", "Fix the code.")
])

# D. Requirements Fix Prompt (For requirements.txt)
requirements_fix_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Dependency Manager.
    
    THE ERROR: pip failed to install requirements.
    ERROR DETAILS: {error_context}
    
    THE BAD FILE CONTENT:
    {current_code}
    
    THE FIX:
    The file likely contains Python code or Markdown. It must ONLY contain library names.
    Remove all code. Just list the libraries needed for: "{task}"
    """),
    ("user", "Fix requirements.txt")
])

def _clean_code(text: str) -> str:
    # Strip markdown code blocks
    text = re.sub(r"^```\w*", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

# --- 3. THE NODE ---
def engineer_node(state: AgentState):
    current_file = state["current_file"]
    task = state["task"]
    error = state.get("error_context")
    file_context = list(state.get("file_history", {}).keys())
    
    print(f"\n--- [ENGINEER] Processing: {current_file} ---")

    # --- ROUTING LOGIC ---
    # We choose the right prompt based on File Type AND Error Status
    
    # CASE 1: Fixing a Bug
    if error:
        print(f"--- [ENGINEER] 🚑 Fixing Bug in {current_file} ---")
        broken_code = read_file(current_file)
        
        if "requirements.txt" in current_file:
            # Use the specialized Dependency Fixer
            chain = requirements_fix_prompt | llm
            response = chain.invoke({
                "task": task,
                "error_context": error,
                "current_code": broken_code
            })
        else:
            # Use the standard Python Fixer
            chain = python_fix_prompt | llm
            response = chain.invoke({
                "current_file": current_file,
                "error_context": error,
                "current_code": broken_code
            })
            
    # CASE 2: Writing New Code
    else:
        if "requirements.txt" in current_file:
            # Use the Dependency Writer
            chain = requirements_prompt | llm
            response = chain.invoke({"task": task})
        else:
            # Use the Python Writer
            chain = python_code_prompt | llm
            response = chain.invoke({
                "task": task,
                "current_file": current_file,
                "file_context": str(file_context)
            })
    
    # Clean and Save
    clean_code = _clean_code(response.content)
    write_result = write_file(current_file, clean_code)
    print(f"---- [ENGINEER] {write_result} ---")
    
    # Update State
    new_history = state.get("file_history", {}).copy()
    new_history[current_file] = "WRITTEN"
    
    return {
        "file_content": clean_code,
        "file_history": new_history,
        "current_file": current_file # Ensure State Update
    }