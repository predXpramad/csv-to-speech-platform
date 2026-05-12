import React, { useState } from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { stopConversion } from '@/services/api';

export const ProgressDashboard = () => {
  const { job } = useAppStore();
  const [stopping, setStopping] = useState(false);
  
  if (!job) return null;

  const handleStop = async () => {
    try {
      setStopping(true);
      await stopConversion(job.jobId);
    } catch (e) {
      console.error(e);
      setStopping(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Conversion Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Status: <span className="font-semibold capitalize">{stopping ? 'Stopping...' : job.status}</span></span>
            <span>{job.progress}% ({job.processedRows}/{job.totalRows})</span>
          </div>
          <div className="h-2 w-full bg-secondary overflow-hidden rounded-full">
            <div className="h-full bg-primary transition-all duration-500" style={{ width: `${job.progress}%` }} />
          </div>
          {job.failedRows.length > 0 && (
            <div className="mt-4 text-sm text-destructive">
              Failed rows: {job.failedRows.length}
            </div>
          )}
          
          {job.status === 'processing' && (
            <div className="pt-4">
              <Button 
                variant="destructive" 
                className="w-full" 
                onClick={handleStop}
                disabled={stopping}
              >
                {stopping ? 'Stopping...' : 'Stop & Download Early'}
              </Button>
            </div>
          )}
          
          {job.status === 'completed' && (
            <div className="pt-4">
              <Button 
                variant="outline" 
                className="w-full" 
                onClick={() => {
                  if (window.confirm("Are you sure you want to discard this job and start a new conversion?")) {
                    useAppStore.getState().resetApp();
                  }
                }}
              >
                Start New Conversion
              </Button>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};
