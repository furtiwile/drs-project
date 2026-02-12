// DTOs for Report operations
// Following SOLID principles - Data Transfer Objects for reports

export interface GenerateReportRequest {
  report_types: ('upcoming' | 'in_progress' | 'completed')[];
}

export interface ReportResponse {
  pdf_url: string;
  filename: string;
  generated_at: string;
  report_types: string[];
}

export const VALID_REPORT_TYPES = ['upcoming', 'in_progress', 'completed'] as const;
export type ReportType = typeof VALID_REPORT_TYPES[number];
