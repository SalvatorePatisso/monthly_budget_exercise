# monthly_budget_exercise
Personal monthly budget software developed in python as exercise

## Azure OpenAI integration

This project now includes a small wrapper around Azure OpenAI's GPT-4o model. Configure the following environment variables or pass them explicitly to use it:

- `AZURE_OPENAI_ENDPOINT` – your Azure OpenAI endpoint (falls back to `PROJECT_ENDPOINT`)
- `AZURE_OPENAI_KEY` – the API key
- `AZURE_OPENAI_DEPLOYMENT` – the name of the GPT‑4o deployment

Example usage:

```python
from python.ai import AzureGPT4O
client = AzureGPT4O()
response = client.chat_completion([{"role": "user", "content": "Hello"}])
print(response)
```

## crewAI document analysis

A helper class is provided to process receipts or invoices using the
[crewAI](https://github.com/joaomdmoura/crewai) agent framework. It creates
an agent capable of extracting expenses from a piece of text.
The `CrewDocumentProcessor` will require the optional `crewai` package.

```python
from python.ai import CrewDocumentProcessor

processor = CrewDocumentProcessor()
expenses = processor.parse_text("""Receipt\n1/1/2024 Coffee 2.50 EUR""")
print(expenses)
```
