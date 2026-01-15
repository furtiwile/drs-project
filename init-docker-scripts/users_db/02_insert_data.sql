-- Seed data for Database 1
-- Insert default administrator
INSERT INTO users (first_name, last_name, email, password, birth_date, gender, country, city, street, house_number, account_balance, role)
VALUES (
    'Admin',
    'User',
    'admin@example.com',
    'scrypt:32768:8:1$jGfnzKn6v7rQ7xvn$76c6f8b163fd4c7c74d84c399ac6d72495d3d7e73e1204325b0366db8ba972703cea221e009c4c25f17739a119d1f5169192621339a31ab8c1bdba14db1a1121', -- password: password (scrypt hash)
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
    ('John', 'Doe', 'john@example.com', 'scrypt:32768:8:1$jGfnzKn6v7rQ7xvn$76c6f8b163fd4c7c74d84c399ac6d72495d3d7e73e1204325b0366db8ba972703cea221e009c4c25f17739a119d1f5169192621339a31ab8c1bdba14db1a1121', '1985-05-15', 'MALE', 'USA', 'Washington', 'Elm Street', 123, 500.00, 'USER'),
    ('Jane', 'Smith', 'jane@example.com', 'scrypt:32768:8:1$jGfnzKn6v7rQ7xvn$76c6f8b163fd4c7c74d84c399ac6d72495d3d7e73e1204325b0366db8ba972703cea221e009c4c25f17739a119d1f5169192621339a31ab8c1bdba14db1a1121', '1992-08-20', 'FEMALE', 'UK', 'Manchester', 'Oak Avenue', 456, 750.00, 'MANAGER');