-- Database 1: User Management Database
-- Create custom types
CREATE TYPE user_role AS ENUM ('USER', 'MANAGER', 'ADMINISTRATOR');
CREATE TYPE gender_type AS ENUM ('MALE', 'FEMALE', 'OTHER');

-- Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    birth_date DATE NOT NULL,
    gender gender_type NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50) NOT NULL,
    street VARCHAR(50) NOT NULL,
    house_number INTEGER NOT NULL,
    account_balance DECIMAL(10,2) DEFAULT 0.00,
    role user_role DEFAULT 'USER',
    profile_picture TEXT
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);