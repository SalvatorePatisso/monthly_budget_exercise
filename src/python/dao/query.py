#TESTED

TRANSFER_FOR_DATE= "SELECT * FROM money_transfer WHERE date = ?"

TRANSFER_FOR_MAX_AMOUNT = "SELECT * FROM money_transfer WHERE amount <= ?"

TRANSFER_FOR_MIN_AMOUNT = "SELECT * FROM money_transfer WHERE amount >= ?"

TRANSFER_FROM_TIME_INTERVAL = "SELECT * FROM money_transfer WHERE date BETWEEN ? AND ?"

TRANSFER_FROM_IMPORT_SELECTION = "SELECT * FROM money_transfer WHERE incoming = ?"

TRANSFER_FROM_DUE_DATE = "SELECT * FROM money_transfer WHERE date = ?"

TRANSFER_FOR_AMOUNT_IN_RANGE = "SELECT * FROM money_transfer WHERE amount <= ? AND amount >= ?"


