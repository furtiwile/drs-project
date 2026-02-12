import React, { useState, useEffect } from 'react';
import type { Booking } from '../../../domain/models/Booking';
import { FlightStatusColors } from '../../../domain/enums/FlightStatus';
import { bookingService } from '../../../infrastructure/services/bookingService';
import { useToast } from '../../../application/context/ToastContext';
import { useAuth } from '../../../application/context/AuthContext';
import { useSocket } from '../../../application/context/SocketContext';
import './MyBookingsPage.css';

export const MyBookingsPage: React.FC = () => {
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [loading, setLoading] = useState(false);

  const toast = useToast();
  const { user } = useAuth();
  const socket = useSocket();

  useEffect(() => {
    if (user) {
      loadBookings();
      setupWebSocketListeners();
    }
  }, [user]);

  const setupWebSocketListeners = () => {
    // Listen for flight cancellations
    socket.on('flight_cancelled', (data: any) => {
      toast.warning(`Your flight ${data.flight_name} has been cancelled!`);
      loadBookings(); // Refresh the list
    });

    // Listen for flight status updates
    socket.on('flight_started', (data: any) => {
      toast.info(`Flight ${data.flight_name} has started!`);
      loadBookings();
    });

    socket.on('flight_completed', (data: any) => {
      toast.success(`Flight ${data.flight_name} has completed!`);
      loadBookings();
    });

    return () => {
      socket.off('flight_cancelled');
      socket.off('flight_started');
      socket.off('flight_completed');
    };
  };

  const loadBookings = async () => {
    if (!user) return;

    setLoading(true);
    try {
      const data = await bookingService.getUserBookings();
      setBookings(data);

      // Join flight rooms for real-time updates
      data.forEach((booking) => {
        if (booking.flight) {
          socket.joinFlightRoom(booking.flight.flight_id);
        }
      });
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to load bookings');
    } finally {
      setLoading(false);
    }
  };

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
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

  const getStatusCategory = (status: string): string => {
    const cleanStatus = status.replace('FlightStatus.', '');
    
    switch (cleanStatus) {
      case 'APPROVED':
        return 'Upcoming';
      case 'IN_PROGRESS':
        return 'In Progress';
      case 'COMPLETED':
        return 'Completed';
      case 'CANCELLED':
        return 'Cancelled';
      default:
        return 'Unknown';
    }
  };

  const categorizeBookings = () => {
    const upcoming: Booking[] = [];
    const inProgress: Booking[] = [];
    const completed: Booking[] = [];
    const cancelled: Booking[] = [];

    bookings.forEach((booking) => {
      if (!booking.flight) return;

      const cleanStatus = booking.flight.status.replace('FlightStatus.', '');

      switch (cleanStatus) {
        case 'APPROVED':
          upcoming.push(booking);
          break;
        case 'IN_PROGRESS':
          inProgress.push(booking);
          break;
        case 'COMPLETED':
          completed.push(booking);
          break;
        case 'CANCELLED':
          cancelled.push(booking);
          break;
      }
    });

    return { upcoming, inProgress, completed, cancelled };
  };

  const renderBookingCard = (booking: Booking) => {
    if (!booking.flight) return null;

    const flight = booking.flight;
    const statusCategory = getStatusCategory(flight.status);
    const cleanStatus = flight.status.replace('FlightStatus.', '');

    return (
      <div key={booking.id} className="booking-card">
        <div className="booking-header">
          <div className="booking-id">Booking #{booking.id}</div>
          <span className={`status-badge ${FlightStatusColors[cleanStatus]}`}>
            {statusCategory}
          </span>
        </div>

        <div className="booking-body">
          <div className="flight-info-section">
            <h3>{flight.flight_name}</h3>
            <span className="airline-name">
              {flight.airline?.name || `Airline #${flight.airline_id}`}
            </span>
          </div>

          <div className="route-info">
            <div className="location">
              <span className="time">{formatTime(flight.departure_time)}</span>
              <span className="airport-code">
                {flight.departure_airport?.code || 'N/A'}
              </span>
              <span className="city">{flight.departure_airport?.name || 'Unknown'}</span>
            </div>

            <div className="route-line">
              <span className="duration">{flight.flight_duration}</span>
              <div className="line-visual">
                <span className="dot"></span>
                <span className="line"></span>
                <span className="dot"></span>
              </div>
            </div>

            <div className="location">
              <span className="time">{formatTime(flight.arrival_time)}</span>
              <span className="airport-code">
                {flight.arrival_airport?.code || 'N/A'}
              </span>
              <span className="city">{flight.arrival_airport?.name || 'Unknown'}</span>
            </div>
          </div>

          <div className="booking-details">
            <div className="detail-row">
              <span className="label">Departure Date:</span>
              <span className="value">{formatDate(flight.departure_time)}</span>
            </div>
            <div className="detail-row">
              <span className="label">Booked On:</span>
              <span className="value">{formatDateTime(booking.created_at)}</span>
            </div>
            <div className="detail-row">
              <span className="label">Price:</span>
              <span className="value price">${flight.price}</span>
            </div>
          </div>

          {cleanStatus === 'CANCELLED' && (
            <div className="cancellation-notice">
              <strong>⚠ This flight has been cancelled</strong>
              <p>You should have received an email notification about this cancellation.</p>
            </div>
          )}
        </div>
      </div>
    );
  };

  if (!user) {
    return (
      <div className="bookings-page">
        <div className="empty-state">
          <p>Please login to view your bookings</p>
        </div>
      </div>
    );
  }

  const { upcoming, inProgress, completed, cancelled } = categorizeBookings();

  return (
    <div className="bookings-page">
      <div className="page-header">
        <h1>My Bookings</h1>
        <p>View and manage your flight bookings</p>
      </div>

      {loading ? (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Loading bookings...</p>
        </div>
      ) : bookings.length === 0 ? (
        <div className="empty-state">
          <p>You haven't booked any flights yet</p>
          <a href="/flights" className="btn btn-primary">
            Browse Available Flights
          </a>
        </div>
      ) : (
        <div className="bookings-sections">
          {upcoming.length > 0 && (
            <section className="bookings-section">
              <h2 className="section-title">Upcoming Flights ({upcoming.length})</h2>
              <div className="bookings-grid">{upcoming.map(renderBookingCard)}</div>
            </section>
          )}

          {inProgress.length > 0 && (
            <section className="bookings-section">
              <h2 className="section-title">In Progress ({inProgress.length})</h2>
              <div className="bookings-grid">{inProgress.map(renderBookingCard)}</div>
            </section>
          )}

          {completed.length > 0 && (
            <section className="bookings-section">
              <h2 className="section-title">Completed ({completed.length})</h2>
              <div className="bookings-grid">{completed.map(renderBookingCard)}</div>
            </section>
          )}

          {cancelled.length > 0 && (
            <section className="bookings-section">
              <h2 className="section-title">Cancelled ({cancelled.length})</h2>
              <div className="bookings-grid">{cancelled.map(renderBookingCard)}</div>
            </section>
          )}
        </div>
      )}
    </div>
  );
};