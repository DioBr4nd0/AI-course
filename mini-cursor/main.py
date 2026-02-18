import sys
from src.graph.workflow import app

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py 'Build a snake game")
        sys.exit(1)
    user_task = sys.argv[1]
    print(f"🚀 Starting Mini-Cursor Agent...")
    print(f"🎯 Task: {user_task}\n")
    
    # Initialize State
    initial_state = {
        "task": user_task,
        "plan": [],
        "file_history": {},
        "revision_count": 0,
        "current_file": "none"
    }

    try:
        final_state = app.invoke(initial_state)
        print("\n✅ Build Complete!")
        print("📂 Checked 'workspace/' for your files.")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")

if __name__ == "__main__":
    main()

