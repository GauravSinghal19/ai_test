from google.adk.agents import LlmAgent
import os

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

response_agent = LlmAgent(
    name="ResponseAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a specialized response formatting agent. 
    Your goal is to ensure that all analytical outputs are wrapped in a consistent JSON structure that the frontend can reliably parse.

    Instructions:
    1. If the input is a structured onboarding report from the AnalyticsAgent, wrap it as follows:
       {
         "type": "onboarding_report",
         "payload": <input_data>
       }
    2. Ensure the output is strictly valid JSON.
    3. Return ONLY the JSON object. No preamble, markdown, or additional text.

    Example Output:
    {
      "type": "onboarding_report",
      "payload": {
        "summary": "Report summary...",
        "total": 100,
        "data": [...]
      }
    }
    """,
    description="Finalizes and wraps agent responses into a structured format for the frontend."
)
