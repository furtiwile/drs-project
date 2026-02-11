import React, { useState, useEffect } from 'react';
import type { Flight } from '../../../domain/models/Flight';
import type { Airline } from '../../../domain/models/Airline';
import type{ Airport } from '../../../domain/models/Airport';
import { FlightStatus, FlightStatusLabels, FlightStatusColors } from '../../../domain/enums/FlightStatus';
import type { CreateFlightDto } from '../../../domain/dtos/FlightDtos';
import { flightService } from '../../../infrastructure/services/flightService';
import { airlineService } from '../../../infrastructure/services/airlineService';
import { airportService } from '../../../infrastructure/services/airportService';
import { useToast } from '../../../application/context/ToastContext';
import { useSocket } from '../../../application/context/SocketContext';
import './ManagerDashboard.css';

type TabType = 'pending' | 'approved' | 'rejected' | 'in_progress' | 'completed';

export const ManagerDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState<TabType>('pending');
  const [flights, setFlights] = useState<Record<TabType, Flight[]>>({
    pending: [],
    approved: [],
    rejected: [],
    in_progress: [],
    completed: [],
  });
  const [airlines, setAirlines] = useState<Airline[]>([]);
  const [airports, setAirports] = useState<Airport[]>([]);
  const [loading, setLoading] = useState(false);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [createFormData, setCreateFormData] = useState<CreateFlightDto>({
    flight_name: '',
    airline_id: 0,
    departure_airport_id: 0,
    arrival_airport_id: 0,
    departure_time: '',
    arrival_time: '',
    price: 0,
    total_seats: 0,
    flight_distance_km: 0,
    flight_duration: 0,
  });
  const [actionLoading, setActionLoading] = useState(false);

  const toast = useToast();
  const socket = useSocket();

  useEffect(() => {
    loadData();
    setupWebSocketListeners();
  }, []);

  const setupWebSocketListeners = () => {
    // Listen for flight status updates
    socket.on('flight_status_updated', (data: any) => {
      const status = data.status.toLowerCase();
      toast.info(`Flight ${data.flight_name} has been ${status}!`);
      loadFlights(); // Refresh the list
    });

    return () => {
      socket.off('flight_status_updated');
    };
  };

  const loadData = async () => {
    setLoading(true);
    try {
      await Promise.all([loadFlights(), loadAirlines(), loadAirports()]);
    } catch (error: any) {
      toast.error('Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const loadFlights = async () => {
    try {
      const [pending, approved, rejected, inProgress, completed] = await Promise.all([
        flightService.getAllFlights({ status: FlightStatus.PENDING, per_page: 100 }),
        flightService.getAllFlights({ status: FlightStatus.APPROVED, per_page: 100 }),
        flightService.getAllFlights({ status: FlightStatus.REJECTED, per_page: 100 }),
        flightService.getAllFlights({ status: FlightStatus.IN_PROGRESS, per_page: 100 }),
        flightService.getAllFlights({ status: FlightStatus.COMPLETED, per_page: 100 }),
      ]);
      setFlights({
        pending: pending.data,
        approved: approved.data,
        rejected: rejected.data,
        in_progress: inProgress.data,
        completed: completed.data,
      });
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to load flights');
    }
  };

  const loadAirlines = async () => {
    try {
      const data = await airlineService.getAllAirlines();
      setAirlines(data);
    } catch (error) {
      toast.error('Failed to load airlines');
    }
  };

  const loadAirports = async () => {
    try {
      const data = await airportService.getAllAirports();
      setAirports(data);
    } catch (error) {
      toast.error('Failed to load airports');
    }
  };

  const handleCreateFlight = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);
    try {
      await flightService.createFlight(createFormData);
      toast.success('Flight created successfully! Pending admin approval.');
      closeCreateModal();
      loadFlights();
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Failed to create flight');
    } finally {
      setActionLoading(false);
    }
  };

  const closeCreateModal = () => {
    setShowCreateModal(false);
    setCreateFormData({
      flight_name: '',
      airline_id: 0,
      departure_airport_id: 0,
      arrival_airport_id: 0,
      departure_time: '',
      arrival_time: '',
      price: 0,
      total_seats: 0,
      flight_distance_km: 0,
      flight_duration: 0,
    });
  };

  const handleInputChange = (field: keyof CreateFlightDto, value: any) => {
    setCreateFormData((prev) => ({ ...prev, [field]: value }));
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

  const renderFlightCard = (flight: Flight) => {
    const isRejected = flight.status === FlightStatus.REJECTED;
    
    return (
      <div key={flight.flight_id} className="flight-card">
        <div className="flight-card-header">
          <h3>{flight.flight_name}</h3>
          <span className={`status-badge ${FlightStatusColors[flight.status]}`}>
            {FlightStatusLabels[flight.status]}
          </span>
        </div>

        <div className="flight-card-body">
          <div className="flight-route">
            <div className="airport">
              <span className="airport-code">
                {flight.departure_airport?.airport_code || 'N/A'}
              </span>
              <span className="airport-name">
                {flight.departure_airport?.city || 'Unknown'}
              </span>
            </div>
            <div className="flight-arrow">→</div>
            <div className="airport">
              <span className="airport-code">
                {flight.arrival_airport?.airport_code || 'N/A'}
              </span>
              <span className="airport-name">
                {flight.arrival_airport?.city || 'Unknown'}
              </span>
            </div>
          </div>

          <div className="flight-details">
            <div className="detail-item">
              <span className="detail-label">Airline:</span>
              <span className="detail-value">
                {flight.airline?.airline_name || `#${flight.airline_id}`}
              </span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Departure:</span>
              <span className="detail-value">{formatDateTime(flight.departure_time)}</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Duration:</span>
              <span className="detail-value">{flight.flight_duration} min</span>
            </div>
            <div className="detail-item">
              <span className="detail-label">Price:</span>
              <span className="detail-value">${flight.price}</span>
            </div>
          </div>

          {isRejected && flight.rejection_reason && (
            <div className="rejection-reason">
              <strong>Rejection Reason:</strong>
              <p>{flight.rejection_reason}</p>
            </div>
          )}
        </div>

        {isRejected && (
          <div className="flight-card-actions">
            <button className="btn btn-primary" onClick={() => toast.info('Edit functionality coming soon')}>
              Edit & Resubmit
            </button>
          </div>
        )}
      </div>
    );
  };

  return (
    <div className="manager-dashboard">
      <div className="dashboard-header">
        <div>
          <h1>Manager Dashboard</h1>
          <p>Manage your flights</p>
        </div>
        <button className="btn btn-primary" onClick={() => setShowCreateModal(true)}>
          + Create Flight
        </button>
      </div>

      <div className="dashboard-tabs">
        <button
          className={`tab-button ${activeTab === 'pending' ? 'active' : ''}`}
          onClick={() => setActiveTab('pending')}
        >
          Pending
          {flights.pending.length > 0 && <span className="badge">{flights.pending.length}</span>}
        </button>
        <button
          className={`tab-button ${activeTab === 'approved' ? 'active' : ''}`}
          onClick={() => setActiveTab('approved')}
        >
          Approved
          {flights.approved.length > 0 && <span className="badge">{flights.approved.length}</span>}
        </button>
        <button
          className={`tab-button ${activeTab === 'rejected' ? 'active' : ''}`}
          onClick={() => setActiveTab('rejected')}
        >
          Rejected
          {flights.rejected.length > 0 && <span className="badge">{flights.rejected.length}</span>}
        </button>
        <button
          className={`tab-button ${activeTab === 'in_progress' ? 'active' : ''}`}
          onClick={() => setActiveTab('in_progress')}
        >
          In Progress
          {flights.in_progress.length > 0 && <span className="badge">{flights.in_progress.length}</span>}
        </button>
        <button
          className={`tab-button ${activeTab === 'completed' ? 'active' : ''}`}
          onClick={() => setActiveTab('completed')}
        >
          Completed
          {flights.completed.length > 0 && <span className="badge">{flights.completed.length}</span>}
        </button>
      </div>

      <div className="dashboard-content">
        {loading ? (
          <div className="loading-container">
            <div className="spinner"></div>
            <p>Loading flights...</p>
          </div>
        ) : (
          <div className="flights-grid">
            {flights[activeTab].length === 0 ? (
              <div className="empty-state">
                <p>No {activeTab.replace('_', ' ')} flights</p>
              </div>
            ) : (
              flights[activeTab].map((flight) => renderFlightCard(flight))
            )}
          </div>
        )}
      </div>

      {/* Create Flight Modal */}
      {showCreateModal && (
        <div className="modal-overlay" onClick={closeCreateModal}>
          <div className="modal-content modal-large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Create New Flight</h2>
              <button className="modal-close" onClick={closeCreateModal}>
                ×
              </button>
            </div>
            <form onSubmit={handleCreateFlight}>
              <div className="modal-body">
                <div className="form-grid">
                  <div className="form-group">
                    <label>Flight Name</label>
                    <input
                      type="text"
                      className="form-input"
                      value={createFormData.flight_name}
                      onChange={(e) => handleInputChange('flight_name', e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Airline</label>
                    <select
                      className="form-input"
                      value={createFormData.airline_id}
                      onChange={(e) => handleInputChange('airline_id', Number(e.target.value))}
                      required
                    >
                      <option value={0}>Select Airline</option>
                      {airlines.map((airline) => (
                        <option key={airline.airline_id} value={airline.airline_id}>
                          {airline.airline_name} ({airline.airline_code})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Departure Airport</label>
                    <select
                      className="form-input"
                      value={createFormData.departure_airport_id}
                      onChange={(e) => handleInputChange('departure_airport_id', Number(e.target.value))}
                      required
                    >
                      <option value={0}>Select Airport</option>
                      {airports.map((airport) => (
                        <option key={airport.airport_id} value={airport.airport_id}>
                          {airport.airport_name} ({airport.airport_code})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Arrival Airport</label>
                    <select
                      className="form-input"
                      value={createFormData.arrival_airport_id}
                      onChange={(e) => handleInputChange('arrival_airport_id', Number(e.target.value))}
                      required
                    >
                      <option value={0}>Select Airport</option>
                      {airports.map((airport) => (
                        <option key={airport.airport_id} value={airport.airport_id}>
                          {airport.airport_name} ({airport.airport_code})
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="form-group">
                    <label>Departure Time</label>
                    <input
                      type="datetime-local"
                      className="form-input"
                      value={createFormData.departure_time}
                      onChange={(e) => handleInputChange('departure_time', e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Arrival Time</label>
                    <input
                      type="datetime-local"
                      className="form-input"
                      value={createFormData.arrival_time}
                      onChange={(e) => handleInputChange('arrival_time', e.target.value)}
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Price ($)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={createFormData.price || ''}
                      onChange={(e) => handleInputChange('price', Number(e.target.value))}
                      min="0"
                      step="0.01"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Total Seats</label>
                    <input
                      type="number"
                      className="form-input"
                      value={createFormData.total_seats || ''}
                      onChange={(e) => handleInputChange('total_seats', Number(e.target.value))}
                      min="1"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Distance (km)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={createFormData.flight_distance_km || ''}
                      onChange={(e) => handleInputChange('flight_distance_km', Number(e.target.value))}
                      min="0"
                      required
                    />
                  </div>

                  <div className="form-group">
                    <label>Duration (minutes)</label>
                    <input
                      type="number"
                      className="form-input"
                      value={createFormData.flight_duration || ''}
                      onChange={(e) => handleInputChange('flight_duration', Number(e.target.value))}
                      min="0"
                      required
                    />
                  </div>
                </div>
              </div>
              <div className="modal-actions">
                <button type="button" className="btn btn-secondary" onClick={closeCreateModal}>
                  Cancel
                </button>
                <button type="submit" className="btn btn-primary" disabled={actionLoading}>
                  {actionLoading ? 'Creating...' : 'Create Flight'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
