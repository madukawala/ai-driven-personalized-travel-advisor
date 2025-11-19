"""
Risk Agent: Analyzes various risks for trip planning
- Budget overrun forecasts
- Weather risks
- Overbooking and holiday closure risks
- Safety risks
- Comfort and time-efficiency scoring
"""

from typing import Dict, Any, List
from datetime import datetime, timedelta
import logging
from ..utils.config import settings

logger = logging.getLogger(__name__)


class RiskAgent:
    """Agent responsible for analyzing trip risks"""

    def __init__(self):
        self.weather_risk_threshold = settings.WEATHER_RISK_THRESHOLD
        self.budget_overrun_threshold = settings.BUDGET_OVERRUN_THRESHOLD

    def analyze_budget_risk(
        self,
        budget: float,
        destination: str,
        duration_days: int,
        interests: List[str],
        exchange_rate: float = 1.0,
    ) -> Dict[str, Any]:
        """
        Analyze budget overrun risk based on destination and planned activities
        """
        # Estimate costs by destination (mock data - in production, use real data)
        destination_costs = {
            "tokyo": {"daily_base": 150, "multiplier": 1.3},
            "paris": {"daily_base": 140, "multiplier": 1.25},
            "london": {"daily_base": 160, "multiplier": 1.35},
            "bangkok": {"daily_base": 60, "multiplier": 0.9},
            "new york": {"daily_base": 180, "multiplier": 1.4},
            "rome": {"daily_base": 120, "multiplier": 1.15},
            "barcelona": {"daily_base": 110, "multiplier": 1.1},
            "default": {"daily_base": 100, "multiplier": 1.0},
        }

        # Get destination costs
        dest_key = destination.lower()
        costs = destination_costs.get(dest_key, destination_costs["default"])

        # Calculate base estimated cost
        daily_cost = costs["daily_base"]

        # Adjust based on interests
        activity_multipliers = {
            "food": 1.2,
            "fine dining": 1.4,
            "luxury": 1.5,
            "shopping": 1.3,
            "adventure": 1.15,
            "culture": 1.0,
            "art": 1.05,
            "nightlife": 1.2,
            "budget": 0.7,
        }

        interest_multiplier = 1.0
        for interest in interests:
            multiplier = activity_multipliers.get(interest.lower(), 1.0)
            interest_multiplier = max(interest_multiplier, multiplier)

        # Calculate estimated total cost
        estimated_cost = (
            daily_cost * duration_days * interest_multiplier * costs["multiplier"] * exchange_rate
        )

        # Budget analysis
        budget_ratio = estimated_cost / budget if budget > 0 else float("inf")
        overrun_risk = "low"
        overrun_percentage = 0

        if budget_ratio > 1.2:
            overrun_risk = "high"
            overrun_percentage = int((budget_ratio - 1) * 100)
        elif budget_ratio > 1.05:
            overrun_risk = "medium"
            overrun_percentage = int((budget_ratio - 1) * 100)
        elif budget_ratio > 0.95:
            overrun_risk = "low"
            overrun_percentage = 0
        else:
            overrun_risk = "very low"
            overrun_percentage = 0

        return {
            "estimated_cost": round(estimated_cost, 2),
            "budget": budget,
            "budget_ratio": round(budget_ratio, 2),
            "overrun_risk": overrun_risk,
            "overrun_percentage": overrun_percentage,
            "daily_estimated_cost": round(estimated_cost / duration_days, 2),
            "recommendations": self._generate_budget_recommendations(
                overrun_risk, budget_ratio, interests
            ),
        }

    def _generate_budget_recommendations(
        self, risk: str, ratio: float, interests: List[str]
    ) -> List[str]:
        """Generate budget recommendations based on risk"""
        recommendations = []

        if risk in ["high", "medium"]:
            recommendations.append(
                f"Your estimated costs are {int((ratio - 1) * 100)}% over budget."
            )
            recommendations.append("Consider reducing expensive activities or extending your budget.")

            if "food" in [i.lower() for i in interests]:
                recommendations.append(
                    "Mix high-end restaurants with local street food to save money."
                )
            if "shopping" in [i.lower() for i in interests]:
                recommendations.append(
                    "Allocate a specific shopping budget to avoid overspending."
                )
        else:
            recommendations.append("Your budget appears adequate for this trip.")
            if ratio < 0.8:
                recommendations.append(
                    "You have room in your budget for additional experiences or upgrades."
                )

        return recommendations

    def analyze_weather_risk(self, weather_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze weather risks for the trip
        """
        forecast = weather_data.get("forecast", [])

        if not forecast:
            return {
                "risk_level": "unknown",
                "rainy_days": 0,
                "extreme_weather_days": 0,
                "recommendations": ["Weather data unavailable"],
            }

        rainy_days = 0
        extreme_temp_days = 0
        hot_days = 0
        cold_days = 0

        for day in forecast:
            # Check rain probability
            if day.get("precipitation_chance", 0) > 60:
                rainy_days += 1

            # Check temperature extremes
            temp_high = day.get("temperature_high", 25)
            temp_low = day.get("temperature_low", 15)

            if temp_high > 35 or temp_low < 0:
                extreme_temp_days += 1

            if temp_high > 32:
                hot_days += 1
            if temp_low < 5:
                cold_days += 1

        total_days = len(forecast)
        rain_percentage = (rainy_days / total_days) * 100 if total_days > 0 else 0

        # Determine risk level
        if rain_percentage > 70:
            risk_level = "high"
        elif rain_percentage > 40:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "risk_level": risk_level,
            "rainy_days": rainy_days,
            "total_days": total_days,
            "rain_percentage": round(rain_percentage, 1),
            "extreme_weather_days": extreme_temp_days,
            "hot_days": hot_days,
            "cold_days": cold_days,
            "recommendations": self._generate_weather_recommendations(
                risk_level, rainy_days, hot_days, cold_days, forecast
            ),
        }

    def _generate_weather_recommendations(
        self, risk: str, rainy_days: int, hot_days: int, cold_days: int, forecast: List
    ) -> List[str]:
        """Generate weather-based recommendations"""
        recommendations = []

        if risk == "high":
            recommendations.append(
                f"High rain probability ({rainy_days} rainy days expected). Consider indoor activities."
            )
            recommendations.append(
                "Bring waterproof gear and plan alternative indoor attractions."
            )
        elif risk == "medium":
            recommendations.append(
                f"Moderate rain expected ({rainy_days} days). Pack an umbrella and have backup plans."
            )

        if hot_days > 0:
            recommendations.append(
                f"{hot_days} hot days expected. Stay hydrated and plan indoor activities during peak heat."
            )

        if cold_days > 0:
            recommendations.append(
                f"{cold_days} cold days expected. Pack warm clothing and layers."
            )

        # Suggest best days for outdoor activities
        if forecast:
            best_days = [
                day for day in forecast
                if day.get("precipitation_chance", 100) < 30
                and 18 < day.get("temperature_high", 0) < 30
            ]
            if best_days:
                best_day = best_days[0]
                recommendations.append(
                    f"Best weather on {best_day['date']} - ideal for outdoor activities."
                )

        return recommendations

    def analyze_crowding_risk(
        self, events: List[Dict[str, Any]], destination: str, dates: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze risk of overcrowding and holiday closures
        """
        # Check for major events
        high_popularity_events = [e for e in events if e.get("popularity") == "high"]
        event_days = set([e["date"] for e in events])

        # Mock holiday data (in production, use real holiday API)
        major_holidays = self._get_major_holidays(destination)
        holiday_dates = set([h["date"] for h in major_holidays])

        crowded_days = event_days.intersection(set(dates))
        holiday_dates_in_trip = holiday_dates.intersection(set(dates))

        risk_level = "low"
        if len(high_popularity_events) >= 2 or len(holiday_dates_in_trip) >= 1:
            risk_level = "high"
        elif len(high_popularity_events) == 1 or len(crowded_days) >= 2:
            risk_level = "medium"

        return {
            "risk_level": risk_level,
            "major_events": high_popularity_events,
            "crowded_days": list(crowded_days),
            "holidays": [h for h in major_holidays if h["date"] in holiday_dates_in_trip],
            "recommendations": self._generate_crowding_recommendations(
                risk_level, high_popularity_events, holiday_dates_in_trip
            ),
        }

    def _get_major_holidays(self, destination: str) -> List[Dict[str, Any]]:
        """Get major holidays for a destination (mock data)"""
        # This would come from a holidays API in production
        from datetime import datetime

        current_year = datetime.now().year

        # Sample holidays
        holidays = {
            "default": [
                {"name": "New Year's Day", "date": f"{current_year}-01-01"},
                {"name": "Christmas", "date": f"{current_year}-12-25"},
            ]
        }

        return holidays.get(destination.lower(), holidays["default"])

    def _generate_crowding_recommendations(
        self, risk: str, events: List, holidays: set
    ) -> List[str]:
        """Generate crowding recommendations"""
        recommendations = []

        if risk == "high":
            recommendations.append(
                "High crowding expected due to major events or holidays."
            )
            recommendations.append(
                "Book attractions and restaurants in advance. Consider visiting popular sites early morning or late evening."
            )
            if holidays:
                recommendations.append(
                    "Some attractions may be closed on holidays. Verify opening hours in advance."
                )
        elif risk == "medium":
            recommendations.append(
                "Moderate crowding expected. Book popular attractions in advance."
            )

        if events:
            recommendations.append(
                f"Major events happening: {', '.join([e['name'] for e in events[:2]])}. "
                "This could affect availability and prices."
            )

        return recommendations

    def calculate_trip_quality_score(
        self,
        budget_risk: Dict,
        weather_risk: Dict,
        crowding_risk: Dict,
        user_preferences: Dict,
    ) -> Dict[str, Any]:
        """
        Calculate overall trip quality score based on multiple factors
        Score from 0-100
        """
        # Component scores
        budget_score = self._score_budget(budget_risk)
        weather_score = self._score_weather(weather_risk)
        crowding_score = self._score_crowding(crowding_risk)

        # Weighted average (can be customized based on user preferences)
        weights = {
            "budget": 0.35,
            "weather": 0.35,
            "crowding": 0.30,
        }

        overall_score = (
            budget_score * weights["budget"]
            + weather_score * weights["weather"]
            + crowding_score * weights["crowding"]
        )

        # Determine comfort level
        if overall_score >= 80:
            comfort_level = "excellent"
        elif overall_score >= 65:
            comfort_level = "good"
        elif overall_score >= 50:
            comfort_level = "fair"
        else:
            comfort_level = "poor"

        return {
            "overall_score": round(overall_score, 1),
            "comfort_level": comfort_level,
            "component_scores": {
                "budget": round(budget_score, 1),
                "weather": round(weather_score, 1),
                "crowding": round(crowding_score, 1),
            },
            "recommendation": self._get_quality_recommendation(overall_score),
        }

    def _score_budget(self, budget_risk: Dict) -> float:
        """Score budget component (0-100)"""
        risk = budget_risk.get("overrun_risk", "low")
        ratio = budget_risk.get("budget_ratio", 1.0)

        if risk == "very low":
            return 95
        elif risk == "low":
            return 85
        elif risk == "medium":
            return 60
        else:  # high
            return max(30, 100 - (ratio - 1) * 100)

    def _score_weather(self, weather_risk: Dict) -> float:
        """Score weather component (0-100)"""
        risk = weather_risk.get("risk_level", "low")
        rain_percentage = weather_risk.get("rain_percentage", 0)

        if risk == "low":
            return 90
        elif risk == "medium":
            return 70 - (rain_percentage * 0.5)
        else:  # high
            return max(30, 70 - rain_percentage)

    def _score_crowding(self, crowding_risk: Dict) -> float:
        """Score crowding component (0-100)"""
        risk = crowding_risk.get("risk_level", "low")

        if risk == "low":
            return 90
        elif risk == "medium":
            return 65
        else:  # high
            return 45

    def _get_quality_recommendation(self, score: float) -> str:
        """Get recommendation based on quality score"""
        if score >= 80:
            return "This trip looks excellent! Conditions are favorable for a great experience."
        elif score >= 65:
            return "This trip looks good with minor considerations. Review the risk factors."
        elif score >= 50:
            return "This trip is feasible but has some concerns. Consider adjustments to improve experience."
        else:
            return "This trip has significant challenges. Consider rescheduling or major adjustments."

    def analyze_all_risks(
        self,
        budget: float,
        destination: str,
        start_date: datetime,
        end_date: datetime,
        interests: List[str],
        weather_data: Dict[str, Any],
        events: List[Dict[str, Any]],
        exchange_rate: float = 1.0,
        user_preferences: Dict = None,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive risk analysis
        """
        duration_days = (end_date - start_date).days + 1
        date_range = [
            (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
            for i in range(duration_days)
        ]

        # Analyze all risk factors
        budget_risk = self.analyze_budget_risk(
            budget, destination, duration_days, interests, exchange_rate
        )

        weather_risk = self.analyze_weather_risk(weather_data)

        crowding_risk = self.analyze_crowding_risk(events, destination, date_range)

        # Calculate quality score
        quality_score = self.calculate_trip_quality_score(
            budget_risk, weather_risk, crowding_risk, user_preferences or {}
        )

        return {
            "budget_risk": budget_risk,
            "weather_risk": weather_risk,
            "crowding_risk": crowding_risk,
            "quality_score": quality_score,
            "analysis_timestamp": datetime.utcnow().isoformat(),
        }
