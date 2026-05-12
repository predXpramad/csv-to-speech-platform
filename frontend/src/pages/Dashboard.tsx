import React, { useEffect } from 'react';
import { UploadZone } from '@/components/features/tts/UploadZone';
import { ConversionForm } from '@/components/features/tts/ConversionForm';
import { ProgressDashboard } from '@/components/features/tts/ProgressDashboard';
import { DownloadCard } from '@/components/features/tts/DownloadCard';
import { useAppStore } from '@/store/useAppStore';
import { getVoices } from '@/services/api';

export const Dashboard = () => {
  const { file, job, setVoices } = useAppStore();

  useEffect(() => {
    getVoices().then(setVoices).catch(console.error);
  }, []);

  return (
    <div className="space-y-8 pb-12 animate-in fade-in duration-500">
      <div className="text-center space-y-2 mt-8">
        <h2 className="text-3xl font-bold tracking-tight">Batch Convert CSV to Audio</h2>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Upload your dataset, select your target column and preferred voice, and we'll generate speech audio for every row instantly.
        </p>
      </div>

      {!file && !job && <UploadZone />}
      
      {file && job?.status === 'pending' && <ConversionForm />}
      
      {(job?.status === 'processing' || job?.status === 'completed') && (
        <ProgressDashboard />
      )}
      
      {job?.status === 'completed' && <DownloadCard />}
    </div>
  );
};
