import os
from openai import OpenAI

# review_agent/agent.py

from agents import Agent

reviewer_agent = Agent(
    name="Review Agent",
    instructions=(
        "You review code for quality, potential issues, and adherence to best practices. "
        "Provide constructive feedback and suggest improvements where necessary."
    ),
    handoff_description="Handles code review tasks."
)

