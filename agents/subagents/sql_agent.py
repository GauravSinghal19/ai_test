from google.adk.agents import LlmAgent
import os
from sqlalchemy import text
from datetime import datetime
from db import get_db_session
import json

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

async def query_onboarding_metrics(start_date: str, end_date: str, system: str = None) -> str:
    """
    Queries the database for UPC onboarding counts within a specific date range.
    
    Args:
        start_date: Start timestamp (YYYY-MM-DD HH:MM:SS)
        end_date: End timestamp (YYYY-MM-DD HH:MM:SS)
        system: Optional specific system to query ('Affinity', 'STEP', or 'Stella'). If omitted, all are queried.
        
    Returns:
        A JSON string containing the counts per system.
    """
    try:
        # Validate date formats
        datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return json.dumps({"error": "Invalid date format. Expected YYYY-MM-DD HH:MM:SS"})

    try:
        with get_db_session() as session:
            results = {}
            
            # These are placeholder queries based on the project specs.
            # In a real production environment, these would be refined.
            queries = {
                "Affinity": """
                    SELECT COUNT(distinct m.upc) as upc_count
                    FROM epc_translation.ep_messages m
                    JOIN epc_orch.epc_create_auto_pdf p ON m.upc = p.upc_id
                    WHERE p.status = 'SUCCESS' and m.message = 'SUCCESS' AND p.file_name LIKE '%create%'
                    AND m.create_timestamp BETWEEN :start AND :end
                """,
                "STEP": """
                    SELECT COUNT(DISTINCT p.upc_id) AS upc_count
                    FROM epc_orch.epc_create_auto_pdf p
                    LEFT JOIN epc_translation.ep_messages m
                           ON m.upc = p.upc_id
                    WHERE p.status = 'SUCCESS'
                      AND p.file_name LIKE '%create%'
                      AND m.upc IS NULL
                      AND p.create_ts BETWEEN :start AND :end
                """,
                "Stella": """
                    SELECT
                        COUNT(DISTINCT m.upc) as upc_count
                    FROM epc_translation.ep_messages m
                    INNER JOIN epc_orch.epc_create_auto_stella s
                        ON m.upc = s.upc_id
                    WHERE s.status = 'SUCCESS'
                    AND s.create_ts BETWEEN :start AND :end
                """
            }
            
            systems_to_query = [system] if system and system in queries else queries.keys()
            
            for sys in systems_to_query:
                stmt = text(queries[sys])
                result = session.execute(stmt, {"start": start_date, "end": end_date})
                row = result.fetchone()
                results[sys] = row[0] if row else 0
                
            return json.dumps(results)
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"DEBUG SQL: Error executing query: {e}")
        print(f"DEBUG SQL: Traceback:\n{error_trace}")
        return json.dumps({"error": f"Database connection error: {str(e)}"})

sql_agent = LlmAgent(
    name="SqlAgent",
    model=GEMINI_MODEL,
    instruction="""
    You are a data retrieval agent specialized in UPC onboarding metrics.
    Your primary responsibility is to fetch raw data from the database using the 'query_onboarding_metrics' tool.
    
    Instructions:
    1. When you receive a date range (start_date and end_date), call the tool.
    2. Do NOT attempt to process or aggregate the data yourself; return the raw JSON from the tool.
    3. If the tool returns an error, pass it along.
    """,
    tools=[query_onboarding_metrics],
    description="Fetches raw UPC onboarding counts from Affinity, STEP, and Stella databases."
)
