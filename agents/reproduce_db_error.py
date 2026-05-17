import asyncio
from subagents.sql_agent import query_onboarding_metrics

async def reproduce_error():
    print("--- Attempting DB Connection ---")
    start = "2026-05-09 00:00:00"
    end = "2026-05-16 23:59:59"
    
    result = await query_onboarding_metrics(start, end)
    print(f"\n--- Tool Result ---\n{result}")

if __name__ == "__main__":
    asyncio.run(reproduce_error())
