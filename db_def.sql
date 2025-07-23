.open 
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER  PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS money_transfer (
    transaction_id INTEGER  PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description VARCHAR(255),
    category_id INTEGER,
    user_id INTEGER NOT NULL,
    incoming BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (category_id) REFERENCES categories(category_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE IF NOT EXISTS categories (
    category_id INTEGER  PRIMARY KEY AUTOINCREMENT,
    description VARCHAR(100) NOT NULL,
    name VARCHAR(50) NOT NULL
);