import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from subagents.sql_agent import query_onboarding_metrics

@pytest.mark.asyncio
async def test_query_onboarding_metrics_success():
    """
    Tests successful retrieval of onboarding metrics with mocked DB calls.
    """
    # Mocking the database session and its execute method
    mock_session = AsyncMock()
    
    # Mocking the result returned by session.execute
    mock_result = MagicMock()
    mock_result.fetchone.return_value = [10] # Return count of 10 for each query
    mock_session.execute.return_value = mock_result
    
    # Patch the get_db_session context manager
    with patch("subagents.sql_agent.get_db_session") as mock_get_db:
        # Mocking the async context manager behavior
        mock_get_db.return_value.__aenter__.return_value = mock_session
        
        start = "2026-05-01 00:00:00"
        end = "2026-05-31 23:59:59"
        
        # Execute the tool function
        result_json = await query_onboarding_metrics(start, end)
        result = json.loads(result_json)
        
        # Verify the results match our mock (10 for each of the 3 systems)
        assert result["Affinity"] == 10
        assert result["STEP"] == 10
        assert result["Stella"] == 10
        assert mock_session.execute.call_count == 3

@pytest.mark.asyncio
async def test_query_onboarding_metrics_system_filter():
    """
    Tests retrieval for a specific system only.
    """
    mock_session = AsyncMock()
    mock_result = MagicMock()
    mock_result.fetchone.return_value = [5]
    mock_session.execute.return_value = mock_result
    
    with patch("subagents.sql_agent.get_db_session") as mock_get_db:
        mock_get_db.return_value.__aenter__.return_value = mock_session
        
        start = "2026-05-01 00:00:00"
        end = "2026-05-31 23:59:59"
        
        # Request only Stella
        result_json = await query_onboarding_metrics(start, end, system="Stella")
        result = json.loads(result_json)
        
        assert "Stella" in result
        assert result["Stella"] == 5
        assert "Affinity" not in result
        assert "STEP" not in result
        assert mock_session.execute.call_count == 1

@pytest.mark.asyncio
async def test_query_onboarding_metrics_invalid_date():
    """
    Tests error handling for invalid date formats.
    """
    result_json = await query_onboarding_metrics("invalid", "date")
    result = json.loads(result_json)
    
    assert "error" in result
    assert "Invalid date format" in result["error"]
