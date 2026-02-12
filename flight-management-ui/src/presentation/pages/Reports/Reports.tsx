import React, { useState, useEffect } from 'react';
import { reportService } from '../../../infrastructure/services/reportService';
import { useToast } from '../../../application/context/ToastContext';
import { useAuth } from '../../../application/context/AuthContext';
import { Role } from '../../../domain/enums/Role';
import type { ReportType } from '../../../domain/dtos/ReportDtos';
import './Reports.css';

interface ReportHistory {
  id: string;
  types: ReportType[];
  generatedAt: Date;
  filename: string;
}

/**
 * Reports Page - Admin-only page for generating PDF reports
 * Follows Single Responsibility Principle - only manages report generation
 * Uses dependency injection for services
 */
export const Reports: React.FC = () => {
  const [selectedReports, setSelectedReports] = useState<Set<ReportType>>(new Set(['upcoming']));
  const [loading, setLoading] = useState(false);
  const [reportHistory, setReportHistory] = useState<ReportHistory[]>([]);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  const toast = useToast();
  const { user } = useAuth();

  // Check if user is admin
  useEffect(() => {
    if (user && user.role !== Role.ADMINISTRATOR) {
      toast.error('You do not have permission to access this page');
    }
  }, [user, toast]);

  const toggleReportType = (reportType: ReportType) => {
    const newSelected = new Set(selectedReports);
    if (newSelected.has(reportType)) {
      newSelected.delete(reportType);
    } else {
      newSelected.add(reportType);
    }
    setSelectedReports(newSelected);
  };

  const handleClearSelection = () => {
    setSelectedReports(new Set());
  };

  const handleGenerateReport = async () => {
    if (selectedReports.size === 0) {
      toast.error('Please select at least one report type');
      return;
    }

    setLoading(true);
    setSuccessMessage(null);
    setErrorMessage(null);

    try {
      const reportTypes = Array.from(selectedReports) as ReportType[];
      const pdfBlob = await reportService.generateFlightReport(reportTypes);

      // Generate filename
      const filename = reportService.generateFilename(reportTypes);

      // Download the PDF
      reportService.downloadPDF(pdfBlob, filename);

      // Add to history
      const newReport: ReportHistory = {
        id: Date.now().toString(),
        types: reportTypes,
        generatedAt: new Date(),
        filename,
      };

      setReportHistory([newReport, ...reportHistory]);
      setSuccessMessage(`Report "${filename}" generated successfully!`);
      toast.success('Report generated and downloaded successfully!');

      // Clear selection after successful generation
      setSelectedReports(new Set());
    } catch (error: any) {
      const errorMsg = error.response?.data?.message || 'Failed to generate report';
      setErrorMessage(errorMsg);
      toast.error(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (date: Date) => {
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const reportDescriptions: Record<ReportType, string> = {
    upcoming: 'Flights scheduled to depart in the future',
    in_progress: 'Flights currently in progress',
    completed: 'Completed and cancelled flights',
  };

  const reportIcons: Record<ReportType, string> = {
    upcoming: '🛫',
    in_progress: '✈️',
    completed: '🛬',
  };

  return (
    <div className="reports-container">
      {/* Header */}
      <div className="reports-header">
        <h1 className="reports-title">Reports & Analytics</h1>
        <p className="reports-subtitle">
          Generate PDF reports for flight management and analysis
        </p>
      </div>

      {/* Messages */}
      {successMessage && (
        <div className="success-message">
          <span>✓ {successMessage}</span>
          <button
            className="close-btn"
            onClick={() => setSuccessMessage(null)}
          >
            ✕
          </button>
        </div>
      )}

      {errorMessage && (
        <div className="error-message">
          <span>✕ {errorMessage}</span>
          <button
            className="close-btn"
            onClick={() => setErrorMessage(null)}
          >
            ✕
          </button>
        </div>
      )}

      {/* Report Cards Overview */}
      <div className="reports-grid">
        {(Object.keys(reportDescriptions) as ReportType[]).map((type) => (
          <div key={type} className={`report-card ${type}`}>
            <div className="report-card-icon">{reportIcons[type]}</div>
            <h3 className="report-card-title">{type.replace('_', ' ')}</h3>
            <p className="report-card-description">{reportDescriptions[type]}</p>
          </div>
        ))}
      </div>

      {/* Report Selection & Generation */}
      <div className="select-report-section">
        <h2 className="section-title">Generate Custom Report</h2>

        <div className="report-checkboxes">
          {(Object.keys(reportDescriptions) as ReportType[]).map((type) => (
            <div key={type}>
              <div className="checkbox-group">
                <input
                  type="checkbox"
                  id={`report-${type}`}
                  checked={selectedReports.has(type)}
                  onChange={() => toggleReportType(type)}
                />
                <label htmlFor={`report-${type}`} className="checkbox-label">
                  {type.replace('_', ' ').charAt(0).toUpperCase() +
                    type.replace('_', ' ').slice(1)}
                </label>
              </div>
              <span className="checkbox-description">{reportDescriptions[type]}</span>
            </div>
          ))}
        </div>

        <div className="action-buttons">
          <button
            className="generate-btn"
            onClick={handleGenerateReport}
            disabled={loading || selectedReports.size === 0}
          >
            {loading ? (
              <>
                <div className="spinner"></div>
                Generating...
              </>
            ) : (
              <>📥 Generate Report</>
            )}
          </button>
          <button
            className="clear-btn"
            onClick={handleClearSelection}
            disabled={loading || selectedReports.size === 0}
          >
            Clear Selection
          </button>
        </div>
      </div>

      {/* Report History */}
      <div className="report-history">
        <h2 className="section-title">Generated Reports</h2>

        {reportHistory.length === 0 ? (
          <div className="report-history-empty">
            No reports generated yet. Create one above to get started!
          </div>
        ) : (
          <div className="report-list">
            {reportHistory.map((report) => (
              <div key={report.id} className="report-item">
                <div className="report-item-info">
                  <p className="report-item-title">{report.filename}</p>
                  <p className="report-item-date">
                    Generated: {formatDate(report.generatedAt)}
                  </p>
                  <div className="report-item-types">
                    {report.types.map((type) => (
                      <span key={type} className="report-type-badge">
                        {type.replace('_', ' ')}
                      </span>
                    ))}
                  </div>
                </div>
                <button
                  className="download-btn"
                  onClick={() => {
                    toast.info('Report file should be in your downloads folder');
                  }}
                >
                  ↓ Downloaded
                </button>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Reports;
