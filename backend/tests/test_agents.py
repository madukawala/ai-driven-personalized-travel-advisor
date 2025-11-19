"""
Basic unit tests for agents
Run with: pytest tests/test_agents.py -v
"""

import pytest
from datetime import datetime, timedelta
from app.services.data_agent import DataAgent
from app.services.risk_agent import RiskAgent


@pytest.mark.asyncio
async def test_data_agent_weather():
    """Test Data Agent weather fetching"""
    agent = DataAgent()
    start_date = datetime.now()
    end_date = start_date + timedelta(days=5)

    result = await agent.fetch_weather_data("Tokyo", start_date, end_date)

    assert result is not None
    assert "location" in result
    assert "forecast" in result
    assert len(result["forecast"]) > 0


@pytest.mark.asyncio
async def test_data_agent_events():
    """Test Data Agent events fetching"""
    agent = DataAgent()
    start_date = datetime.now()
    end_date = start_date + timedelta(days=5)

    result = await agent.fetch_local_events("Tokyo", start_date, end_date)

    assert result is not None
    assert isinstance(result, list)


def test_risk_agent_budget():
    """Test Risk Agent budget analysis"""
    agent = RiskAgent()

    result = agent.analyze_budget_risk(
        budget=700,
        destination="Tokyo",
        duration_days=5,
        interests=["food", "culture"],
        exchange_rate=1.0,
    )

    assert result is not None
    assert "estimated_cost" in result
    assert "overrun_risk" in result
    assert result["overrun_risk"] in ["very low", "low", "medium", "high"]


def test_risk_agent_quality_score():
    """Test Risk Agent quality scoring"""
    agent = RiskAgent()

    budget_risk = {"overrun_risk": "low", "budget_ratio": 0.95}
    weather_risk = {"risk_level": "low", "rain_percentage": 20}
    crowding_risk = {"risk_level": "medium"}

    result = agent.calculate_trip_quality_score(
        budget_risk, weather_risk, crowding_risk, {}
    )

    assert result is not None
    assert "overall_score" in result
    assert 0 <= result["overall_score"] <= 100
    assert "comfort_level" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
