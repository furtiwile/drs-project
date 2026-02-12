// Report Service following Clean Architecture and SOLID principles
// Single Responsibility: Managing all report-related API calls
// Uses Bearer token authentication from localStorage

import axios from 'axios';
import type { GenerateReportRequest, ReportType } from '../../domain/dtos/ReportDtos';

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://metro.proxy.rlwy.net:12922";
const API_PREFIX = import.meta.env.VITE_API_PREFIX || '/api/v1';
const API_URL = `${API_BASE_URL}${API_PREFIX}`;

/**
 * Service for managing reports (admin only)
 * Follows Interface Segregation Principle - only exposes report-related methods
 * Uses Bearer token authentication as per server specification
 */
class ReportService {
  private basePath = '/reports';

  /**
   * Generate PDF report for flights (admin only)
   * Uses Bearer token authentication from localStorage
   * This returns a PDF blob that can be downloaded
   */
  async generateFlightReport(reportTypes: ReportType[]): Promise<Blob> {
    const payload: GenerateReportRequest = {
      report_types: reportTypes,
    };

    try {
      const token = this.getAuthToken();
      const response = await axios.post(
        `${API_URL}${this.basePath}/flights`,
        payload,
        {
          responseType: 'blob',
          headers: {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
          },
        }
      );

      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Generate and download a report for a specific report type
   * Convenience method used by AdminDashboard
   */
  async generateReport(reportType: ReportType): Promise<void> {
    const blob = await this.generateFlightReport([reportType]);
    const filename = this.generateFilename([reportType]);
    this.downloadPDF(blob, filename);
  }

  /**
   * Helper method to download PDF
   * Automatically downloads the PDF to the user's device
   */
  downloadPDF(blob: Blob, filename: string): void {
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    window.URL.revokeObjectURL(url);
  }

  /**
   * Helper method to generate filename with timestamp
   */
  generateFilename(reportTypes: ReportType[], extension: string = 'pdf'): string {
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').split('T')[0];
    const types = reportTypes.join('_');
    return `flight_report_${types}_${timestamp}.${extension}`;
  }

  /**
   * Helper method to get authentication token from localStorage
   */
  private getAuthToken(): string {
    const token = localStorage.getItem('token');
    if (!token) {
      throw new Error('User not authenticated');
    }
    return token;
  }
}

// Export singleton instance following Singleton pattern
export const reportService = new ReportService();
