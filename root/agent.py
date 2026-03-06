import os
import urllib.request
import json
import uuid
from google.adk.agents import LlmAgent
from google.adk.tools import function_tool

def call_adk_agent(agent_url: str, agent_app_name: str, request_text: str) -> str:
    user_id = "user1"
    session_id = str(uuid.uuid4())
    base_url = agent_url.rstrip('/')
    
    # Attempt to create session (may fail if already exists or not strictly required)
    try:
        session_req = urllib.request.Request(
            f"{base_url}/apps/{agent_app_name}/users/{user_id}/sessions",
            data=b'',
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        resp = urllib.request.urlopen(session_req)
        session_data = json.loads(resp.read().decode())
        if "id" in session_data:
            session_id = session_data["id"]
    except Exception as e:
        print(f"Session creation error (ignoring): {e}")

    # Call /run endpoint
    run_url = f"{base_url}/run"
    data = json.dumps({
        "appName": agent_app_name,
        "userId": user_id,
        "sessionId": session_id,
        "newMessage": {
            "role": "user",
            "parts": [{"text": request_text}]
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(run_url, data=data, headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode("utf-8"))
        output = []
        for event in result:
            if "content" in event and event["content"]:
                for part in event["content"].get("parts", []):
                    if "text" in part:
                        output.append(part["text"])
        return "\n".join(output) if output else json.dumps(result)
    except Exception as e:
        return f"Error calling {agent_app_name} at {run_url}: {e}"

def invoke_flight_agent(request: str) -> str:
    """Flight booking agent."""
    url = os.getenv("FLIGHT_AGENT_URL", "http://multi-adk-flight:8080")
    return call_adk_agent(url, "flight", request)

def invoke_hotel_agent(request: str) -> str:
    """Hotel booking agent."""
    url = os.getenv("HOTEL_AGENT_URL", "http://multi-adk-hotel:8080")
    return call_adk_agent(url, "hotel", request)

def invoke_sightseeing_agent(request: str) -> str:
    """Sightseeing information agent."""
    url = os.getenv("SIGHTSEEING_AGENT_URL", "http://multi-adk-sightseeing:8080")
    return call_adk_agent(url, "sightseeing", request)

flight_tool = function_tool.FunctionTool(func=invoke_flight_agent)
hotel_tool = function_tool.FunctionTool(func=invoke_hotel_agent)
sightseeing_tool = function_tool.FunctionTool(func=invoke_sightseeing_agent)

root_agent = LlmAgent(
    model=os.getenv('MODEL_NAME', 'gemini-2.0-flash'),
    name="TripPlanner",
    instruction="""
    Acts as a comprehensive trip planner.
    - Use the FlightAgent to find and book flights
    - Use the HotelAgent to find and book accommodation
    - Use the SightseeingAgent to find information on places to visit
    - Coordinate between all agents to provide complete trip planning
    - Ensure all user requirements are met across flight, hotel, and sightseeing needs
    """,
    tools=[flight_tool, hotel_tool, sightseeing_tool]
)
