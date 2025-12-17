-- Database 2: Flight Management Database
-- Create custom types
CREATE TYPE flight_status AS ENUM ('PENDING', 'APPROVED', 'REJECTED', 'CANCELLED', 'COMPLETED');

-- Airports table
CREATE TABLE airports (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(10) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Airlines table
CREATE TABLE airlines (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Flights table
CREATE TABLE flights (
    flight_id SERIAL PRIMARY KEY,
    flight_name VARCHAR(255) NOT NULL,
    airline_id INTEGER REFERENCES airlines(id) ON DELETE CASCADE,
    flight_distance_km INTEGER NOT NULL,
    flight_duration INTERVAL NOT NULL,
    departure_time TIMESTAMP NOT NULL,
    arrival_time TIMESTAMP NOT NULL,
    departure_airport_id INTEGER REFERENCES airports(id) ON DELETE CASCADE,
    arrival_airport_id INTEGER REFERENCES airports(id) ON DELETE CASCADE,
    created_by INTEGER NOT NULL, -- Reference to user id from users_db
    price DECIMAL(10,2) NOT NULL,
    total_seats INTEGER NOT NULL,
    status flight_status DEFAULT 'PENDING',
    rejection_reason TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bookings table
CREATE TABLE bookings (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL, -- Reference to user id from users_db
    flight_id INTEGER REFERENCES flights(flight_id) ON DELETE CASCADE,
    purchased_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    rating SMALLINT CHECK (rating >= 1 AND rating <= 5)
);

-- Indexes
CREATE INDEX idx_flights_airline_id ON flights(airline_id);
CREATE INDEX idx_flights_status ON flights(status);
CREATE INDEX idx_flights_departure_time ON flights(departure_time);
CREATE INDEX idx_bookings_user_id ON bookings(user_id);
CREATE INDEX idx_bookings_flight_id ON bookings(flight_id);