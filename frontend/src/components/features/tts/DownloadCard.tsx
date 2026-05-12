import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Trash } from 'lucide-react';
import { deleteJob } from '@/services/api';

export const DownloadCard = () => {
  const { job, setJob, setFile } = useAppStore();
  if (!job || job.status !== 'completed') return null;

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete these files permanently? This cannot be undone.")) return;
    
    try {
      await deleteJob(job.jobId);
      useAppStore.getState().resetApp();
    } catch(err) {
      console.error(err);
      alert("Failed to delete job files from server.");
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8 bg-primary/5 border-primary/20">
      <CardHeader>
        <CardTitle className="text-primary">Conversion Complete!</CardTitle>
      </CardHeader>
      <CardContent className="flex gap-4">
        <Button className="flex-1" onClick={() => window.location.href = `/api/download/${job.jobId}`}>
          <Download className="mr-2 h-4 w-4" /> Download ZIP
        </Button>
        <Button variant="destructive" onClick={handleDelete}>
          <Trash className="mr-2 h-4 w-4" /> Delete
        </Button>
      </CardContent>
    </Card>
  );
};
