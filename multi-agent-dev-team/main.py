# main.py

import os
from dotenv import load_dotenv
from agents import Agent, Runner, handoff
from developer_agent.agent import developer_agent
from reviewer_agent.agent import reviewer_agent
from devops_agent.agent import devops_agent, read_file_from_github, update_file_on_github
from memory_manager import MemoryManager

# Load environment variables
load_dotenv()

# Initialize memory manager
memory_manager = MemoryManager()

# Define the root agent with handoffs to specialized agents
root_agent = Agent(
    name="Root Agent",
    instructions=(
        "You are the Root Agent responsible for delegating tasks to specialized agents. "
        "Analyze the user's request and hand off to the appropriate agent: Developer Agent, Review Agent, or DevOps Agent."
    ),
    handoffs=[
        handoff(developer_agent),
        handoff(reviewer_agent),
        handoff(devops_agent)
    ]
)

async def main():
    # Example user instruction
    user_instruction = "Create a new Python script that prints 'Hello, World!'"

    # Run the root agent with the user's instruction
    result = await Runner.run(root_agent, user_instruction)

    # Retrieve the final output and the last agent that handled the task
    final_output = result.final_output
    last_agent = result.last_agent

    # Handle the output based on the agent that processed the task
    if last_agent == developer_agent:
        # Store the generated code in memory
        memory_manager.save_to_memory("new_script.py", final_output)
        print("Code generated and stored in memory.")

    elif last_agent == reviewer_agent:
        # Output the review feedback
        print("Code review feedback:")
        print(final_output)

    elif last_agent == devops_agent:
        # Example: Read a file from GitHub
        owner = "your_github_username"
        repo = "your_repository_name"
        file_path = "path/to/your/file.py"
        try:
            file_content = read_file_from_github(owner, repo, file_path)
            print("File content retrieved from GitHub:")
            print(file_content)
        except Exception as e:
            print(f"Error retrieving file: {e}")

        # Example: Update a file on GitHub
        new_content = "print('Updated content')"
        commit_message = "Update file with new content"
        try:
            update_response = update_file_on_github(owner, repo, file_path, new_content, commit_message)
            print("File successfully updated on GitHub.")
        except Exception as e:
            print(f"Error updating file: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
