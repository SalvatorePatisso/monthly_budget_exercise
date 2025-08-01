"""Utility integration with crewAI for expense extraction."""

from __future__ import annotations

from typing import Iterable, Mapping, List
import json
import os

from ..dao.money_transfer_dao import MoneyTransferDAO
from ..dao.db_connection import ConnectionDB


class CrewDocumentProcessor:
    """Use crewAI agents to extract expenses from document text."""

    def __init__(self, crew: object | None = None, db_path: str | None = None) -> None:
        """Initialize the processor with an optional pre-configured crew and database."""
        try:
            from crewai import Agent, Crew, Task
        except ImportError as exc:
            raise ImportError(
                "crewai package is required to use CrewDocumentProcessor"
            ) from exc

        if crew is not None:
            self.crew = crewsd
            return

        self.db_path = db_path or os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "data",
            "ddl",
            "debug.db",
        )
        self.db_connection = ConnectionDB(db_path=self.db_path)

        def read_file(path: str) -> str:
            """Tool to read a file and return its contents."""
            with open(path, "r", encoding="utf-8") as fh:
                return fh.read()

       
            return rows

        extractor = Agent(
            role="expense extraction expert",
            goal="extract each expense from the given document",
            backstory=(
                "You carefully read receipts and invoices to identify all"
                " expenses with date, description and amount."
            ),
            tools=[read_file],
        )

        db_agent = Agent(
            role="database agent",
            goal="store the extracted expenses into the SQLite database",
            backstory="You can execute queries on the local database.",
            tools=[insert_expenses],
        )

        extract_task = Task(
            description="Identify all expenses in the document text using the file reader tool.",
            expected_output=(
                "A JSON array of objects each containing date, description,"
                " and amount fields"
            ),
            agent=extractor,
        )

        insert_task = Task(
            description="Insert the extracted expenses into the database using the provided tool.",
            expected_output="Number of rows inserted",
            agent=db_agent,
            context=[extract_task],
        )

        self.crew = Crew(agents=[extractor, db_agent], tasks=[extract_task, insert_task])
   
    def insert_expense_from_json(expenses_json: str) -> int:
            """Tool to insert expenses into the database."""
            expenses = json.loads(expenses_json)
            dao = MoneyTransferDAO(db_path=self.db_path)
            rows = 0
            for exp in expenses:
                rows += dao.create_transfer(
                    exp.get("date"),
                    float(exp.get("amount")),
                    exp.get("category_id"),
                    exp.get("user_id"),
                    exp.get("description"),
                    exp.get("incoming")
                )

    def parse_file(self, file_path: str) -> List[Mapping[str, str]]:
        """Run the crew on ``file_path`` and return parsed expenses."""
        result = self.crew.kickoff({"file_path": file_path})
        if isinstance(result, str):
            return json.loads(result)
        return result
