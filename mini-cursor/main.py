import sys
from src.graph.workflow import app

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'Build a snake game'")
        print("Example: python main.py 'Build a calculator'")
        sys.exit(1)
    user_task = sys.argv[1]
    print(f"Starting Mini-Cursor Agent...")
    print(f"Task: {user_task}\n")
    
    initial_state = {
        "task": user_task,
        "plan": [],
        "file_history": {},
        "retry_count": 0,
        "current_file": "none",
        "file_context": {}
    }

    try:
        final_state = app.invoke(initial_state)
        print("\n=== Build Complete! ===")
        print("Files created in workspace/:")
        for f in final_state.get("file_history", {}).keys():
            print(f"  - {f}")
    except Exception as e:
        print(f"\nError: {e}")

if __name__ == "__main__":
    main()
