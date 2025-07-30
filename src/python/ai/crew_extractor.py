"""Utility integration with crewAI for expense extraction."""

from __future__ import annotations

from typing import Iterable, Mapping, List


class CrewDocumentProcessor:
    """Use crewAI agents to extract expenses from document text."""

    def __init__(self, crew: object | None = None) -> None:
        """Initialize the processor with an optional pre-configured crew."""
        try:
            from crewai import Agent, Crew, Task
        except ImportError as exc:
            raise ImportError(
                "crewai package is required to use CrewDocumentProcessor"
            ) from exc

        if crew is not None:
            self.crew = crew
            return

        expert = Agent(
            role="expense extraction expert",
            goal="extract each expense from the given document",
            backstory=(
                "You carefully read receipts and invoices to identify all"
                " expenses with date, description and amount."
            ),
        )

        task = Task(
            description="Identify all expenses in the document text.",
            expected_output=(
                "A JSON array of objects each containing date, description,"
                " and amount fields"
            ),
        )

        self.crew = Crew(agents=[expert], tasks=[task])

    def parse_text(self, text: str) -> List[Mapping[str, str]]:
        """Run the crew on ``text`` and return parsed expenses."""
        result = self.crew.kickoff({"text": text})
        if isinstance(result, str):
            import json
            return json.loads(result)
        return result
