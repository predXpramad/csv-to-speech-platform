export interface Job {
  jobId: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
  progress: number;
  totalRows: number;
  processedRows: number;
  failedRows: FailedRow[];
  downloadUrl?: string;
  expiresAt?: string;
}

export interface FailedRow {
  row: number;
  error: string;
}

export interface Voice {
  Name: string;
  ShortName: string;
  Gender: string;
  Locale: string;
}
