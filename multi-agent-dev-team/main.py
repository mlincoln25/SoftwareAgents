from dotenv import load_dotenv
load_dotenv()
import sys
from reviewer_agent.agent import review_code
from developer_agent.agent import handle_task
from devops_agent.agent import commit_and_push
from memory_manager import add_snippet

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python main.py develop '<task description>'")
        print("  python main.py review '<code snippet>'")
        print("  python main.py commit '<commit message>'")
        return

    action = sys.argv[1]

    if action == 'develop':
        task = sys.argv[2]
        result = handle_task(task)
        print("Generated code:\n", result)

    elif action == 'review':
        code_snippet = sys.argv[2]
        result = review_code(code_snippet)
        print("Reviewed code:\n", result)

    elif action == 'commit':
        commit_message = sys.argv[2]
        result = commit_and_push(commit_message)
        print(result)

    else:
        print(f"Unknown action: {action}")

if __name__ == "__main__":
    main()
