import React, { useState } from 'react';
import type { Flight } from '../../../domain/models/Flight';
import Comments from '../Comments/Comments';
import { FlightTimer } from '../FlightTimer/FlightTimer';
import './FlightDetail.css';

interface FlightDetailProps {
  flight: Flight;
  isOpen: boolean;
  onClose: () => void;
  onBook?: (flight: Flight) => void;
  isBooking?: boolean;
}

/**
 * FlightDetail Component - Displays detailed flight information
 * Follows Single Responsibility Principle - only manages flight detail display
 * Reuses Comments component for ratings/reviews
 */
export const FlightDetail: React.FC<FlightDetailProps> = ({
  flight,
  isOpen,
  onClose,
  onBook,
  isBooking = false,
}) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set(['info']));

  if (!isOpen) {
    return null;
  }

  const toggleSection = (section: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(section)) {
      newExpanded.delete(section);
    } else {
      newExpanded.add(section);
    }
    setExpandedSections(newExpanded);
  };

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

  const getStatusDisplay = (status: string) => {
    const cleanStatus = status.replace('FlightStatus.', '');
    const statusMap: Record<string, { label: string; icon: string; class: string }> = {
      PENDING: { label: 'Pending Approval', icon: '⏳', class: 'pending' },
      APPROVED: { label: 'Available', icon: '🛫', class: 'approved' },
      IN_PROGRESS: { label: 'In Progress', icon: '✈️', class: 'in-progress' },
      COMPLETED: { label: 'Completed', icon: '🛬', class: 'completed' },
      CANCELLED: { label: 'Cancelled', icon: '❌', class: 'cancelled' },
      REJECTED: { label: 'Rejected', icon: '❌', class: 'rejected' },
    };

    return statusMap[cleanStatus] || { label: cleanStatus, icon: '❓', class: 'unknown' };
  };

  const statusDisplay = getStatusDisplay(flight.status);
  const cleanStatus = flight.status.replace('FlightStatus.', '');
  const canAddComment = cleanStatus === 'COMPLETED';

  return (
    <div className="flight-detail-overlay" onClick={onClose}>
      <div className="flight-detail-modal" onClick={(e) => e.stopPropagation()}>
        {/* Header */}
        <div className="flight-detail-header">
          <h2 className="flight-detail-title">{flight.flight_name}</h2>
          <button className="flight-detail-close" onClick={onClose}>
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flight-detail-content">
          {/* Route Section */}
          <div className="flight-detail-section">
            <div
              className="section-header"
              onClick={() => toggleSection('route')}
            >
              <h3 className="section-title">
                {expandedSections.has('route') ? '▼' : '▶'} Route Information
              </h3>
            </div>

            {expandedSections.has('route') && (
              <div className="section-body route-section">
                <div className="flight-route-info">
                  <div className="airport-detail">
                    <h4 className="airport-code-detail">
                      {flight.departure_airport?.code || 'N/A'}
                    </h4>
                    <p className="airport-name-detail">
                      {flight.departure_airport?.name || 'Unknown Airport'}
                    </p>
                    <p className="airport-time-detail">{formatTime(flight.departure_time)}</p>
                  </div>

                  <div className="route-connector">
                    <div className="connector-label">
                      {flight.flight_duration}
                    </div>
                    <div className="connector-line"></div>
                    <div className="connector-label">{flight.flight_distance_km} km</div>
                  </div>

                  <div className="airport-detail">
                    <h4 className="airport-code-detail">
                      {flight.arrival_airport?.code || 'N/A'}
                    </h4>
                    <p className="airport-name-detail">
                      {flight.arrival_airport?.name || 'Unknown Airport'}
                    </p>
                    <p className="airport-time-detail">{formatTime(flight.arrival_time)}</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Flight Information */}
          <div className="flight-detail-section">
            <div
              className="section-header"
              onClick={() => toggleSection('info')}
            >
              <h3 className="section-title">
                {expandedSections.has('info') ? '▼' : '▶'} Flight Details
              </h3>
            </div>

            {expandedSections.has('info') && (
              <div className="section-body">
                <div className="details-grid">
                  <div className="detail-item">
                    <span className="detail-label">Airline</span>
                    <span className="detail-value">{flight.airline?.name || 'Unknown'}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">Status</span>
                    <span className={`status-badge-detail ${statusDisplay.class}`}>
                      {statusDisplay.icon} {statusDisplay.label}
                    </span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">Departure</span>
                    <span className="detail-value">
                      {formatDate(flight.departure_time)} {formatTime(flight.departure_time)}
                    </span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">Arrival</span>
                    <span className="detail-value">
                      {formatDate(flight.arrival_time)} {formatTime(flight.arrival_time)}
                    </span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">Price</span>
                    <span className="detail-value price">${(Number(flight.price) || 0).toFixed(2)}</span>
                  </div>

                  <div className="detail-item">
                    <span className="detail-label">Available Seats</span>
                    <span className="detail-value">
                      {flight.available_seats || 0} / {flight.total_seats}
                    </span>
                  </div>
                </div>

                {/* Timer for in-progress flights */}
                {cleanStatus === 'IN_PROGRESS' && (
                  <div style={{ marginTop: '15px' }}>
                    <FlightTimer
                      arrivalTime={flight.arrival_time}
                    />
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Comments/Reviews Section */}
          <div className="flight-detail-section">
            <div
              className="section-header"
              onClick={() => toggleSection('comments')}
            >
              <h3 className="section-title">
                {expandedSections.has('comments') ? '▼' : '▶'} Comments & Reviews
              </h3>
            </div>

            {expandedSections.has('comments') && (
              <div className="section-body">
                <Comments
                  flightId={flight.flight_id}
                  canAddComment={canAddComment}
                />
              </div>
            )}
          </div>
        </div>

        {/* Footer with Actions */}
        <div className="flight-detail-footer">
          {onBook && cleanStatus === 'APPROVED' && (
            <button
              className="action-btn primary"
              onClick={() => onBook(flight)}
              disabled={isBooking || flight.available_seats === 0}
            >
              {isBooking ? 'Booking...' : flight.available_seats === 0 ? 'Sold Out' : 'Book Flight'}
            </button>
          )}
          <button className="action-btn secondary" onClick={onClose}>
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default FlightDetail;
