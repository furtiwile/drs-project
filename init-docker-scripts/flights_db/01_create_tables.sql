-- Database 2: Flight Management Database
-- Create custom types
CREATE TYPE flight_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED');

-- Airlines table
CREATE TABLE airlines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flights table
CREATE TABLE flights (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    airline_id INTEGER REFERENCES airlines(id) ON DELETE CASCADE,
    distance_km INTEGER NOT NULL,
    duration INTERVAL NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    departure_airport VARCHAR(100) NOT NULL,
    arrival_airport VARCHAR(100) NOT NULL,
    creator_id INTEGER NOT NULL, -- Reference to user id from users_db
    price DECIMAL(10,2) NOT NULL,
    status flight_status DEFAULT 'PENDING',
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL, -- Reference to user id from users_db
    flight_id INTEGER REFERENCES flights(id) ON DELETE CASCADE,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating SMALLINT CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes
CREATE INDEX idx_flights_airline_id ON flights(airline_id);
CREATE INDEX idx_flights_status ON flights(status);
CREATE INDEX idx_flights_departure_time ON flights(departure_time);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_flight_id ON bookings(flight_id);