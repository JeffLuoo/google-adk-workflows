import os
from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model=os.getenv('MODEL_NAME', 'gemini-2.0-flash'),
    name="FlightAgent",
    description="Flight booking agent",
    instruction="""You are a flight booking agent.
    - You take any flight booking or confirmation request
    - You check for available flights based on user preferences
    - You return a valid JSON with flight booking and confirmation details, including flight number, departure and arrival times, airline, price, and status based on user request.
    - If the user does not provide specific details, make reasonable assumptions about the flight and booking details.
    """
)
