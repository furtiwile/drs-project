import React, { useState, useEffect } from 'react';
import type { Flight } from '../../../domain/models/Flight';
import type { Airline } from '../../../domain/models/Airline';
import type { Airport } from '../../../domain/models/Airport';
import { FlightStatus } from '../../../domain/enums/FlightStatus';
import { Role } from '../../../domain/enums/Role';
import { flightService } from '../../../infrastructure/services/flightService';
import { airlineService } from '../../../infrastructure/services/airlineService';
import { airportService } from '../../../infrastructure/services/airportService';
import { bookingService } from '../../../infrastructure/services/bookingService';
import { useToast } from '../../../application/context/ToastContext';
import { useAuth } from '../../../application/context/AuthContext';
import { useSocket } from '../../../application/context/SocketContext';
import { FlightTimer } from '../../shared/FlightTimer/FlightTimer';
import './FlightsPage.css';

type TabType = 'upcoming' | 'in-progress' | 'completed';

export const FlightsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('upcoming');
  const [flights, setFlights] = useState<Flight[]>([]);
  const [airlines, setAirlines] = useState<Airline[]>([]);
  const [airports, setAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(false);
  const [totalPages, setTotalPages] = useState(1);
  const [currentPage, setCurrentPage] = useState(1);
  const [deleteLoading, setDeleteLoading] = useState<number | null>(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<number | null>(null);

  // Search & Filters
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [selectedAirline, setSelectedAirline] = useState<number>(0);
  const [departureAirport, setDepartureAirport] = useState<number>(0);
  const [arrivalAirport, setArrivalAirport] = useState<number>(0);
  const [departureDate, setDepartureDate] = useState<string>('');
  const [maxPrice, setMaxPrice] = useState<number>(0);
  const [bookingLoading, setBookingLoading] = useState<number | null>(null);

  const toast = useToast();
  const { user } = useAuth();
  const { on, off } = useSocket();

  useEffect(() => {
    loadAirlines();
    loadAirports();
  }, []);

  useEffect(() => {
    loadFlights();
  }, [activeTab, currentPage, searchQuery, selectedAirline, departureAirport, arrivalAirport, departureDate, maxPrice]);

  useEffect(() => {
    // Listen to websocket events for real-time updates
    on('flight_deleted', handleFlightDeleted);
    on('flight_status_updated', handleFlightStatusUpdated);
    on('flight_started', handleFlightStarted);
    on('flight_completed', handleFlightCompleted);
    on('flight_cancelled', handleFlightCancelled);

    return () => {
      off('flight_deleted');
      off('flight_status_updated');
      off('flight_started');
      off('flight_completed');
      off('flight_cancelled');
    };
  }, [flights]);

  const handleFlightDeleted = (data: any) => {
    setFlights((prev) => prev.filter((f) => f.flight_id !== data.flight_id));
    toast.info(`Flight ${data.flight_name} has been deleted`);
  };

  const handleFlightStatusUpdated = () => {
    loadFlights(); // Refresh to get updated data
  };

  const handleFlightStarted = (data: any) => {
    toast.info(`Flight ${data.flight_name} has started`);
    loadFlights();
  };

  const handleFlightCompleted = (data: any) => {
    toast.info(`Flight ${data.flight_name} has completed`);
    loadFlights();
  };

  const handleFlightCancelled = (data: any) => {
    toast.warning(`Flight ${data.flight_name} has been cancelled`);
    loadFlights();
  };

  const loadFlights = async () => {
    setLoading(true);
    try {
      const params: any = {
        page: currentPage,
        per_page: 12,
      };

      if (searchQuery.trim()) params.flight_name = searchQuery.trim();
      if (selectedAirline > 0) params.airline_id = selectedAirline;
      if (departureAirport > 0) params.departure_airport_id = departureAirport;
      if (arrivalAirport > 0) params.arrival_airport_id = arrivalAirport;
      if (departureDate) params.departure_date = departureDate;
      if (maxPrice > 0) params.max_price = maxPrice;

      const response = await flightService.getFlightsByTab(activeTab, params);
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
      loadFlights();
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to book flight');
    } finally {
      setBookingLoading(null);
    }
  };

  const handleDeleteFlight = async (flightId: number) => {
    setDeleteLoading(flightId);
    try {
      await flightService.deleteFlight(flightId);
      toast.success('Flight deleted successfully');
      setFlights((prev) => prev.filter((f) => f.flight_id !== flightId));
      setShowDeleteConfirm(null);
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to delete flight');
    } finally {
      setDeleteLoading(null);
    }
  };

  const resetFilters = () => {
    setSearchQuery('');
    setSelectedAirline(0);
    setDepartureAirport(0);
    setArrivalAirport(0);
    setDepartureDate('');
    setMaxPrice(0);
    setCurrentPage(1);
  };

  const handleTabChange = (tab: TabType) => {
    setActiveTab(tab);
    setCurrentPage(1);
  };

  const isAdmin = user?.role === Role.ADMINISTRATOR;
  const canBook = activeTab === 'upcoming';

  const getStatusBadge = (status: FlightStatus) => {
    const statusConfig: Record<FlightStatus, { label: string; className: string }> = {
      [FlightStatus.PENDING]: { label: 'Pending', className: 'status-pending' },
      [FlightStatus.APPROVED]: { label: 'Approved', className: 'status-approved' },
      [FlightStatus.REJECTED]: { label: 'Rejected', className: 'status-rejected' },
      [FlightStatus.IN_PROGRESS]: { label: 'In Flight', className: 'status-in-progress' },
      [FlightStatus.COMPLETED]: { label: 'Completed', className: 'status-completed' },
      [FlightStatus.CANCELLED]: { label: 'Cancelled', className: 'status-cancelled' },
    };

    const config = statusConfig[status] || { label: status, className: 'status-default' };
    return <span className={`status-badge ${config.className}`}>{config.label}</span>;
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
        <h1>Flight Management</h1>
        <p>{activeTab === 'upcoming' ? 'Browse and book available flights' : activeTab === 'in-progress' ? 'Flights currently in progress' : 'View flight history'}</p>
      </div>

      {/* Tab Navigation */}
      <div className="tabs-container">
        <div className="tabs">
          <button
            className={`tab ${activeTab === 'upcoming' ? 'active' : ''}`}
            onClick={() => handleTabChange('upcoming')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            </svg>
            Upcoming Flights
          </button>
          <button
            className={`tab ${activeTab === 'in-progress' ? 'active' : ''}`}
            onClick={() => handleTabChange('in-progress')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
            In Progress
          </button>
          <button
            className={`tab ${activeTab === 'completed' ? 'active' : ''}`}
            onClick={() => handleTabChange('completed')}
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <polyline points="20 6 9 17 4 12" />
            </svg>
            Completed & Cancelled
          </button>
        </div>
      </div>

      {/* Search Bar */}
      <div className="search-section">
        <div className="search-group">
          <svg className="search-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <circle cx="11" cy="11" r="8" />
            <path d="m21 21-4.35-4.35" />
          </svg>
          <input
            type="text"
            className="search-input"
            placeholder="Search by flight name..."
            value={searchQuery}
            onChange={(e) => {
              setSearchQuery(e.target.value);
              setCurrentPage(1);
            }}
          />
        </div>
        <div className="airline-search">
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
      </div>

      {/* Advanced Filters (collapsible) - only for upcoming tab */}
      {activeTab === 'upcoming' && (
        <div className="filters-section">
          <div className="filters-grid">
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
      )}

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
                <p>No flights found{searchQuery || selectedAirline ? ' matching your criteria' : ` in ${activeTab.replace('-', ' ')}`}</p>
                {(searchQuery || selectedAirline) && (
                  <button className="btn btn-primary" onClick={resetFilters}>
                    Clear Filters
                  </button>
                )}
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
                          {getStatusBadge(flight.status)}
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

                        {/* Show timer for in-progress flights */}
                        {activeTab === 'in-progress' && (
                          <div className="timer-section">
                            <FlightTimer 
                              arrivalTime={flight.arrival_time} 
                              onComplete={() => loadFlights()}
                            />
                          </div>
                        )}

                        <div className="flight-item-footer">
                          <div className="seats-info">
                            {activeTab === 'upcoming' && (
                              <span className="seats-available">
                                {flight.available_seats !== undefined
                                  ? `${flight.available_seats} seats available`
                                  : `${flight.total_seats} total seats`}
                              </span>
                            )}
                            {activeTab === 'completed' && flight.rejection_reason && (
                              <span className="rejection-reason" title={flight.rejection_reason}>
                                Reason: {flight.rejection_reason}
                              </span>
                            )}
                          </div>

                          <div className="flight-actions">
                            {/* Book button for upcoming flights */}
                            {canBook && flight.status === FlightStatus.APPROVED && (
                              <button
                                className="btn btn-book"
                                onClick={() => handleBookFlight(flight)}
                                disabled={bookingLoading === flight.flight_id || flight.available_seats === 0}
                              >
                                {bookingLoading === flight.flight_id ? 'Booking...' : 'Book Now'}
                              </button>
                            )}

                            {/* Delete button for admin */}
                            {isAdmin && (
                              <>
                                {showDeleteConfirm === flight.flight_id ? (
                                  <div className="delete-confirm">
                                    <span>Delete this flight?</span>
                                    <button
                                      className="btn btn-danger btn-sm"
                                      onClick={() => handleDeleteFlight(flight.flight_id)}
                                      disabled={deleteLoading === flight.flight_id}
                                    >
                                      {deleteLoading === flight.flight_id ? 'Deleting...' : 'Confirm'}
                                    </button>
                                    <button
                                      className="btn btn-secondary btn-sm"
                                      onClick={() => setShowDeleteConfirm(null)}
                                    >
                                      Cancel
                                    </button>
                                  </div>
                                ) : (
                                  <button
                                    className="btn btn-danger-outline"
                                    onClick={() => setShowDeleteConfirm(flight.flight_id)}
                                    title="Delete flight"
                                  >
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                                      <polyline points="3 6 5 6 21 6" />
                                      <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                                    </svg>
                                    Delete
                                  </button>
                                )}
                              </>
                            )}
                          </div>
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
