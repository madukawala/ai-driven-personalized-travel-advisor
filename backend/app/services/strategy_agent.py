"""
Strategy Agent: Generates personalized travel itineraries
- Combines weather forecasts, RAG insights, and user preferences
- Generates day-by-day itineraries
- Suggests optimizations and alternatives
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import logging
from ..rag.ollama_client import OllamaClient

logger = logging.getLogger(__name__)


class StrategyAgent:
    """Agent responsible for generating travel strategies and itineraries"""

    def __init__(self, ollama_client: OllamaClient = None):
        """Initialize strategy agent"""
        self.ollama_client = ollama_client or OllamaClient()

    async def generate_itinerary(
        self,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        budget: float,
        interests: List[str],
        constraints: Dict[str, Any],
        weather_data: Dict[str, Any],
        knowledge_snippets: List[Dict[str, Any]],
        events: List[Dict[str, Any]],
        risk_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate comprehensive trip itinerary

        Args:
            destination: Destination location
            start_date: Trip start date
            end_date: Trip end date
            budget: Trip budget
            interests: User interests
            constraints: User constraints
            weather_data: Weather forecast data
            knowledge_snippets: RAG retrieved knowledge
            events: Local events
            risk_analysis: Risk analysis results

        Returns:
            Complete itinerary with daily plans
        """
        try:
            duration_days = (end_date - start_date).days + 1

            # Generate itinerary using LLM
            itinerary_prompt = self._build_itinerary_prompt(
                destination,
                start_date,
                end_date,
                budget,
                interests,
                constraints,
                weather_data,
                knowledge_snippets,
                events,
                risk_analysis,
            )

            system_prompt = (
                "You are an expert travel planner. Generate detailed, practical, "
                "and personalized travel itineraries based on user preferences, "
                "weather conditions, and local insights. Focus on creating balanced "
                "daily schedules that maximize enjoyment while respecting budget and constraints."
            )

            response = await self.ollama_client.generate(
                itinerary_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
            )

            # Parse and structure the itinerary
            structured_itinerary = await self._structure_itinerary(
                response,
                destination,
                start_date,
                duration_days,
                budget,
                weather_data,
                events,
            )

            return structured_itinerary

        except Exception as e:
            logger.error(f"Error generating itinerary: {e}")
            return self._generate_fallback_itinerary(
                destination, start_date, end_date, budget, interests
            )

    def _build_itinerary_prompt(
        self,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        budget: float,
        interests: List[str],
        constraints: Dict[str, Any],
        weather_data: Dict,
        knowledge_snippets: List[Dict],
        events: List[Dict],
        risk_analysis: Dict,
    ) -> str:
        """Build comprehensive prompt for itinerary generation"""

        duration_days = (end_date - start_date).days + 1

        prompt = f"""Create a detailed {duration_days}-day travel itinerary for {destination}.

**Trip Details:**
- Dates: {start_date.strftime('%B %d, %Y')} to {end_date.strftime('%B %d, %Y')}
- Budget: ${budget}
- Interests: {', '.join(interests)}

**User Constraints:**
{self._format_constraints(constraints)}

**Weather Forecast:**
{self._format_weather(weather_data)}

**Local Events:**
{self._format_events(events)}

**Travel Insights:**
{self._format_knowledge(knowledge_snippets)}

**Risk Considerations:**
{self._format_risks(risk_analysis)}

Generate a day-by-day itinerary with:
1. Morning, afternoon, and evening activities
2. Estimated costs for each activity
3. Transportation suggestions
4. Dining recommendations
5. Tips and alternatives for each day

Format the response as:
Day X (Date):
- Morning (9:00-12:00): [Activity] - [Location] - Cost: $X
  Tips: [practical tips]
- Afternoon (13:00-18:00): [Activity] - [Location] - Cost: $X
  Tips: [practical tips]
- Evening (19:00-22:00): [Activity] - [Location] - Cost: $X
  Tips: [practical tips]
Daily Total: $X
"""
        return prompt

    def _format_constraints(self, constraints: Dict) -> str:
        """Format user constraints for prompt"""
        if not constraints:
            return "No specific constraints"

        formatted = []
        if constraints.get("no_early_mornings"):
            formatted.append("- Start activities after 9:00 AM")
        if constraints.get("dietary"):
            formatted.append(f"- Dietary: {constraints['dietary']}")
        if constraints.get("pace"):
            formatted.append(f"- Preferred pace: {constraints['pace']}")

        return "\n".join(formatted) if formatted else "No specific constraints"

    def _format_weather(self, weather_data: Dict) -> str:
        """Format weather data for prompt"""
        forecast = weather_data.get("forecast", [])
        if not forecast:
            return "Weather data unavailable"

        formatted = []
        for day in forecast[:5]:  # First 5 days
            formatted.append(
                f"- {day['date']}: {day['condition']}, "
                f"H: {day['temperature_high']}°C, L: {day['temperature_low']}°C, "
                f"Rain: {day['precipitation_chance']}%"
            )

        return "\n".join(formatted)

    def _format_events(self, events: List[Dict]) -> str:
        """Format events for prompt"""
        if not events:
            return "No major events during this period"

        formatted = []
        for event in events[:5]:  # Top 5 events
            formatted.append(
                f"- {event['date']}: {event['name']} "
                f"(Category: {event['category']}, Cost: ${event['estimated_cost']})"
            )

        return "\n".join(formatted)

    def _format_knowledge(self, knowledge: List[Dict]) -> str:
        """Format RAG knowledge for prompt"""
        if not knowledge:
            return "No specific insights available"

        formatted = []
        for snippet in knowledge[:3]:  # Top 3 snippets
            text = snippet.get("text", "")
            source = snippet.get("source_name", "Travel Guide")
            # Truncate long texts
            summary = text[:300] + "..." if len(text) > 300 else text
            formatted.append(f"- {source}: {summary}")

        return "\n".join(formatted)

    def _format_risks(self, risk_analysis: Dict) -> str:
        """Format risk analysis for prompt"""
        formatted = []

        budget_risk = risk_analysis.get("budget_risk", {})
        if budget_risk.get("overrun_risk") in ["high", "medium"]:
            formatted.append(
                f"- Budget: {budget_risk['overrun_risk']} risk of overrun "
                f"({budget_risk.get('overrun_percentage', 0)}%)"
            )

        weather_risk = risk_analysis.get("weather_risk", {})
        if weather_risk.get("rainy_days", 0) > 0:
            formatted.append(
                f"- Weather: {weather_risk['rainy_days']} rainy days expected"
            )

        crowding_risk = risk_analysis.get("crowding_risk", {})
        if crowding_risk.get("risk_level") in ["high", "medium"]:
            formatted.append(
                f"- Crowding: {crowding_risk['risk_level']} crowding expected"
            )

        return "\n".join(formatted) if formatted else "No significant risks identified"

    async def _structure_itinerary(
        self,
        llm_response: str,
        destination: str,
        start_date: datetime,
        duration_days: int,
        budget: float,
        weather_data: Dict,
        events: List[Dict],
    ) -> Dict[str, Any]:
        """Structure LLM response into proper itinerary format"""

        # Parse the LLM response
        daily_plans = self._parse_daily_plans(llm_response, start_date, duration_days)

        # Create structured itinerary
        itinerary = {
            "destination": destination,
            "start_date": start_date.isoformat(),
            "end_date": (start_date + timedelta(days=duration_days - 1)).isoformat(),
            "total_days": duration_days,
            "budget": budget,
            "daily_itineraries": daily_plans,
            "summary": {
                "total_estimated_cost": sum(
                    day.get("estimated_cost", 0) for day in daily_plans
                ),
                "average_daily_cost": sum(
                    day.get("estimated_cost", 0) for day in daily_plans
                )
                / len(daily_plans)
                if daily_plans
                else 0,
            },
        }

        return itinerary

    def _parse_daily_plans(
        self, response: str, start_date: datetime, duration_days: int
    ) -> List[Dict[str, Any]]:
        """Parse LLM response into structured daily plans"""

        daily_plans = []

        # Split response by days
        lines = response.split("\n")
        current_day = None
        current_activities = []
        daily_cost = 0.0

        for line in lines:
            line = line.strip()

            # Detect day header
            if line.startswith("Day ") and ":" in line:
                # Save previous day
                if current_day is not None:
                    daily_plans.append({
                        "day_number": current_day,
                        "date": (start_date + timedelta(days=current_day - 1)).isoformat(),
                        "activities": current_activities,
                        "estimated_cost": daily_cost,
                    })

                # Start new day
                try:
                    day_num = int(line.split()[1])
                    current_day = day_num
                    current_activities = []
                    daily_cost = 0.0
                except:
                    pass

            # Parse activities (simplified parsing)
            elif "-" in line and current_day is not None:
                # Extract activity information
                activity = self._parse_activity_line(line)
                if activity:
                    current_activities.append(activity)
                    daily_cost += activity.get("cost", 0)

        # Add last day
        if current_day is not None:
            daily_plans.append({
                "day_number": current_day,
                "date": (start_date + timedelta(days=current_day - 1)).isoformat(),
                "activities": current_activities,
                "estimated_cost": daily_cost,
            })

        return daily_plans

    def _parse_activity_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single activity line (simplified)"""
        try:
            # Very basic parsing - in production, use more robust parsing
            parts = line.split(":")
            if len(parts) >= 2:
                time_part = parts[0].strip("- ")
                details_part = ":".join(parts[1:])

                # Extract cost if present
                cost = 0.0
                if "$" in details_part:
                    cost_str = details_part.split("$")[-1].split()[0]
                    try:
                        cost = float(cost_str)
                    except:
                        pass

                return {
                    "time_slot": time_part,
                    "description": details_part.strip(),
                    "cost": cost,
                }
        except Exception as e:
            logger.debug(f"Could not parse activity line: {line}")

        return None

    def _generate_fallback_itinerary(
        self,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        budget: float,
        interests: List[str],
    ) -> Dict[str, Any]:
        """Generate a basic fallback itinerary if LLM fails"""

        duration_days = (end_date - start_date).days + 1
        daily_budget = budget / duration_days

        daily_plans = []
        for i in range(duration_days):
            day_date = start_date + timedelta(days=i)
            daily_plans.append({
                "day_number": i + 1,
                "date": day_date.isoformat(),
                "activities": [
                    {
                        "time_slot": "Morning (9:00-12:00)",
                        "description": f"Explore {destination} - {interests[0] if interests else 'sightseeing'}",
                        "cost": daily_budget * 0.3,
                    },
                    {
                        "time_slot": "Afternoon (13:00-18:00)",
                        "description": f"Visit local attractions in {destination}",
                        "cost": daily_budget * 0.4,
                    },
                    {
                        "time_slot": "Evening (19:00-22:00)",
                        "description": "Dinner and local experience",
                        "cost": daily_budget * 0.3,
                    },
                ],
                "estimated_cost": daily_budget,
            })

        return {
            "destination": destination,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_days": duration_days,
            "budget": budget,
            "daily_itineraries": daily_plans,
            "summary": {
                "total_estimated_cost": budget,
                "average_daily_cost": daily_budget,
            },
            "note": "This is a basic itinerary. For personalized recommendations, please ensure Ollama is running.",
        }
