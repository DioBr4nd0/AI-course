from traceback import print_tb
import re
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from src.state import AgentState
from src.tools.file_ops import write_file

# --- 1. THE MODEL ---
# Slightly higher temperature (0.2) for creative coding solutions
llm = ChatOllama(model="llama3.2:3b", temperature=0.2)

engineer_prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a Senior Python Developer.
    
    CONTEXT:
    You are building an app file by file.
    
    CURRENT TASK:
    Write the code for the file: '{current_file}'
    
    ALREADY WRITTEN FILES (For Context/Imports):
    {file_context}
    
    RULES:
    1. Output ONLY the raw Python code.
    2. Do not use Markdown blocks (no ```python).
    3. Include all necessary imports.
    4. If writing requirements.txt, list libraries line by line.
    """),
    ("user", "Write the code for {current_file}.")
])

def _clean_code(text: str) -> str:
    """Helper to strip Markdown and whitespace from LLM output"""
    text = re.sub(r"^```python", "", text, flags=re.MULTILINE)
    text = re.sub(r"^```", "", text, flags=re.MULTILINE)
    text = re.sub(r"```$", "", text, flags=re.MULTILINE)
    return text.strip()

def engineer_node(state: AgentState):
    current_file = state["current_file"]
    print(f"\n--- [ENGINEER] Writing file: {current_file} ---")

    file_content = list(state.get("file_history",{}).keys())

    chain = engineer_prompt | llm
    response = chain.invoke({
        "current_file": current_file,
        "file_context": str(file_content)
    })

    clean_code = _clean_code(response.content)

    write_result = write_file(current_file, clean_code)
    print(f"---- [ENGINEER] {write_result} ---")

    new_history = state.get("file_history",{}).copy()
    new_history[current_file] = "WRITTEN"

    return {
        "file_content": clean_code,
        "file_history": new_history,
    }