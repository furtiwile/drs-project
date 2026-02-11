export const FlightStatus = {
  PENDING: 'PENDING',
  APPROVED: 'APPROVED',
  REJECTED: 'REJECTED',
  IN_PROGRESS: 'IN_PROGRESS',
  CANCELLED: 'CANCELLED',
  COMPLETED: 'COMPLETED',
} as const;

export type FlightStatus = typeof FlightStatus[keyof typeof FlightStatus];

export const FlightStatusLabels: Record<string, string> = {
  'PENDING': 'Pending Approval',
  'APPROVED': 'Approved',
  'REJECTED': 'Rejected',
  'IN_PROGRESS': 'In Progress',
  'CANCELLED': 'Cancelled',
  'COMPLETED': 'Completed',
};

export const FlightStatusColors: Record<string, string> = {
  'PENDING': 'text-yellow-400',
  'APPROVED': 'text-green-400',
  'REJECTED': 'text-red-400',
  'IN_PROGRESS': 'text-blue-400',
  'CANCELLED': 'text-gray-400',
  'COMPLETED': 'text-purple-400',
};
