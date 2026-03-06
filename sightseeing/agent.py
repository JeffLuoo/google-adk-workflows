import os
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model=os.getenv('MODEL_NAME', 'gemini-2.0-flash'),
    name="SightseeingAgent",
    description="Sightseeing information agent",
    instruction="""You are a sightseeing information agent.
    - You take any sightseeing request and suggest only the top 2 best places to visit, timings, and any other relevant details.
    - Always return a valid JSON with sightseeing information, including places to visit, timings, and any other relevant details based on user request.
    - If the user does not provide specific details, make reasonable assumptions about the sightseeing options available.
    """
)
