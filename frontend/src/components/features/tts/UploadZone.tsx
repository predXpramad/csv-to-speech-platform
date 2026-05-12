import React, { useState } from 'react';
import { UploadCloud } from 'lucide-react';
import { useAppStore } from '@/store/useAppStore';
import { uploadCsv } from '@/services/api';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';

export const UploadZone = () => {
  const { setFile, setHeaders, setJob } = useAppStore();
  const [isLoading, setIsLoading] = useState(false);

  const handleUpload = async (file: File) => {
    if (file.type !== 'text/csv' && !file.name.endsWith('.csv')) {
      alert('Please upload a valid CSV file.');
      return;
    }
    
    setIsLoading(true);
    try {
      const data = await uploadCsv(file);
      setFile(file);
      setHeaders(data.headers);
      setJob({
        jobId: data.jobId || data.file_id,
        status: 'pending',
        progress: 0,
        totalRows: data.totalRows || data.row_count,
        processedRows: 0,
        failedRows: []
      });
    } catch (err) {
      console.error(err);
      alert('Upload failed');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8 border-dashed border-2 bg-muted/20">
      <CardContent className="p-12 flex flex-col items-center justify-center text-center">
        <UploadCloud className="w-12 h-12 text-muted-foreground mb-4" />
        <h3 className="text-xl font-semibold mb-2">Upload your CSV</h3>
        <p className="text-muted-foreground mb-6">Drag and drop your file here, or click to browse.</p>
        <div className="relative">
          <Button disabled={isLoading}>{isLoading ? 'Uploading...' : 'Select File'}</Button>
          <input 
            type="file" 
            accept=".csv"
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            onChange={(e) => e.target.files && handleUpload(e.target.files[0])}
            disabled={isLoading}
          />
        </div>
      </CardContent>
    </Card>
  );
};
