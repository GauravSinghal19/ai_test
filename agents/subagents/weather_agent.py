from google.adk.agents import LlmAgent
import os

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

weather_agent = LlmAgent(
    name="WeatherAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a weather assistant. 
    Provide weather information for any location requested. 
    Since you don't have real-time access, you can simulate or provide general climate information.
    """,
    description="Useful for getting weather updates and climate information for different locations."
)
