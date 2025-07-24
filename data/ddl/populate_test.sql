-- This SQL script is intended for populating test data into the wallet_tracker database.
-- Add your INSERT statements below to create sample data for testing purposes.

INSERT INTO users (user_id, username, email, password) VALUES
(1, 'alice', 'alice@example.com', 'password123'),
(2, 'bob', 'bob@example.com', 'securepass'),
(3, 'charlie', 'charlie@example.com', 'charliepwd');


INSERT INTO categories (category_id, description, name) VALUES
(1, 'Groceries', 'Food'),
(2, 'Utilities', 'Bills'),
(3, 'Entertainment', 'Leisure');

INSERT INTO money_transfer (transaction_id, date, amount, description, category_id, user_id) VALUES
(1, '2023-01-15', 50.00, 'Grocery shopping', 1, 1),
(2, '2023-01-20', 100.00, 'Electricity bill', 2, 2),
(3, '2023-01-25', 30.00, 'Movie night', 3, 3);

