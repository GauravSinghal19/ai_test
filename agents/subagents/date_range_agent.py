from google.adk.agents import LlmAgent
import os
from datetime import datetime

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

# We provide the current date to help the LLM parse relative date ranges correctly.
CURRENT_DATE = datetime.now().strftime("%Y-%m-%d")

date_range_agent = LlmAgent(
    name="DateRangeAgent",
    model=GEMINI_MODEL,
    instruction=f"""
    You are a specialized agent for parsing natural language date ranges into a structured JSON format.
    The current date is {CURRENT_DATE}.

    Your task is to extract the start and end timestamps from the user's query.
    
    Rules:
    1. For relative ranges like "last week", calculate from 7 days ago to today.
    2. For "yesterday", use the start and end of the previous day.
    3. For a specific month like "March 2026", use the first day to the last day of that month.
    4. Always return a JSON object with the following keys:
       - "start_date": "YYYY-MM-DD 00:00:00"
       - "end_date": "YYYY-MM-DD 23:59:59"
    5. Return ONLY the JSON object. No preamble, no markdown formatting (unless specifically asked, but default to raw JSON).

    Example Response:
    {{"start_date": "2026-05-09 00:00:00", "end_date": "2026-05-16 23:59:59"}}
    """,
    description="Parses natural language date expressions (e.g., 'last week', 'March 2026') into structured start and end timestamps."
)
