import { useAppStore } from '../store/useAppStore';

let ws: WebSocket | null = null;

export const connectWebSocket = (jobId: string) => {
  if (ws) {
    ws.close();
  }

  const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
  // Use current host for proxy setup
  const wsUrl = `${protocol}//${window.location.host}/ws/progress/${jobId}`;
  
  ws = new WebSocket(wsUrl);

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    useAppStore.getState().updateJobProgress({
      status: data.status,
      progress: data.progress,
      processedRows: data.processedRows,
      failedRows: data.failedRows || []
    });
  };

  ws.onerror = (error) => {
    console.error('WebSocket Error:', error);
  };
  
  ws.onclose = () => {
    console.log('WebSocket connection closed');
  }
};

export const disconnectWebSocket = () => {
  if (ws) {
    ws.close();
    ws = null;
  }
};
