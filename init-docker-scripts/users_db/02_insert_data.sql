-- Seed data for Database 1
-- Insert default administrator
INSERT INTO users (first_name, last_name, email, password, birth_date, gender, country, city, street, house_number, account_balance, role)
VALUES (
    'Admin',
    'User',
    'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMhE6Xc.', -- password: admin123 (bcrypt hash)
    '1990-01-01',
    'MALE',
    'Serbia',
    'Belgrade',
    'Main Street',
    1,
    1000.00,
    'ADMINISTRATOR'
);

-- Insert sample users
INSERT INTO users (first_name, last_name, email, password, birth_date, gender, country, city, street, house_number, account_balance, role)
VALUES
    ('John', 'Doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMhE6Xc.', '1985-05-15', 'MALE', 'USA', 'Washington', 'Elm Street', 123, 500.00, 'USER'),
    ('Jane', 'Smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6fMhE6Xc.', '1992-08-20', 'FEMALE', 'UK', 'Manchester', 'Oak Avenue', 456, 750.00, 'MANAGER');