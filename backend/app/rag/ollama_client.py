"""
Ollama Client: Handles interactions with local Ollama LLM
"""

import httpx
from typing import List, Dict, Any, Optional
import logging
from ..utils.config import settings

logger = logging.getLogger(__name__)


class OllamaClient:
    """Client for interacting with Ollama local LLM"""

    def __init__(self, base_url: str = None, model: str = None):
        """
        Initialize Ollama client

        Args:
            base_url: Ollama API base URL
            model: Model name to use
        """
        self.base_url = base_url or settings.OLLAMA_BASE_URL
        self.model = model or settings.OLLAMA_MODEL
        self.timeout = 120.0  # 2 minutes timeout for LLM requests

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate text completion from Ollama

        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated text
        """
        try:
            url = f"{self.base_url}/api/generate"

            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                }
            }

            if max_tokens:
                payload["options"]["num_predict"] = max_tokens

            if system_prompt:
                payload["system"] = system_prompt

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)

                if response.status_code != 200:
                    logger.error(f"Ollama API error: {response.status_code}")
                    return self._get_fallback_response(prompt)

                result = response.json()
                return result.get("response", "")

        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return self._get_fallback_response(prompt)
        except Exception as e:
            logger.error(f"Error calling Ollama: {e}")
            return self._get_fallback_response(prompt)

    async def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Chat completion from Ollama

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate

        Returns:
            Generated response
        """
        try:
            url = f"{self.base_url}/api/chat"

            payload = {
                "model": self.model,
                "messages": messages,
                "stream": False,
                "options": {
                    "temperature": temperature,
                }
            }

            if max_tokens:
                payload["options"]["num_predict"] = max_tokens

            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)

                if response.status_code != 200:
                    logger.error(f"Ollama API error: {response.status_code}")
                    return self._get_fallback_response("")

                result = response.json()
                return result.get("message", {}).get("content", "")

        except httpx.TimeoutException:
            logger.error("Ollama request timed out")
            return self._get_fallback_response("")
        except Exception as e:
            logger.error(f"Error calling Ollama chat: {e}")
            return self._get_fallback_response("")

    def _get_fallback_response(self, prompt: str) -> str:
        """
        Get a fallback response when Ollama is unavailable
        """
        return (
            "I'm having trouble connecting to the AI service. "
            "Please ensure Ollama is running locally with the command: "
            f"'ollama run {self.model}'"
        )

    async def check_health(self) -> bool:
        """
        Check if Ollama service is available

        Returns:
            True if service is healthy, False otherwise
        """
        try:
            url = f"{self.base_url}/api/tags"
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            return False
