-- Seed data for Database 2
-- Insert sample airlines
INSERT INTO airlines (name) VALUES
    ('Air Serbia'),
    ('Lufthansa'),
    ('Ryanair'),
    ('Turkish Airlines');

-- Insert sample flights (assuming creator_id 3 is the manager from db1)
INSERT INTO flights (name, airline_id, distance_km, duration, departure_time, departure_airport, arrival_airport, creator_id, price, status)
VALUES
    ('Flight 101', 1, 500, '1 hour', '2025-12-20 10:00:00', 'Belgrade', 'Paris', 3, 150.00, 'APPROVED'),
    ('Flight 202', 2, 800, '1 hour 30 minutes', '2025-12-21 14:00:00', 'Frankfurt', 'London', 3, 200.00, 'APPROVED'),
    ('Flight 303', 3, 1200, '2 hours', '2025-12-22 16:00:00', 'Dublin', 'Barcelona', 3, 100.00, 'PENDING'),
    ('Flight 404', 4, 600, '1 hour 15 minutes', '2025-12-23 12:00:00', 'Istanbul', 'Rome', 3, 180.00, 'APPROVED');

-- Insert sample bookings (assuming user_id 2 from db1)
INSERT INTO bookings (user_id, flight_id, purchased_at, rating)
VALUES
    (2, 1, '2025-12-18 09:00:00', 4),
    (2, 2, '2025-12-19 11:00:00', NULL); -- No rating yet