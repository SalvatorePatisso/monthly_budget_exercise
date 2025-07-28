import types
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Inject a fake openai module so tests do not require the real package
fake_openai = types.SimpleNamespace()

class _ChatCompletion:
    @staticmethod
    def create(engine=None, messages=None, **kwargs):
        return types.SimpleNamespace(choices=[types.SimpleNamespace(message={"content": "hi"})])

fake_openai.ChatCompletion = _ChatCompletion
sys.modules['openai'] = fake_openai

from python.ai.azure_gpt import AzureGPT4O


def test_chat_completion_returns_string(monkeypatch):
    client = AzureGPT4O(endpoint="http://example.com", api_key="k", deployment="d")
    result = client.chat_completion([{"role": "user", "content": "hello"}])
    assert result == "hi"


def test_project_endpoint_fallback(monkeypatch):
    os.environ.pop("AZURE_OPENAI_ENDPOINT", None)
    os.environ["PROJECT_ENDPOINT"] = "http://example.com"
    client = AzureGPT4O(api_key="k", deployment="d")
    assert client.endpoint == "http://example.com"
