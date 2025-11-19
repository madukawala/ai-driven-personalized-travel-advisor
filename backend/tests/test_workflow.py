"""
Test cases for LangGraph workflow and trip planning
Run with: pytest tests/test_workflow.py -v
"""

import pytest
from datetime import datetime, timedelta
from app.agents.langgraph_workflow import TripPlanningWorkflow, TripPlanningState


@pytest.fixture
def workflow():
    """Create workflow instance"""
    return TripPlanningWorkflow()


@pytest.fixture
def sample_trip_state():
    """Sample trip planning state"""
    start_date = datetime.now() + timedelta(days=30)
    end_date = start_date + timedelta(days=5)

    return {
        "destination": "Tokyo",
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat(),
        "budget": 800,
        "interests": ["food", "culture"],
        "constraints": {},
        "user_id": 1
    }


def test_workflow_initialization(workflow):
    """Test workflow initializes correctly"""
    assert workflow is not None
    assert workflow.data_agent is not None
    assert workflow.risk_agent is not None
    assert workflow.knowledge_agent is not None
    assert workflow.strategy_agent is not None


@pytest.mark.asyncio
async def test_workflow_run_complete(workflow, sample_trip_state):
    """Test complete workflow execution"""
    result = await workflow.run(sample_trip_state)

    assert result is not None
    assert "destination" in result
    assert result["destination"] == "Tokyo"


@pytest.mark.asyncio
async def test_workflow_fetch_data_node(workflow, sample_trip_state):
    """Test data fetching node"""
    # Create initial state
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints=sample_trip_state["constraints"],
        user_id=sample_trip_state["user_id"],
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={},
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="initialized",
        errors=[],
        warnings=[]
    )

    result = await workflow._fetch_data_node(state)

    assert result is not None
    assert "weather_data" in result
    assert "events_data" in result
    assert "current_step" in result
    assert result["current_step"] == "data_fetched"


@pytest.mark.asyncio
async def test_workflow_analyze_risks_node(workflow, sample_trip_state):
    """Test risk analysis node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={"forecast": []},
        events_data=[],
        safety_data={},
        exchange_rate={"rate": 1.0},
        knowledge_snippets=[],
        risk_analysis={},
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="data_fetched",
        errors=[],
        warnings=[]
    )

    result = await workflow._analyze_risks_node(state)

    assert result is not None
    assert "risk_analysis" in result
    assert result["current_step"] == "risks_analyzed"


@pytest.mark.asyncio
async def test_workflow_retrieve_knowledge_node(workflow, sample_trip_state):
    """Test knowledge retrieval node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={},
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="risks_analyzed",
        errors=[],
        warnings=[]
    )

    result = await workflow._retrieve_knowledge_node(state)

    assert result is not None
    assert "knowledge_snippets" in result
    assert isinstance(result["knowledge_snippets"], list)
    assert result["current_step"] == "knowledge_retrieved"


@pytest.mark.asyncio
async def test_workflow_check_major_issues_node(workflow, sample_trip_state):
    """Test major issues checking node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={
            "budget_risk": {"overrun_risk": "low", "estimated_cost": 700},
            "weather_risk": {"risk_level": "low"},
            "crowding_risk": {"risk_level": "low"},
            "quality_score": {"overall_score": 80}
        },
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="knowledge_retrieved",
        errors=[],
        warnings=[]
    )

    result = await workflow._check_major_issues_node(state)

    assert result is not None
    assert "requires_approval" in result
    assert isinstance(result["requires_approval"], bool)
    assert result["current_step"] == "approval_check"


@pytest.mark.asyncio
async def test_workflow_high_budget_risk_requires_approval(workflow, sample_trip_state):
    """Test that high budget risk triggers approval"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=500,  # Low budget
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={
            "budget_risk": {
                "overrun_risk": "high",
                "estimated_cost": 800,
                "overrun_percentage": 60
            },
            "weather_risk": {"risk_level": "low"},
            "crowding_risk": {"risk_level": "low"},
            "quality_score": {"overall_score": 50}
        },
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="knowledge_retrieved",
        errors=[],
        warnings=[]
    )

    result = await workflow._check_major_issues_node(state)

    assert result["requires_approval"] is True
    assert "Budget Alert" in result["approval_message"]


@pytest.mark.asyncio
async def test_workflow_generate_itinerary_node(workflow, sample_trip_state):
    """Test itinerary generation node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={},
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=True,
        current_step="approval_check",
        errors=[],
        warnings=[]
    )

    result = await workflow._generate_itinerary_node(state)

    assert result is not None
    assert "itinerary" in result
    assert result["current_step"] == "itinerary_generated"


@pytest.mark.asyncio
async def test_workflow_optimize_itinerary_node(workflow, sample_trip_state):
    """Test itinerary optimization node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={
            "forecast": [
                {"date": "2024-09-01", "condition": "Rainy", "precipitation_chance": 80}
            ]
        },
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={
            "budget_risk": {"overrun_risk": "medium"}
        },
        itinerary={
            "daily_itineraries": [
                {"day": 1, "activities": []}
            ],
            "summary": {"total_estimated_cost": 900}
        },
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=True,
        current_step="itinerary_generated",
        errors=[],
        warnings=[]
    )

    result = await workflow._optimize_itinerary_node(state)

    assert result is not None
    assert result["current_step"] == "itinerary_optimized"


@pytest.mark.asyncio
async def test_workflow_finalize_node(workflow, sample_trip_state):
    """Test finalization node"""
    state = TripPlanningState(
        destination=sample_trip_state["destination"],
        start_date=sample_trip_state["start_date"],
        end_date=sample_trip_state["end_date"],
        budget=sample_trip_state["budget"],
        interests=sample_trip_state["interests"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={
            "quality_score": {"overall_score": 85}
        },
        itinerary={
            "summary": {"total_estimated_cost": 750}
        },
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=True,
        current_step="itinerary_optimized",
        errors=[],
        warnings=[]
    )

    result = await workflow._finalize_node(state)

    assert result is not None
    assert result["current_step"] == "completed"
    assert "summary_message" in result


@pytest.mark.asyncio
async def test_workflow_error_handling(workflow):
    """Test workflow error handling with invalid data"""
    invalid_state = {
        "destination": "",  # Empty destination
        "start_date": "invalid-date",
        "end_date": "invalid-date",
        "budget": -100,  # Negative budget
        "interests": [],
        "constraints": {},
        "user_id": 1
    }

    result = await workflow.run(invalid_state)

    # Should handle errors gracefully
    assert result is not None


def test_workflow_should_request_approval_logic(workflow):
    """Test approval request logic"""
    # Low risk state - no approval needed
    state_low_risk = TripPlanningState(
        destination="Tokyo",
        start_date="2024-09-01",
        end_date="2024-09-05",
        budget=1000,
        interests=["food"],
        constraints={},
        user_id=1,
        weather_data={},
        events_data=[],
        safety_data={},
        exchange_rate={},
        knowledge_snippets=[],
        risk_analysis={},
        itinerary={},
        requires_approval=False,
        approval_message="",
        approval_data={},
        user_approved=False,
        current_step="approval_check",
        errors=[],
        warnings=[]
    )

    decision = workflow._should_request_approval(state_low_risk)
    assert decision == "generate_itinerary"

    # High risk state - approval needed
    state_high_risk = state_low_risk.copy()
    state_high_risk["requires_approval"] = True

    decision = workflow._should_request_approval(state_high_risk)
    assert decision == "generate_itinerary"  # Still proceeds with assumed approval


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
