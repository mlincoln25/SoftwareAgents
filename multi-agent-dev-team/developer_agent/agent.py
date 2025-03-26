import os
from openai import OpenAI

# developer_agent/agent.py

from agents import Agent

developer_agent = Agent(
    name="Developer Agent",
    instructions=(
        "You are responsible for writing and modifying code based on user instructions. "
        "Ensure that the code is efficient, clean, and follows best practices."
    ),
    handoff_description="Handles code development tasks."
)
