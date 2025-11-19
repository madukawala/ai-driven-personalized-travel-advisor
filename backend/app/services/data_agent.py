"""
Data Agent: Fetches real-time information from external APIs
- Weather data from OpenWeatherMap
- Events data from Eventbrite
- Currency exchange rates
- Travel safety information (mocked)
"""

import httpx
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from ..utils.config import settings
import logging

logger = logging.getLogger(__name__)


class DataAgent:
    """Agent responsible for fetching real-time travel data"""

    def __init__(self):
        self.openweather_api_key = settings.OPENWEATHER_API_KEY
        self.eventbrite_api_key = settings.EVENTBRITE_API_KEY
        self.exchangerate_api_key = settings.EXCHANGERATE_API_KEY

    async def fetch_weather_data(
        self, location: str, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """
        Fetch weather forecast for a location and date range
        Uses OpenWeatherMap API
        """
        try:
            # For demo purposes, if no API key, return mock data
            if not self.openweather_api_key or self.openweather_api_key == "your_openweather_api_key_here":
                logger.warning("Using mock weather data - no API key configured")
                return self._generate_mock_weather(location, start_date, end_date)

            async with httpx.AsyncClient() as client:
                # Get coordinates for location
                geo_url = f"http://api.openweathermap.org/geo/1.0/direct"
                geo_params = {"q": location, "limit": 1, "appid": self.openweather_api_key}

                geo_response = await client.get(geo_url, params=geo_params, timeout=10.0)

                if geo_response.status_code != 200 or not geo_response.json():
                    logger.warning(f"Could not fetch coordinates for {location}, using mock data")
                    return self._generate_mock_weather(location, start_date, end_date)

                geo_data = geo_response.json()[0]
                lat, lon = geo_data["lat"], geo_data["lon"]

                # Fetch 5-day forecast
                weather_url = "http://api.openweathermap.org/data/2.5/forecast"
                weather_params = {
                    "lat": lat,
                    "lon": lon,
                    "appid": self.openweather_api_key,
                    "units": "metric",
                }

                weather_response = await client.get(
                    weather_url, params=weather_params, timeout=10.0
                )

                if weather_response.status_code != 200:
                    logger.warning(f"Weather API error: {weather_response.status_code}")
                    return self._generate_mock_weather(location, start_date, end_date)

                weather_data = weather_response.json()
                return self._process_weather_data(weather_data, start_date, end_date)

        except Exception as e:
            logger.error(f"Error fetching weather data: {e}")
            return self._generate_mock_weather(location, start_date, end_date)

    def _generate_mock_weather(
        self, location: str, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Generate mock weather data for testing"""
        import random

        days = (end_date - start_date).days + 1
        forecast = []

        conditions = ["Clear", "Partly Cloudy", "Cloudy", "Rainy", "Sunny"]

        for i in range(days):
            day = start_date + timedelta(days=i)
            forecast.append({
                "date": day.strftime("%Y-%m-%d"),
                "condition": random.choice(conditions),
                "temperature_high": random.randint(20, 32),
                "temperature_low": random.randint(15, 22),
                "precipitation_chance": random.randint(0, 80),
                "humidity": random.randint(40, 80),
                "wind_speed": random.randint(5, 25),
            })

        return {
            "location": location,
            "forecast": forecast,
            "source": "mock_data",
        }

    def _process_weather_data(
        self, weather_data: Dict, start_date: datetime, end_date: datetime
    ) -> Dict[str, Any]:
        """Process OpenWeatherMap API response"""
        forecast_list = weather_data.get("list", [])
        daily_forecast = {}

        for item in forecast_list:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")

            if date_key not in daily_forecast:
                daily_forecast[date_key] = {
                    "date": date_key,
                    "temps": [],
                    "conditions": [],
                    "precipitation": [],
                    "humidity": [],
                    "wind_speed": [],
                }

            daily_forecast[date_key]["temps"].append(item["main"]["temp"])
            daily_forecast[date_key]["conditions"].append(item["weather"][0]["main"])
            daily_forecast[date_key]["humidity"].append(item["main"]["humidity"])
            daily_forecast[date_key]["wind_speed"].append(item["wind"]["speed"])

            if "rain" in item:
                daily_forecast[date_key]["precipitation"].append(
                    item["rain"].get("3h", 0)
                )
            else:
                daily_forecast[date_key]["precipitation"].append(0)

        # Aggregate daily data
        processed_forecast = []
        for date_key, data in sorted(daily_forecast.items()):
            processed_forecast.append({
                "date": date_key,
                "condition": max(set(data["conditions"]), key=data["conditions"].count),
                "temperature_high": max(data["temps"]),
                "temperature_low": min(data["temps"]),
                "precipitation_chance": int(
                    (sum(1 for p in data["precipitation"] if p > 0) / len(data["precipitation"]))
                    * 100
                ),
                "humidity": int(sum(data["humidity"]) / len(data["humidity"])),
                "wind_speed": sum(data["wind_speed"]) / len(data["wind_speed"]),
            })

        return {
            "location": weather_data.get("city", {}).get("name", "Unknown"),
            "forecast": processed_forecast[:7],  # Limit to 7 days
            "source": "openweathermap",
        }

    async def fetch_local_events(
        self, location: str, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """
        Fetch local events for a location and date range
        Uses Eventbrite API or mock data
        """
        try:
            # For demo purposes, return mock data
            if not self.eventbrite_api_key or self.eventbrite_api_key == "your_eventbrite_api_key_here":
                logger.warning("Using mock events data - no API key configured")
                return self._generate_mock_events(location, start_date, end_date)

            # Eventbrite API implementation would go here
            # For now, return mock data
            return self._generate_mock_events(location, start_date, end_date)

        except Exception as e:
            logger.error(f"Error fetching events: {e}")
            return self._generate_mock_events(location, start_date, end_date)

    def _generate_mock_events(
        self, location: str, start_date: datetime, end_date: datetime
    ) -> List[Dict[str, Any]]:
        """Generate mock events data"""
        import random

        event_types = ["Concert", "Festival", "Exhibition", "Workshop", "Conference", "Sports"]
        events = []

        num_events = random.randint(3, 8)
        for i in range(num_events):
            event_date = start_date + timedelta(
                days=random.randint(0, (end_date - start_date).days)
            )
            events.append({
                "id": f"event_{i+1}",
                "name": f"{random.choice(event_types)} in {location}",
                "date": event_date.strftime("%Y-%m-%d"),
                "time": f"{random.randint(10, 20)}:00",
                "category": random.choice(event_types).lower(),
                "estimated_cost": random.choice([0, 10, 25, 50, 100]),
                "popularity": random.choice(["low", "medium", "high"]),
                "description": f"A wonderful {random.choice(event_types).lower()} event happening in {location}",
            })

        return sorted(events, key=lambda x: x["date"])

    async def fetch_exchange_rate(
        self, from_currency: str, to_currency: str
    ) -> Dict[str, Any]:
        """
        Fetch currency exchange rate
        """
        try:
            if not self.exchangerate_api_key or self.exchangerate_api_key == "your_exchangerate_api_key_here":
                logger.warning("Using mock exchange rate - no API key configured")
                return self._generate_mock_exchange_rate(from_currency, to_currency)

            async with httpx.AsyncClient() as client:
                url = f"https://v6.exchangerate-api.com/v6/{self.exchangerate_api_key}/pair/{from_currency}/{to_currency}"
                response = await client.get(url, timeout=10.0)

                if response.status_code != 200:
                    return self._generate_mock_exchange_rate(from_currency, to_currency)

                data = response.json()
                return {
                    "from_currency": from_currency,
                    "to_currency": to_currency,
                    "rate": data.get("conversion_rate", 1.0),
                    "last_updated": data.get("time_last_update_utc", ""),
                    "source": "exchangerate-api",
                }

        except Exception as e:
            logger.error(f"Error fetching exchange rate: {e}")
            return self._generate_mock_exchange_rate(from_currency, to_currency)

    def _generate_mock_exchange_rate(
        self, from_currency: str, to_currency: str
    ) -> Dict[str, Any]:
        """Generate mock exchange rate"""
        # Common exchange rates (approximate)
        rates = {
            ("USD", "EUR"): 0.92,
            ("USD", "GBP"): 0.79,
            ("USD", "JPY"): 149.5,
            ("EUR", "USD"): 1.09,
            ("GBP", "USD"): 1.27,
        }

        rate = rates.get((from_currency, to_currency), 1.0)

        return {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "rate": rate,
            "last_updated": datetime.utcnow().isoformat(),
            "source": "mock_data",
        }

    async def fetch_safety_info(self, location: str) -> Dict[str, Any]:
        """
        Fetch travel safety information for a location
        Uses mock data since TravelBriefing API is archived
        """
        return self._generate_mock_safety_info(location)

    def _generate_mock_safety_info(self, location: str) -> Dict[str, Any]:
        """Generate mock safety information"""
        import random

        risk_levels = ["low", "moderate", "medium", "high"]
        risk_level = random.choice(risk_levels[:3])  # Avoid high for demo

        return {
            "location": location,
            "overall_risk": risk_level,
            "safety_score": random.randint(60, 95),
            "advisories": [
                "Check local COVID-19 regulations",
                "Be aware of pickpockets in tourist areas",
                "Emergency number: varies by country",
            ],
            "health_warnings": ["Routine vaccinations recommended"],
            "last_updated": datetime.utcnow().strftime("%Y-%m-%d"),
            "source": "mock_data",
        }

    async def fetch_all_data(
        self, location: str, start_date: datetime, end_date: datetime, currency: str = "USD"
    ) -> Dict[str, Any]:
        """
        Fetch all relevant data for a trip in parallel
        """
        # Fetch all data concurrently
        weather_task = self.fetch_weather_data(location, start_date, end_date)
        events_task = self.fetch_local_events(location, start_date, end_date)
        safety_task = self.fetch_safety_info(location)
        exchange_task = self.fetch_exchange_rate("USD", currency) if currency != "USD" else None

        results = await asyncio.gather(
            weather_task,
            events_task,
            safety_task,
            exchange_task if exchange_task else asyncio.sleep(0),
            return_exceptions=True,
        )

        return {
            "weather": results[0] if not isinstance(results[0], Exception) else {},
            "events": results[1] if not isinstance(results[1], Exception) else [],
            "safety": results[2] if not isinstance(results[2], Exception) else {},
            "exchange_rate": results[3] if exchange_task and not isinstance(results[3], Exception) else None,
            "fetched_at": datetime.utcnow().isoformat(),
        }
