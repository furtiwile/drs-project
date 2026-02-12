import { apiClient } from '../api/apiClient';

class ReportService {
  private basePath = '/reports/flights';

  async generateReport(activeTab: string): Promise<void> {
    await apiClient.post(this.basePath, {"report_types": [activeTab]});
  }

}

export const reportService = new ReportService();
