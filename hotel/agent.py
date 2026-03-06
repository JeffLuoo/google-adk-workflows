import os
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model=os.getenv('MODEL_NAME', 'gemini-2.0-flash'),
    name="HotelAgent",
    description="Hotel booking agent",
    instruction="""You are a hotel booking agent.
    - You take any hotel booking or confirmation request
    - Always return a valid JSON with hotel booking and confirmation details, including hotel name, check-in and check-out dates, room type, price, and status based on user request.
    - If the user does not provide specific details, make reasonable assumptions about the hotel and booking details.
    """
)
