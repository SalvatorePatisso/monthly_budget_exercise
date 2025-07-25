from enum import Enum

class MoneyTransferAttribute(Enum):
    START_AMOUNT = "start_amount"
    END_AMOUNT = "end_amount"
    MONEY_TRANSFER_START_DATE = "start_date"
    MONEY_TRANSFER_END_DATE = "end_date"
    MONEY_TRANSFER_AMOUNT = "amount"
    CATEGORY_ID = "category_id"
    DESCRIPTION = "description"
    TRANSACTION_ID = "transaction_id"
    INCOMING = "incoming"
 

class QueryBuilder: 

    # TRANSFER_FOR_DATE= "SELECT * FROM money_transfer WHERE date = ?"

    # TRANSFER_FOR_MAX_AMOUNT = "SELECT * FROM money_transfer WHERE amount <= ?"

    # TRANSFER_FOR_MIN_AMOUNT = "SELECT * FROM money_transfer WHERE amount >= ?"

    # TRANSFER_FROM_TIME_INTERVAL = "SELECT * FROM money_transfer WHERE date BETWEEN ? AND ?"

    # TRANSFER_FROM_IMPORT_SELECTION = "SELECT * FROM money_transfer WHERE incoming = ?"

    # TRANSFER_FROM_DUE_DATE = "SELECT * FROM money_transfer WHERE date = ?"

    # TRANSFER_FOR_AMOUNT_IN_RANGE = "SELECT * FROM money_transfer WHERE amount <= ? AND amount >= ?"

    # TRANSFER_FOR_CATEGORY = "SELECT * FROM money_transfer WHERE category_id = ?"

    # TRANSFER_FOR_DESCRIPTION = "SELECT * FROM money_transfer WHERE description LIKE ?"  # ? Must be a regex
    # #TO TEST
    # TRANSFER_FOR_DATE_AND_CATEGORY = "SELECT * FROM money_transfer WHERE date = ? AND category_id = ?"

    # TRANSFER_FOR_ID = "SELECT * FROM money_transfer WHERE transaction_id = ?"

    def insert_amount_range(self, attributes):
    # Check if the attributes contain amount range conditions
        if (MoneyTransferAttribute.START_AMOUNT in attributes) and (MoneyTransferAttribute.END_AMOUNT in attributes):
        
            #query must be BETWEEN
            self.query += " AND amount BETWEEN ? AND ?"

            attributes.remove(MoneyTransferAttribute.START_AMOUNT)
            attributes.remove(MoneyTransferAttribute.END_AMOUNT)

        elif MoneyTransferAttribute.START_AMOUNT in attributes:

            self.query += " AND amount >= ?"
            attributes.remove(MoneyTransferAttribute.START_AMOUNT)

        elif MoneyTransferAttribute.END_AMOUNT in attributes:

            self.query += " AND amount <= ?"
            attributes.remove(MoneyTransferAttribute.END_AMOUNT)

    def insert_date_range(self, attributes):
    # Check if the attributes contain date range conditions
        if (MoneyTransferAttribute.MONEY_TRANSFER_START_DATE in attributes) and (MoneyTransferAttribute.MONEY_TRANSFER_END_DATE in attributes):
        
            #query must be BETWEEN
            self.query += " date BETWEEN ? AND ?"

            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_START_DATE)
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_END_DATE)

        elif MoneyTransferAttribute.MONEY_TRANSFER_START_DATE in attributes:

            self.query += " date >= ?"
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_START_DATE)

        elif MoneyTransferAttribute.MONEY_TRANSFER_END_DATE in attributes:

            self.query += " date <= ?"
            attributes.remove(MoneyTransferAttribute.MONEY_TRANSFER_END_DATE)

    def __init__(self, attributes):
        """
        Initialize the QueryBuilder with the given parameters.
        :param params: A dictionary of parameters to be used in the queries.
        """
        self.params_accepted =  [attr for attr in MoneyTransferAttribute]
    
        for attr in attributes:
            if attr not in self.params_accepted:
                raise ValueError(f"Invalid attribute: {attr}. Accepted attributes are: {self.params_accepted}")
        self.attributes = attributes
        self.query = "SELECT * FROM money_transfer WHERE"
        
        self.insert_date_range(attributes=self.attributes)
        self.insert_amount_range(attributes=self.attributes)

        if MoneyTransferAttribute.DESCRIPTION in attributes:
            self.query += " AND description LIKE ?"
            attributes.remove(MoneyTransferAttribute.DESCRIPTION)
    
        # Add the remaining attributes to the query
        for attr in attributes: 
            #do not put OR in the beginning
            if self.query.endswith("WHERE"):
                self.query += f" {attr.value} = ?"
            else:
                self.query += f" AND {attr.value} = ?"



if __name__== "__main__":
    list = [MoneyTransferAttribute.MONEY_TRANSFER_START_DATE, 
            MoneyTransferAttribute.MONEY_TRANSFER_END_DATE,
            MoneyTransferAttribute.CATEGORY_ID,
            MoneyTransferAttribute.START_AMOUNT,
            MoneyTransferAttribute.END_AMOUNT]
    query_builder = QueryBuilder(list)
    print(query_builder.query)