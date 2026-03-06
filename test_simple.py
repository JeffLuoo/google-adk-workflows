import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_CLOUD_PROJECT"] = "jeffluoo-gke-dev"
os.environ["GOOGLE_CLOUD_LOCATION"] = "us-central1"

from simple.agent import root_agent

async def main():
    try:
        async for chunk in root_agent.run("Book a flight to Paris"):
            print("Chunk:", chunk)
    except Exception as e:
        import traceback
        traceback.print_exc()

asyncio.run(main())
