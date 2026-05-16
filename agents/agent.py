import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# Load environment variables
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

# Configure environment for ADK / Vertex AI
if USE_VERTEXAI.upper() == "TRUE":
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
    if GCP_PROJECT_ID:
        os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT_ID
    if GCP_LOCATION:
        os.environ["GOOGLE_CLOUD_LOCATION"] = GCP_LOCATION

# Import sub-agents after env vars are set (since they use GEMINI_MODEL)
from subagents.calculator_agent import calculator_agent
from subagents.weather_agent import weather_agent

# Define the root Coordinator agent
root_agent = LlmAgent(
    name="Coordinator",
    model=GEMINI_MODEL,
    instruction="""
    You are the primary interface for the AI Chat System. 
    Your goal is to help the user by either answering their questions directly 
    or delegating the task to one of your specialized sub-agents.

    - If the user needs math or calculations, delegate to the CalculatorAgent.
    - If the user asks about the weather, delegate to the WeatherAgent.
    - For general conversation, handle it yourself.
    """,
    sub_agents=[calculator_agent, weather_agent]
)
