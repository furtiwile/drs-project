import React, { useState } from 'react';
import type { Booking } from '../../../domain/models/Booking';
import { bookingService } from '../../../infrastructure/services/bookingService';
import { useToast } from '../../../application/context/ToastContext';
import Comments from '../Comments/Comments';
import './BookingPreview.css';

interface BookingPreviewProps {
  booking: Booking;
  isOpen: boolean;
  onClose: () => void;
  onBookingUpdated?: () => void;
}

/**
 * BookingPreview Component - Displays detailed booking information
 * Follows Single Responsibility Principle - only manages booking preview display
 * Uses composition pattern with Comments component
 */
export const BookingPreview: React.FC<BookingPreviewProps> = ({
  booking,
  isOpen,
  onClose,
  onBookingUpdated,
}) => {
  const [loading, setLoading] = useState(false);

  const toast = useToast();

  if (!isOpen || !booking || !booking.flight) {
    return null;
  }

  const flight = booking.flight;

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'long',
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

  const formatDateTime = (dateString: string) => {
    return new Date(dateString).toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getStatusDisplay = (status: string) => {
    const cleanStatus = status.replace('FlightStatus.', '');
    const statusMap: Record<string, { label: string; icon: string; class: string }> = {
      PENDING: { label: 'Pending Approval', icon: '⏳', class: 'upcoming' },
      APPROVED: { label: 'Upcoming', icon: '🛫', class: 'upcoming' },
      IN_PROGRESS: { label: 'In Progress', icon: '✈️', class: 'in-progress' },
      COMPLETED: { label: 'Completed', icon: '🛬', class: 'completed' },
      CANCELLED: { label: 'Cancelled', icon: '❌', class: 'cancelled' },
      REJECTED: { label: 'Rejected', icon: '❌', class: 'cancelled' },
    };

    return statusMap[cleanStatus] || { label: cleanStatus, icon: '❓', class: 'upcoming' };
  };

  const handleCancelBooking = async () => {
    if (!window.confirm('Are you sure you want to cancel this booking?')) {
      return;
    }

    setLoading(true);
    try {
      await bookingService.cancelBooking(booking.id);
      toast.success('Booking cancelled successfully!');
      onBookingUpdated?.();
      onClose();
    } catch (error: any) {
      const errorMessage = error.response?.data?.message || 'Failed to cancel booking';
      toast.error(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const canCancelBooking = () => {
    const cleanStatus = flight.status.replace('FlightStatus.', '');
    return cleanStatus === 'APPROVED' || cleanStatus === 'PENDING';
  };

  const statusDisplay = getStatusDisplay(flight.status);
  const cleanStatus = flight.status.replace('FlightStatus.', '');
  const canAddComment = cleanStatus === 'COMPLETED';

  return (
    <div className="booking-preview-overlay" onClick={onClose}>
      <div className="booking-preview-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="booking-preview-header">
          <h2 className="booking-preview-title">Booking Details</h2>
          <button className="booking-preview-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="booking-preview-content">
          {/* Flight Route */}
          <div className="booking-preview-section">
            <div className="flight-route-preview">
              <div className="route-header">
                <h3 className="flight-name-large">{flight.flight_name}</h3>
                <span className="airline-badge">
                  {flight.airline?.name || `Airline #${flight.airline_id}`}
                </span>
              </div>

              <div className="route-display">
                <div className="airport-detail">
                  <h4 className="airport-code-large">
                    {flight.departure_airport?.code || 'N/A'}
                  </h4>
                  <p className="airport-name-detail">
                    {flight.departure_airport?.name || 'Unknown Airport'}
                  </p>
                  <p className="airport-time-detail">{formatTime(flight.departure_time)}</p>
                </div>

                <div className="route-connector">
                  <div
                    style={{
                      textAlign: 'center',
                      fontSize: '12px',
                      color: '#6c757d',
                      marginBottom: '5px',
                    }}
                  >
                    Duration
                  </div>
                  <div className="connector-line"></div>
                  <div className="flight-duration-detail">{flight.flight_duration}</div>
                </div>

                <div className="airport-detail">
                  <h4 className="airport-code-large">
                    {flight.arrival_airport?.code || 'N/A'}
                  </h4>
                  <p className="airport-name-detail">
                    {flight.arrival_airport?.name || 'Unknown Airport'}
                  </p>
                  <p className="airport-time-detail">{formatTime(flight.arrival_time)}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Booking Details */}
          <div className="booking-preview-section">
            <h4 className="booking-preview-section-title">Booking Information</h4>
            <div className="booking-details-grid">
              <div className="detail-card">
                <div className="detail-label">Booking Status</div>
                <div
                  className={`status-display ${statusDisplay.class}`}
                  style={{ marginTop: '8px' }}
                >
                  <span className="status-icon">{statusDisplay.icon}</span>
                  <span>{statusDisplay.label}</span>
                </div>
              </div>

              <div className="detail-card date">
                <div className="detail-label">Departure Date</div>
                <p className="detail-value">{formatDate(flight.departure_time)}</p>
              </div>

              <div className="detail-card date">
                <div className="detail-label">Booked On</div>
                <p className="detail-value">{formatDateTime(booking.created_at)}</p>
              </div>

              <div className="detail-card price">
                <div className="detail-label">Price</div>
                <p className="detail-value price">${(Number(flight.price) || 0).toFixed(2)}</p>
              </div>

              <div className="detail-card seats">
                <div className="detail-label">Seats Available</div>
                <p className="detail-value">{flight.available_seats || 0} / {flight.total_seats}</p>
              </div>

              <div className="detail-card">
                <div className="detail-label">Distance</div>
                <p className="detail-value">{flight.flight_distance_km} km</p>
              </div>
            </div>
          </div>

          {/* Comments/Ratings Section */}
          <Comments
            flightId={flight.flight_id}
            canAddComment={canAddComment}
          />

          {/* Actions */}
          <div className="booking-actions">
            {canCancelBooking() && (
              <button
                className="action-button danger"
                onClick={handleCancelBooking}
                disabled={loading}
              >
                {loading ? 'Cancelling...' : 'Cancel Booking'}
              </button>
            )}
            <button className="action-button secondary" onClick={onClose}>
              Close
            </button>
          </div>
        </div>

        {/* Footer */}
        <div className="booking-preview-footer">
          <span className="booking-id-footer">Booking #{booking.id}</span>
          <span>Flight ID: {flight.flight_id}</span>
        </div>
      </div>
    </div>
  );
};

export default BookingPreview;
