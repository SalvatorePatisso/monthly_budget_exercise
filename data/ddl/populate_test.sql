-- This SQL script is intended for populating test data into the wallet_tracker database.
-- Add your INSERT statements below to create sample data for testing purposes.

INSERT INTO users (user_id, username, email, password) VALUES
(1, 'alice', 'alice@example.com', 'password123'),
(2, 'bob', 'bob@example.com', 'securepass'),
(3, 'charlie', 'charlie@example.com', 'charliepwd');


INSERT INTO categories (category_id, description, name) VALUES
(1, 'Groceries', 'Food'),
(2, 'Utilities', 'Bills'),
(3, 'Entertainment', 'Leisure');-- ...existing code...

INSERT INTO users (user_id, username, email, password) VALUES
(4, 'diana', 'diana@example.com', 'dianapass'),
(5, 'edward', 'edward@example.com', 'edwardpwd');

INSERT INTO categories (category_id, description, name) VALUES
(4, 'Transport', 'Travel'),
(5, 'Health', 'Medical');

INSERT INTO money_transfer (transaction_id, date, amount, description, category_id, user_id) VALUES
(4, '2023-02-01', 20.00, 'Bus ticket', 4, 1),
(5, '2023-02-05', 75.00, 'Doctor visit', 5, 2),
(6, '2023-02-10', 120.00, 'Concert tickets', 3, 4),
(7, '2023-02-15', 60.00, 'Supermarket', 1, 5),
(8, '2023-02-20', 90.00, 'Water bill', 2, 3),
(9, '2023-02-25', 45.00, 'Pharmacy', 5, 4),
(10, '2023-03-01', 15.00, 'Taxi ride', 4,-- ...existing code...

-- Altri 5 utenti
INSERT INTO users (user_id, username, email, password) VALUES
(6, 'frank', 'frank@example.com', 'frankpass'),
(7, 'gina', 'gina@example.com', 'ginapwd'),
(8, 'hugo', 'hugo@example.com', 'hugopass'),
(9, 'irene', 'irene@example.com', 'irenepwd'),
(10, 'jack', 'jack@example.com', 'jackpass');

-- Altre 5 categorie
INSERT INTO categories (category_id, description, name) VALUES
(6, 'Education', 'School'),
(7, 'Savings', 'Deposit'),
(8, 'Dining', 'Restaurant'),
(9, 'Gifts', 'Present'),
(10, 'Insurance', 'Protection');

-- Altri 5 trasferimenti di denaro
INSERT INTO money_transfer (transaction_id, date, amount, description, category_id, user_id) VALUES
(11, '2023-03-05', 200.00, 'Tuition fee', 6, 6),
(12, '2023-03-10', 300.00, 'Savings deposit', 7, 7),
(13, '2023-03-15', 40.00, 'Dinner out', 8, 8),
(14, '2023-03-20', 60.00, 'Birthday gift', 9, 9),
(15, '2023-03-25', 120.00, 'Health insurance', 10, 10);

-- ...existing

INSERT INTO money_transfer (transaction_id, date, amount, description, category_id, user_id) VALUES
(1, '2023-01-15', 50.00, 'Grocery shopping', 1, 1),
(2, '2023-01-20', 100.00, 'Electricity bill', 2, 2),
(3, '2023-01-25', 30.00, 'Movie night', 3, 3);

