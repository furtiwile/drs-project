import React, { useState, useEffect } from 'react';
import type { Flight } from '../../../domain/models/Flight';
import { FlightStatus } from '../../../domain/enums/FlightStatus';
import { flightService } from '../../../infrastructure/services/flightService';
import { reportService } from '../../../infrastructure/services/reportService';
import { useToast } from '../../../application/context/ToastContext';
import { useSocket } from '../../../application/context/SocketContext';
import './AdminDashboard.css';

interface RejectModalData {
  flight: Flight;
  isOpen: boolean;
}

interface CancelModalData {
  flight: Flight;
  isOpen: boolean;
}

export const AdminDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'pending' | 'approved'>('pending');
  const [pendingFlights, setPendingFlights] = useState<Flight[]>([]);
  const [approvedFlights, setApprovedFlights] = useState<Flight[]>([]);
  const [loading, setLoading] = useState(false);
  const [rejectModal, setRejectModal] = useState<RejectModalData>({
    flight: null as any,
    isOpen: false,
  });
  const [cancelModal, setCancelModal] = useState<CancelModalData>({
    flight: null as any,
    isOpen: false,
  });
  const [rejectionReason, setRejectionReason] = useState('');
  const [actionLoading, setActionLoading] = useState(false);
  const [reportLoading, setReportLoading] = useState(false);

  const toast = useToast();
  const socket = useSocket();

  useEffect(() => {
    if (socket) {
      loadFlights();
      setupWebSocketListeners();
    }
  }, [socket]);

  const setupWebSocketListeners = () => {
    socket.on('new_flight_pending', (data: any) => {
      toast.info(`New flight pending approval: ${data.flight_name}`);
      loadFlights();
    });

    socket.on('flight_cancelled', (data: any) => {
      toast.warning(`Flight ${data.flight_name} has been cancelled`);
      loadFlights();
    });

    return () => {
      socket.off('new_flight_pending');
      socket.off('flight_cancelled');
    };
  };

  const loadFlights = async () => {
    setLoading(true);
    try {
      const [pending, approved] = await Promise.all([
        flightService.getAllFlights({ status: FlightStatus.PENDING, per_page: 100 }),
        flightService.getAllFlights({ status: FlightStatus.APPROVED, per_page: 100 }),
      ]);
      setPendingFlights(pending?.flights || []);
      setApprovedFlights(approved?.flights || []);
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to load flights');
      setPendingFlights([]);
      setApprovedFlights([]);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateReport = async () => {
    setReportLoading(true);
    try {
      const tab = activeTab == "pending" ? "upcoming" : "in_progress";
      await reportService.generateReport(tab);
      toast.success('Flight report generated successfully!');
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to generate report');
    } finally {
      setReportLoading(false);
    }
  };

  const handleApproveFlight = async (flight: Flight) => {
    setActionLoading(true);
    try {
      await flightService.approveFlight(flight.flight_id);
      toast.success(`Flight ${flight.flight_name} approved successfully!`);
      loadFlights();
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to approve flight');
    } finally {
      setActionLoading(false);
    }
  };

  const openRejectModal = (flight: Flight) => {
    setRejectModal({ flight, isOpen: true });
    setRejectionReason('');
  };

  const closeRejectModal = () => {
    setRejectModal({ flight: null as any, isOpen: false });
    setRejectionReason('');
  };

  const handleRejectFlight = async () => {
    if (!rejectionReason.trim() || rejectionReason.length < 10) {
      toast.error('Rejection reason must be at least 10 characters');
      return;
    }

    setActionLoading(true);
    try {
      await flightService.rejectFlight(rejectModal.flight.flight_id, rejectionReason);
      toast.success(`Flight ${rejectModal.flight.flight_name} rejected`);
      closeRejectModal();
      loadFlights();
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to reject flight');
    } finally {
      setActionLoading(false);
    }
  };

  const openCancelModal = (flight: Flight) => {
    setCancelModal({ flight, isOpen: true });
  };

  const closeCancelModal = () => {
    setCancelModal({ flight: null as any, isOpen: false });
  };

  const handleCancelFlight = async () => {
    setActionLoading(true);
    try {
      await flightService.cancelFlight(cancelModal.flight.flight_id);
      toast.success(`Flight ${cancelModal.flight.flight_name} cancelled. Users notified by email.`);
      closeCancelModal();
      loadFlights();
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to cancel flight');
    } finally {
      setActionLoading(false);
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

  const renderFlightCard = (flight: Flight, isPending: boolean) => (
    <div key={flight.flight_id} className="flight-card">
      <div className="flight-card-header">
        <h3>{flight.flight_name}</h3>
        <span className="flight-badge">
          {flight.airline?.name || `Airline #${flight.airline_id}`}
        </span>
      </div>

      <div className="flight-card-body">
        <div className="flight-route">
          <div className="airport">
            <span className="airport-code">
              {flight.departure_airport?.code || 'N/A'}
            </span>
            <span className="airport-name">
              {flight.departure_airport?.name || 'Unknown'}
            </span>
          </div>
          <div className="flight-arrow">→</div>
          <div className="airport">
            <span className="airport-code">
              {flight.arrival_airport?.code || 'N/A'}
            </span>
            <span className="airport-name">
              {flight.arrival_airport?.name || 'Unknown'}
            </span>
          </div>
        </div>

        <div className="flight-details">
          <div className="detail-item">
            <span className="detail-label">Departure:</span>
            <span className="detail-value">{formatDateTime(flight.departure_time)}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Duration:</span>
            <span className="detail-value">{flight.flight_duration}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Price:</span>
            <span className="detail-value">${flight.price}</span>
          </div>
          <div className="detail-item">
            <span className="detail-label">Seats:</span>
            <span className="detail-value">{flight.total_seats}</span>
          </div>
        </div>
      </div>

      <div className="flight-card-actions">
        {isPending ? (
          <>
            <button
              className="btn btn-success"
              onClick={() => handleApproveFlight(flight)}
              disabled={actionLoading}
            >
              Approve
            </button>
            <button
              className="btn btn-danger"
              onClick={() => openRejectModal(flight)}
              disabled={actionLoading}
            >
              Reject
            </button>
          </>
        ) : (
          <button
            className="btn btn-warning"
            onClick={() => openCancelModal(flight)}
            disabled={actionLoading}
          >
            Cancel Flight
          </button>
        )}
      </div>
    </div>
  );

  return (
    <div className="admin-dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <div>
            <h1>Admin Dashboard</h1>
            <p>Manage flight approvals and cancellations</p>
          </div>
        </div>
      </div>

      <div className="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === 'pending' ? 'active' : ''}`}
          onClick={() => setActiveTab('pending')}
        >
          Pending Flights
          {pendingFlights.length > 0 && (
            <span className="badge">{pendingFlights.length}</span>
          )}
        </button>
        <button
          className={`tab-button ${activeTab === 'approved' ? 'active' : ''}`}
          style={{ marginRight: 'auto' }}
          onClick={() => setActiveTab('approved')}
        >
          Approved Flights
          {approvedFlights.length > 0 && (
            <span className="badge">{approvedFlights.length}</span>
          )}
        </button>

        <button
            className="btn btn-primary report-btn"
            onClick={handleGenerateReport}
            disabled={reportLoading}
          >
            <svg className="report-btn-svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <polyline points="10 9 9 9 8 9" />
            </svg>
            {reportLoading ? 'Generating...' : 'Generate Report'}
          </button>
      </div>

      <div className="dashboard-content">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading flights...</p>
          </div>
        ) : (
          <>
            {activeTab === 'pending' && (
              <div className="flights-grid">
                {pendingFlights.length === 0 ? (
                  <div className="empty-state">
                    <p>No pending flights</p>
                  </div>
                ) : (
                  pendingFlights.map((flight) => renderFlightCard(flight, true))
                )}
              </div>
            )}

            {activeTab === 'approved' && (
              <div className="flights-grid">
                {approvedFlights.length === 0 ? (
                  <div className="empty-state">
                    <p>No approved flights</p>
                  </div>
                ) : (
                  approvedFlights.map((flight) => renderFlightCard(flight, false))
                )}
              </div>
            )}
          </>
        )}
      </div>

      {/* Reject Modal */}
      {rejectModal.isOpen && (
        <div className="modal-overlay" onClick={closeRejectModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Reject Flight</h2>
              <button className="modal-close" onClick={closeRejectModal}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <p>
                Please provide a reason for rejecting flight{' '}
                <strong>{rejectModal.flight?.flight_name}</strong>:
              </p>
              <textarea
                className="rejection-textarea"
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="Enter rejection reason (minimum 10 characters)..."
                rows={5}
              />
              <p className="char-count">
                {rejectionReason.length} / 10 characters minimum
              </p>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={closeRejectModal}>
                Cancel
              </button>
              <button
                className="btn btn-danger"
                onClick={handleRejectFlight}
                disabled={actionLoading || rejectionReason.length < 10}
              >
                {actionLoading ? 'Rejecting...' : 'Reject Flight'}
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Cancel Modal */}
      {cancelModal.isOpen && (
        <div className="modal-overlay" onClick={closeCancelModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Cancel Flight</h2>
              <button className="modal-close" onClick={closeCancelModal}>
                ×
              </button>
            </div>
            <div className="modal-body">
              <p>
                Are you sure you want to cancel flight{' '}
                <strong>{cancelModal.flight?.flight_name}</strong>?
              </p>
              <p className="warning-text">
                All users who have booked this flight will be notified by email.
              </p>
            </div>
            <div className="modal-actions">
              <button className="btn btn-secondary" onClick={closeCancelModal}>
                No, Keep Flight
              </button>
              <button
                className="btn btn-warning"
                onClick={handleCancelFlight}
                disabled={actionLoading}
              >
                {actionLoading ? 'Cancelling...' : 'Yes, Cancel Flight'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};