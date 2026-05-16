from google.adk.agents import LlmAgent
import os

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

calculator_agent = LlmAgent(
    name="CalculatorAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a math expert. 
    Perform any calculations requested by the user. 
    Always show your work and provide clear, step-by-step explanations.
    """,
    description="Useful for performing mathematical calculations and solving word problems."
    tools=[apis]
)
