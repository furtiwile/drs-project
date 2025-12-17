-- Seed data for Database 2
-- Insert sample airports
INSERT INTO airports (name, code) VALUES
    ('Belgrade Nikola Tesla Airport', 'BEG'),
    ('Paris Charles de Gaulle Airport', 'CDG'),
    ('Frankfurt Airport', 'FRA'),
    ('London Heathrow Airport', 'LHR'),
    ('Dublin Airport', 'DUB'),
    ('Barcelona El Prat Airport', 'BCN'),
    ('Istanbul Airport', 'IST'),
    ('Rome Fiumicino Airport', 'FCO');

-- Insert sample airlines
INSERT INTO airlines (name) VALUES
    ('Air Serbia'),
    ('Lufthansa'),
    ('Ryanair'),
    ('Turkish Airlines');

-- Insert sample flights (assuming created_by 3 is the manager from db1)
INSERT INTO flights (flight_name, airline_id, flight_distance_km, flight_duration, departure_time, arrival_time, departure_airport_id, arrival_airport_id, created_by, price, total_seats, status)
VALUES
    ('Flight 101', 1, 500, '1 hour', '2025-12-20 10:00:00', '2025-12-20 11:00:00', 1, 2, 3, 150.00, 100, 'APPROVED'),
    ('Flight 202', 2, 800, '1 hour 30 minutes', '2025-12-21 14:00:00', '2025-12-21 15:30:00', 3, 4, 3, 200.00, 150, 'APPROVED'),
    ('Flight 303', 3, 1200, '2 hours', '2025-12-22 16:00:00', '2025-12-22 18:00:00', 5, 6, 3, 100.00, 200, 'PENDING'),
    ('Flight 404', 4, 600, '1 hour 15 minutes', '2025-12-23 12:00:00', '2025-12-23 13:15:00', 7, 8, 3, 180.00, 120, 'APPROVED');

-- Insert sample bookings (assuming user_id 2 from db1)
INSERT INTO bookings (user_id, flight_id, purchased_at, rating)
VALUES
    (2, 1, '2025-12-18 09:00:00', 4),
    (2, 2, '2025-12-19 11:00:00', NULL); -- No rating yet