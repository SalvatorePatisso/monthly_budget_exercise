"""Utility class for interacting with Azure OpenAI GPT-4o."""

from __future__ import annotations
from dotenv import load_dotenv
import os
from typing import Iterable, Mapping


class AzureGPT4O:
    """Simple wrapper around the Azure OpenAI GPT-4o deployment."""

    def __init__(self, *, endpoint: str | None = None, api_key: str | None = None, api_version: str = "2024-05-01-preview"):
        load_dotenv()
        self.endpoint = endpoint or os.getenv("AZURE_API_ENDPOINT") or os.getenv("PROJECT_ENDPOINT")
        self.api_key = api_key or os.getenv("AZURE_API_KEY")
        self.api_version = os.getenv("AZURE_API_VERSION")
        if not all([self.endpoint, self.api_key]):
            raise ValueError("Endpoint, API key and deployment must be provided")

    def chat_completion(self, messages: Iterable[Mapping[str, str]], **kwargs) -> str:
        """Send chat messages to the model and return the response text."""
        try:
            import openai
        except ImportError as exc:
            raise ImportError("openai package is required to use AzureGPT4O") from exc

        openai.api_type = "azure"
        openai.api_base = self.endpoint
        openai.api_version = self.api_version
        openai.api_key = self.api_key
        print("Messages: ",messages)#TODO DEBUG
        response = openai.ChatCompletion.create(
            engine=self.deployment,
            messages=list(messages),
            **kwargs,
        )
        return response.choices[0].message["content"]
