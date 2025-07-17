# Functional Requirements

- [x] The system must allow user to insert a new transaction
- [x] The system must allow user to delete a transaction
- [x] The system must allow user to update a transaction
- [x] The system must allow user to view a transaction details
- [x] The system must allow the user to search for a transaction by date, amount, or description
- [x] The system must allow user to generate reports based on transactions
- [x] The system must allow user to insert transaction in bulk based on an execel file
- [x] The system shall allow user to create a new account and profile


# Actors
- User: A person who uses the system to manage their transactions.
- Transaction Database: The backend system that stores all transaction data.
- LLM (Large Language Model): An AI model that processes natural language queries and provides insights based on transaction data.

# Description of the world
The system is designed to help users manage their financial transactions efficiently. Users can perform various operations such as inserting, deleting, updating, and viewing transactions. They can also search for specific transactions and generate reports. The system supports bulk transaction insertion from Excel files and allows users to create new accounts and profiles. The LLM enhances user experience by providing natural language processing capabilities for querying transaction data. 
Considering this context, i choose to use a sqlite database to store the transaction data. SQLite is lightweight, easy to set up, and suitable for applications that require a simple database solution without the overhead of a full-fledged database server. It will allow for efficient storage and retrieval of transaction records while being easy to integrate with the application.
