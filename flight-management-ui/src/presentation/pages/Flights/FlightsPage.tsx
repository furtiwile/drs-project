import React, { useState, useEffect } from 'react';
import type { Flight } from '../../../domain/models/Flight';
import type { Airline } from '../../../domain/models/Airline';
import type { Airport } from '../../../domain/models/Airport';
import { FlightStatus } from '../../../domain/enums/FlightStatus';
import { flightService } from '../../../infrastructure/services/flightService';
import { airlineService } from '../../../infrastructure/services/airlineService';
import { airportService } from '../../../infrastructure/services/airportService';
import { bookingService } from '../../../infrastructure/services/bookingService';
import { useToast } from '../../../application/context/ToastContext';
import { useAuth } from '../../../application/context/AuthContext';
import './FlightsPage.css';

export const FlightsPage: React.FC = () => {
  const [flights, setFlights] = useState<Flight[]>([]);
  const [airlines, setAirlines] = useState<Airline[]>([]);
  const [airports, setAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);

  // Filters
  const [selectedAirline, setSelectedAirline] = useState<number>(0);
  const [departureAirport, setDepartureAirport] = useState<number>(0);
  const [arrivalAirport, setArrivalAirport] = useState<number>(0);
  const [departureDate, setDepartureDate] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<number>(0);
  const [bookingLoading, setBookingLoading] = useState<number | null>(null);

  const toast = useToast();
  const { user } = useAuth();

  useEffect(() => {
    loadAirlines();
    loadAirports();
  }, []);

  useEffect(() => {
    loadFlights();
  }, [currentPage, selectedAirline, departureAirport, arrivalAirport, departureDate, maxPrice]);

  const loadFlights = async () => {
    setLoading(true);
    try {
      const params: any = {
        status: FlightStatus.APPROVED,
        page: currentPage,
        per_page: 12,
      };

      if (selectedAirline > 0) params.airline_id = selectedAirline;
      if (departureAirport > 0) params.departure_airport_id = departureAirport;
      if (arrivalAirport > 0) params.arrival_airport_id = arrivalAirport;
      if (departureDate) params.departure_date = departureDate;
      if (maxPrice > 0) params.max_price = maxPrice;

      const response = await flightService.getAllFlights(params);
      setFlights(response?.flights || []);
      setTotalPages(response?.pages || 1);
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to load flights');
      setFlights([]);
      setTotalPages(1);
    } finally {
      setLoading(false);
    }
  };

  const loadAirlines = async () => {
    try {
      const data = await airlineService.getAllAirlines();
      setAirlines(data || []);
    } catch (error) {
      console.error('Failed to load airlines');
      setAirlines([]);
    }
  };

  const loadAirports = async () => {
    try {
      const data = await airportService.getAllAirports();
      setAirports(data || []);
    } catch (error) {
      console.error('Failed to load airports');
      setAirports([]);
    }
  };

  const handleBookFlight = async (flight: Flight) => {
    if (!user) {
      toast.error('Please login to book a flight');
      return;
    }

    setBookingLoading(flight.flight_id);
    try {
      await bookingService.createBooking({ flight_id: flight.flight_id });
      toast.success(`Successfully booked ${flight.flight_name}!`);
      loadFlights(); // Refresh to update available seats
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to book flight');
    } finally {
      setBookingLoading(null);
    }
  };

  const resetFilters = () => {
    setSelectedAirline(0);
    setDepartureAirport(0);
    setArrivalAirport(0);
    setDepartureDate('');
    setMaxPrice(0);
    setCurrentPage(1);
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    });
  };

  const formatTime = (dateString: string) => {
    return new Date(dateString).toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="flights-page">
      <div className="page-header">
        <h1>Available Flights</h1>
        <p>Search and book your next flight</p>
      </div>

      <div className="filters-section">
        <div className="filters-grid">
          <div className="filter-group">
            <label>Airline</label>
            <select
              className="filter-select"
              value={selectedAirline}
              onChange={(e) => {
                setSelectedAirline(Number(e.target.value));
                setCurrentPage(1);
              }}
            >
              <option value={0}>All Airlines</option>
              {airlines.map((airline) => (
                <option key={airline.id} value={airline.id}>
                  {airline.name}
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>From</label>
            <select
              className="filter-select"
              value={departureAirport}
              onChange={(e) => {
                setDepartureAirport(Number(e.target.value));
                setCurrentPage(1);
              }}
            >
              <option value={0}>Any Airport</option>
              {airports.map((airport) => (
                <option key={airport.id} value={airport.id}>
                  {airport.name} ({airport.code})
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>To</label>
            <select
              className="filter-select"
              value={arrivalAirport}
              onChange={(e) => {
                setArrivalAirport(Number(e.target.value));
                setCurrentPage(1);
              }}
            >
              <option value={0}>Any Airport</option>
              {airports.map((airport) => (
                <option key={airport.id} value={airport.id}>
                  {airport.name} ({airport.code})
                </option>
              ))}
            </select>
          </div>

          <div className="filter-group">
            <label>Departure Date</label>
            <input
              type="date"
              className="filter-select"
              value={departureDate}
              onChange={(e) => {
                setDepartureDate(e.target.value);
                setCurrentPage(1);
              }}
            />
          </div>

          <div className="filter-group">
            <label>Max Price</label>
            <input
              type="number"
              className="filter-select"
              value={maxPrice || ''}
              onChange={(e) => {
                setMaxPrice(Number(e.target.value));
                setCurrentPage(1);
              }}
              placeholder="Any price"
              min="0"
            />
          </div>

          <div className="filter-group">
            <label>&nbsp;</label>
            <button className="btn btn-secondary" onClick={resetFilters}>
              Clear Filters
            </button>
          </div>
        </div>
      </div>

      <div className="flights-content">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading flights...</p>
          </div>
        ) : (
          <>
            {flights.length === 0 ? (
              <div className="empty-state">
                <p>No flights found matching your criteria</p>
                <button className="btn btn-primary" onClick={resetFilters}>
                  Clear Filters
                </button>
              </div>
            ) : (
              <>
                <div className="flights-list">
                  {flights.map((flight) => (
                    <div key={flight.flight_id} className="flight-item">
                      <div className="flight-item-header">
                        <div className="airline-info">
                          <h3>{flight.airline?.name || 'Airline'}</h3>
                          <span className="flight-name">{flight.flight_name}</span>
                        </div>
                        <div className="price-info">
                          <span className="price-label">From</span>
                          <span className="price">${flight.price}</span>
                        </div>
                      </div>

                      <div className="flight-item-body">
                        <div className="route-section">
                          <div className="time-location">
                            <span className="time">{formatTime(flight.departure_time)}</span>
                            <span className="airport-code">
                              {flight.departure_airport?.code || 'N/A'}
                            </span>
                            <span className="city">
                              {flight.departure_airport?.name || 'Unknown'}
                            </span>
                          </div>

                          <div className="flight-info-center">
                            <span className="duration">{flight.flight_duration} min</span>
                            <div className="flight-line">
                              <span className="dot"></span>
                              <span className="line"></span>
                              <span className="dot"></span>
                            </div>
                            <span className="flight-date">{formatDate(flight.departure_time)}</span>
                          </div>

                          <div className="time-location">
                            <span className="time">{formatTime(flight.arrival_time)}</span>
                            <span className="airport-code">
                              {flight.arrival_airport?.code || 'N/A'}
                            </span>
                            <span className="city">
                              {flight.arrival_airport?.name || 'Unknown'}
                            </span>
                          </div>
                        </div>

                        <div className="flight-item-footer">
                          <div className="seats-info">
                            <span className="seats-available">
                              {flight.available_seats !== undefined
                                ? `${flight.available_seats} seats available`
                                : `${flight.total_seats} total seats`}
                            </span>
                          </div>
                          <button
                            className="btn btn-book"
                            onClick={() => handleBookFlight(flight)}
                            disabled={bookingLoading === flight.flight_id}
                          >
                            {bookingLoading === flight.flight_id ? 'Booking...' : 'Book Now'}
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                {totalPages > 1 && (
                  <div className="pagination">
                    <button
                      className="pagination-btn"
                      onClick={() => setCurrentPage((prev) => Math.max(1, prev - 1))}
                      disabled={currentPage === 1}
                    >
                      Previous
                    </button>
                    <span className="pagination-info">
                      Page {currentPage} of {totalPages}
                    </span>
                    <button
                      className="pagination-btn"
                      onClick={() => setCurrentPage((prev) => Math.min(totalPages, prev + 1))}
                      disabled={currentPage === totalPages}
                    >
                      Next
                    </button>
                  </div>
                )}
              </>
            )}
          </>
        )}
      </div>
    </div>
  );
};
