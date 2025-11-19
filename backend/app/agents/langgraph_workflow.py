"""
LangGraph Workflow: Orchestrates the multi-step AI workflow for trip planning
- Implements state machine for trip planning
- Includes human-in-the-loop checkpoints
- Conditional logic based on risks and user preferences
"""

from typing import Dict, Any, List, TypedDict, Annotated
from datetime import datetime
import logging
from ..services.data_agent import DataAgent
from ..services.risk_agent import RiskAgent
from ..services.knowledge_agent import KnowledgeAgent
from ..services.strategy_agent import StrategyAgent
from ..rag.vector_store import VectorStore
from ..rag.ollama_client import OllamaClient

# Workaround for Python 3.14 compatibility - import langgraph components lazily
try:
    from langgraph.graph import StateGraph, END
    from langgraph.checkpoint import MemorySaver
    LANGGRAPH_AVAILABLE = True
except Exception as e:
    logging.warning(f"LangGraph not fully compatible, using simplified workflow: {e}")
    LANGGRAPH_AVAILABLE = False
    END = "END"

logger = logging.getLogger(__name__)


class TripPlanningState(TypedDict):
    """State schema for trip planning workflow"""

    # User input
    destination: str
    start_date: str
    end_date: str
    budget: float
    interests: List[str]
    constraints: Dict[str, Any]
    user_id: int

    # Collected data
    weather_data: Dict[str, Any]
    events_data: List[Dict[str, Any]]
    safety_data: Dict[str, Any]
    exchange_rate: Dict[str, Any]

    # Analysis results
    knowledge_snippets: List[Dict[str, Any]]
    risk_analysis: Dict[str, Any]

    # Generated itinerary
    itinerary: Dict[str, Any]

    # Human-in-the-loop
    requires_approval: bool
    approval_message: str
    approval_data: Dict[str, Any]
    user_approved: bool

    # Workflow control
    current_step: str
    errors: List[str]
    warnings: List[str]


