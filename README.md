# monthly_budget_exercise
Personal monthly budget software developed in python as exercise

## Azure OpenAI integration

This project now includes a small wrapper around Azure OpenAI's GPT-4o model. Configure the following environment variables or pass them explicitly to use it:

- `AZURE_OPENAI_ENDPOINT` – your Azure OpenAI endpoint (falls back to `PROJECT_ENDPOINT`)
- `AZURE_OPENAI_KEY` – the API key
- `AZURE_OPENAI_DEPLOYMENT` – the name of the GPT‑4o deployment

Example usage:

```python
from python.ai.azure_gpt import AzureGPT4O
client = AzureGPT4O()
response = client.chat_completion([{"role": "user", "content": "Hello"}])
print(response)
```
