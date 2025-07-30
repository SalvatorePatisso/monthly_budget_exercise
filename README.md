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

The project includes a helper class built on top of
[crewAI](https://github.com/joaomdmoura/crewai).  It now defines two
agents: one reads a document and extracts the expenses into JSON while the
second agent stores those expenses into the local SQLite database.  The
`CrewDocumentProcessor` will require the optional `crewai` package.

```python
from python.ai import CrewDocumentProcessor

processor = CrewDocumentProcessor()
expenses = processor.parse_file("receipt.txt")
print(expenses)
```