class TripPlanningWorkflow:
    """LangGraph workflow for trip planning"""

    def __init__(self):
        """Initialize workflow with agents"""
        self.data_agent = DataAgent()
        self.risk_agent = RiskAgent()
        self.knowledge_agent = KnowledgeAgent()
        self.strategy_agent = StrategyAgent()

        # Build workflow graph
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph workflow"""

        if not LANGGRAPH_AVAILABLE:
            # Return None - we'll use simplified sequential workflow
            logger.warning("Using simplified sequential workflow (LangGraph not available)")
            return None

        # Create graph
        workflow = StateGraph(TripPlanningState)

        # Add nodes
        workflow.add_node("fetch_data", self._fetch_data_node)
        workflow.add_node("analyze_risks", self._analyze_risks_node)
        workflow.add_node("retrieve_knowledge", self._retrieve_knowledge_node)
        workflow.add_node("check_major_issues", self._check_major_issues_node)
        workflow.add_node("generate_itinerary", self._generate_itinerary_node)
        workflow.add_node("optimize_itinerary", self._optimize_itinerary_node)
        workflow.add_node("finalize", self._finalize_node)

        # Set entry point
        workflow.set_entry_point("fetch_data")

        # Add edges
        workflow.add_edge("fetch_data", "analyze_risks")
        workflow.add_edge("analyze_risks", "retrieve_knowledge")
        workflow.add_edge("retrieve_knowledge", "check_major_issues")

        # Conditional edge based on risk analysis
        workflow.add_conditional_edges(
            "check_major_issues",
            self._should_request_approval,
            {
                "generate_itinerary": "generate_itinerary",
                "end": END,  # If user doesn't approve major changes
            },
        )

        workflow.add_edge("generate_itinerary", "optimize_itinerary")
        workflow.add_edge("optimize_itinerary", "finalize")
        workflow.add_edge("finalize", END)

        return workflow.compile()

    async def _fetch_data_node(self, state: TripPlanningState) -> TripPlanningState:
        """Node: Fetch real-time data"""
        logger.info("Fetching real-time data...")

        try:
            start_date = datetime.fromisoformat(state["start_date"])
            end_date = datetime.fromisoformat(state["end_date"])

            # Fetch all data
            data = await self.data_agent.fetch_all_data(
                state["destination"],
                start_date,
                end_date,
                state.get("budget_currency", "USD"),
            )

            state["weather_data"] = data.get("weather", {})
            state["events_data"] = data.get("events", [])
            state["safety_data"] = data.get("safety", {})
            state["exchange_rate"] = data.get("exchange_rate")
            state["current_step"] = "data_fetched"

        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            state.setdefault("errors", []).append(f"Data fetch error: {str(e)}")

        return state

    async def _analyze_risks_node(self, state: TripPlanningState) -> TripPlanningState:
        """Node: Analyze risks"""
        logger.info("Analyzing risks...")

        try:
            start_date = datetime.fromisoformat(state["start_date"])
            end_date = datetime.fromisoformat(state["end_date"])

            exchange_rate = 1.0
            if state.get("exchange_rate"):
                exchange_rate = state["exchange_rate"].get("rate", 1.0)

            # Perform risk analysis
            risk_analysis = self.risk_agent.analyze_all_risks(
                budget=state["budget"],
                destination=state["destination"],
                start_date=start_date,
                end_date=end_date,
                interests=state["interests"],
                weather_data=state["weather_data"],
                events=state["events_data"],
                exchange_rate=exchange_rate,
            )

            state["risk_analysis"] = risk_analysis
            state["current_step"] = "risks_analyzed"

        except Exception as e:
            logger.error(f"Error analyzing risks: {e}")
            state.setdefault("errors", []).append(f"Risk analysis error: {str(e)}")

        return state

    async def _retrieve_knowledge_node(
        self, state: TripPlanningState
    ) -> TripPlanningState:
        """Node: Retrieve knowledge from RAG"""
        logger.info("Retrieving knowledge...")

        try:
            # Build query from user input
            query = f"Travel to {state['destination']} {' '.join(state['interests'])}"

            # Retrieve knowledge
            knowledge = await self.knowledge_agent.retrieve_knowledge(
                query=query,
                location=state["destination"],
                user_interests=state["interests"],
                top_k=5,
            )

            state["knowledge_snippets"] = knowledge
            state["current_step"] = "knowledge_retrieved"

        except Exception as e:
            logger.error(f"Error retrieving knowledge: {e}")
            state.setdefault("errors", []).append(
                f"Knowledge retrieval error: {str(e)}"
            )
            state["knowledge_snippets"] = []

        return state

    async def _check_major_issues_node(
        self, state: TripPlanningState
    ) -> TripPlanningState:
        """Node: Check for major issues requiring approval"""
        logger.info("Checking for major issues...")

        requires_approval = False
        approval_message = ""
        approval_data = {}

        # Check budget overrun
        budget_risk = state["risk_analysis"].get("budget_risk", {})
        if budget_risk.get("overrun_risk") == "high":
            requires_approval = True
            overrun_pct = budget_risk.get("overrun_percentage", 0)
            approval_message += (
                f"⚠️ Budget Alert: Estimated costs are {overrun_pct}% over your budget. "
                f"Estimated: ${budget_risk['estimated_cost']}, Budget: ${state['budget']}. "
            )
            approval_data["budget_overrun"] = {
                "estimated": budget_risk["estimated_cost"],
                "budget": state["budget"],
                "overrun_percentage": overrun_pct,
            }

        # Check weather risks
        weather_risk = state["risk_analysis"].get("weather_risk", {})
        if weather_risk.get("risk_level") == "high":
            rainy_days = weather_risk.get("rainy_days", 0)
            total_days = weather_risk.get("total_days", 1)
            approval_message += (
                f"🌧️ Weather Alert: {rainy_days} out of {total_days} days expected to have rain (>60% chance). "
            )
            approval_data["weather_risk"] = {
                "rainy_days": rainy_days,
                "total_days": total_days,
            }

        # Check crowding
        crowding_risk = state["risk_analysis"].get("crowding_risk", {})
        if crowding_risk.get("risk_level") == "high":
            requires_approval = True
            events = crowding_risk.get("major_events", [])
            approval_message += (
                f"👥 Crowding Alert: Major events or holidays will cause high crowding. "
                f"Events: {', '.join([e['name'] for e in events[:2]])}. "
            )
            approval_data["crowding"] = {"events": events}

        # Check quality score
        quality_score = state["risk_analysis"].get("quality_score", {})
        if quality_score.get("overall_score", 100) < 50:
            requires_approval = True
            approval_message += (
                f"📊 Quality Alert: Trip quality score is low ({quality_score['overall_score']}/100). "
            )
            approval_data["low_quality"] = quality_score

        if requires_approval:
            approval_message += "\n\nWould you like to:\n"
            approval_message += "1. Proceed with adjustments\n"
            approval_message += "2. Change dates or destination\n"
            approval_message += "3. Adjust budget\n"

        state["requires_approval"] = requires_approval
        state["approval_message"] = approval_message
        state["approval_data"] = approval_data
        state["current_step"] = "approval_check"

        return state

    def _should_request_approval(
        self, state: TripPlanningState
    ) -> str:
        """Conditional edge: Determine if approval is needed"""
        if state.get("requires_approval", False):
            # In a real application, this would pause and wait for user input
            # For now, we'll assume approval
            logger.info("Approval required - assuming user approved")
            state["user_approved"] = True

        # Continue to itinerary generation
        return "generate_itinerary"

    async def _generate_itinerary_node(
        self, state: TripPlanningState
    ) -> TripPlanningState:
        """Node: Generate travel itinerary"""
        logger.info("Generating itinerary...")

        try:
            start_date = datetime.fromisoformat(state["start_date"])
            end_date = datetime.fromisoformat(state["end_date"])

            # Generate itinerary
            itinerary = await self.strategy_agent.generate_itinerary(
                destination=state["destination"],
                start_date=start_date,
                end_date=end_date,
                budget=state["budget"],
                interests=state["interests"],
                constraints=state["constraints"],
                weather_data=state["weather_data"],
                knowledge_snippets=state["knowledge_snippets"],
                events=state["events_data"],
                risk_analysis=state["risk_analysis"],
            )

            state["itinerary"] = itinerary
            state["current_step"] = "itinerary_generated"

        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            state.setdefault("errors", []).append(
                f"Itinerary generation error: {str(e)}"
            )

        return state

    async def _optimize_itinerary_node(
        self, state: TripPlanningState
    ) -> TripPlanningState:
        """Node: Optimize itinerary based on conditions"""
        logger.info("Optimizing itinerary...")

        try:
            itinerary = state.get("itinerary", {})
            weather_data = state.get("weather_data", {})

            # Apply weather-based optimizations
            if weather_data:
                itinerary = self._apply_weather_optimizations(
                    itinerary, weather_data
                )

            # Apply budget optimizations if needed
            budget_risk = state["risk_analysis"].get("budget_risk", {})
            if budget_risk.get("overrun_risk") in ["high", "medium"]:
                itinerary = self._apply_budget_optimizations(
                    itinerary, state["budget"]
                )

            state["itinerary"] = itinerary
            state["current_step"] = "itinerary_optimized"

        except Exception as e:
            logger.error(f"Error optimizing itinerary: {e}")
            state.setdefault("warnings", []).append(
                f"Optimization warning: {str(e)}"
            )

        return state

    def _apply_weather_optimizations(
        self, itinerary: Dict, weather_data: Dict
    ) -> Dict:
        """Apply weather-based optimizations to itinerary"""

        forecast = weather_data.get("forecast", [])
        if not forecast:
            return itinerary

        daily_itineraries = itinerary.get("daily_itineraries", [])

        for i, day in enumerate(daily_itineraries):
            if i < len(forecast):
                day_forecast = forecast[i]

                # Add weather info to day
                day["weather"] = {
                    "condition": day_forecast.get("condition"),
                    "high": day_forecast.get("temperature_high"),
                    "low": day_forecast.get("temperature_low"),
                    "rain_chance": day_forecast.get("precipitation_chance"),
                }

                # Add weather recommendation
                if day_forecast.get("precipitation_chance", 0) > 60:
                    day.setdefault("recommendations", []).append(
                        "⛈️ High chance of rain - consider indoor activities or bring rain gear"
                    )

                if day_forecast.get("temperature_high", 25) > 32:
                    day.setdefault("recommendations", []).append(
                        "🌡️ Hot day expected - stay hydrated and plan indoor activities during peak heat"
                    )

        return itinerary

    def _apply_budget_optimizations(
        self, itinerary: Dict, budget: float
    ) -> Dict:
        """Apply budget optimizations to itinerary"""

        estimated_cost = itinerary.get("summary", {}).get("total_estimated_cost", 0)

        if estimated_cost > budget:
            overrun_pct = ((estimated_cost - budget) / budget) * 100
            itinerary.setdefault("warnings", []).append(
                f"⚠️ Estimated cost (${estimated_cost:.2f}) exceeds budget (${budget:.2f}) by {overrun_pct:.1f}%"
            )
            itinerary.setdefault("recommendations", []).append(
                "Consider reducing expensive activities, dining at mid-range restaurants, or using public transportation"
            )

        return itinerary

    async def _finalize_node(self, state: TripPlanningState) -> TripPlanningState:
        """Node: Finalize trip plan"""
        logger.info("Finalizing trip plan...")

        # Add final summary
        state["current_step"] = "completed"

        # Generate summary message
        quality_score = state["risk_analysis"].get("quality_score", {})
        summary_message = (
            f"✅ Trip plan completed for {state['destination']}!\n"
            f"Quality Score: {quality_score.get('overall_score', 'N/A')}/100\n"
            f"Total Estimated Cost: ${state['itinerary'].get('summary', {}).get('total_estimated_cost', 0):.2f}"
        )

        state["summary_message"] = summary_message

        return state

    async def run(self, initial_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Run the workflow

        Args:
            initial_state: Initial state with user input

        Returns:
            Final state with completed trip plan
        """
        try:
            logger.info("Starting trip planning workflow...")

            # Initialize state
            state = TripPlanningState(
                destination=initial_state["destination"],
                start_date=initial_state["start_date"],
                end_date=initial_state["end_date"],
                budget=initial_state["budget"],
                interests=initial_state.get("interests", []),
                constraints=initial_state.get("constraints", {}),
                user_id=initial_state.get("user_id", 1),
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
                warnings=[],
            )

            # Execute workflow
            if self.graph is not None and LANGGRAPH_AVAILABLE:
                result = await self.graph.ainvoke(state)
            else:
                # Simplified sequential workflow for Python 3.14 compatibility
                logger.info("Using simplified sequential workflow")
                state = await self._fetch_data_node(state)
                state = await self._analyze_risks_node(state)
                state = await self._retrieve_knowledge_node(state)
                state = await self._check_major_issues_node(state)

                # Check if approval needed
                if not state.get("requires_approval", False) or state.get("user_approved", True):
                    state = await self._generate_itinerary_node(state)
                    state = await self._optimize_itinerary_node(state)
                    state = await self._finalize_node(state)

                result = state

            logger.info("Workflow completed successfully")
            return result

        except Exception as e:
            logger.error(f"Workflow error: {e}")
            return {
                "error": str(e),
                "current_step": "failed",
            }
