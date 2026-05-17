import os
from dotenv import load_dotenv
from google.adk.agents import LlmAgent

# Load environment variables
load_dotenv()

GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
USE_VERTEXAI = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "FALSE")

# Configure environment for ADK / Vertex AI
if USE_VERTEXAI.upper() == "TRUE":
    os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "TRUE"
    if GCP_PROJECT_ID:
        os.environ["GOOGLE_CLOUD_PROJECT"] = GCP_PROJECT_ID
    if GCP_LOCATION:
        os.environ["GOOGLE_CLOUD_LOCATION"] = GCP_LOCATION

from google.adk.tools import AgentTool

# Import sub-agents after env vars are set (since they use GEMINI_MODEL)
from subagents.calculator_agent import calculator_agent
from subagents.weather_agent import weather_agent
from subagents.date_range_agent import date_range_agent
from subagents.sql_agent import sql_agent
from subagents.analytics_agent import analytics_agent
from subagents.response_agent import response_agent

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
    - If the user asks for a UPC onboarding report or analytics:
        1. Call the DateRangeAgent tool to parse the time interval.
        2. Pass those dates to the SqlAgent tool to fetch the counts.
        3. Pass those counts to the AnalyticsAgent tool to process the metrics.
        4. Pass the metrics to the ResponseAgent tool to format the final JSON output.
        5. Return the final output from the ResponseAgent.
    
    For general conversation, handle it yourself.
    """,
    sub_agents=[
        calculator_agent, 
        weather_agent
    ],
    tools=[
        AgentTool(date_range_agent),
        AgentTool(sql_agent),
        AgentTool(analytics_agent),
        AgentTool(response_agent)
    ]
)
