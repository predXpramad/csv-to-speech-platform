import React, { useMemo, useState, useEffect } from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { startConversion } from '@/services/api';
import { connectWebSocket } from '@/services/websocket';

export const ConversionForm = () => {
  const { 
    headers, 
    voices, 
    selectedTextCol, 
    setSelectedTextCol, 
    selectedLanguage, 
    setSelectedLanguage, 
    selectedVoice, 
    setSelectedVoice, 
    job 
  } = useAppStore();

  const [startRow, setStartRow] = useState<number>(1);
  const [endRow, setEndRow] = useState<number>(0);

  useEffect(() => {
    if (job?.totalRows) {
      setEndRow(job.totalRows);
    }
  }, [job?.totalRows]);

  const languages = useMemo(() => {
    return Array.from(new Set(voices.map(v => v.Locale))).sort();
  }, [voices]);

  const filteredVoices = useMemo(() => {
    return voices.filter(v => v.Locale === selectedLanguage);
  }, [voices, selectedLanguage]);

  const handleStart = async () => {
    if (!job || !selectedTextCol || !selectedVoice) return;
    
    try {
      await startConversion(job.jobId, selectedTextCol, selectedVoice, startRow, endRow);
      connectWebSocket(job.jobId);
    } catch (err) {
      console.error(err);
      alert('Failed to start conversion');
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Configuration</CardTitle>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="space-y-2">
          <label className="text-sm font-medium">Text Column</label>
          <select 
            className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedTextCol} 
            onChange={(e) => setSelectedTextCol(e.target.value)}
          >
            <option value="">Select column...</option>
            {headers.map(h => <option key={h} value={h}>{h}</option>)}
          </select>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div className="space-y-2">
            <label className="text-sm font-medium">Start Row</label>
            <input 
              type="number"
              min={1}
              max={job?.totalRows || 1}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              value={startRow}
              onChange={(e) => setStartRow(Number(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium">End Row</label>
            <input 
              type="number"
              min={1}
              max={job?.totalRows || 1}
              className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
              value={endRow}
              onChange={(e) => setEndRow(Number(e.target.value))}
            />
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium">Language</label>
          <select 
            className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedLanguage} 
            onChange={(e) => setSelectedLanguage(e.target.value)}
          >
            <option value="">Select language...</option>
            {languages.map(lang => <option key={lang} value={lang}>{lang}</option>)}
          </select>
        </div>

        {selectedLanguage && (
          <div className="space-y-2 animate-in fade-in slide-in-from-top-2">
            <label className="text-sm font-medium">Voice</label>
            <select 
              className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
              value={selectedVoice} 
              onChange={(e) => setSelectedVoice(e.target.value)}
            >
              <option value="">Select voice...</option>
              {filteredVoices.map(v => (
                <option key={v.ShortName} value={v.ShortName}>
                  {v.Name} ({v.Gender}) {v.ShortName.toLowerCase().includes('neural') ? '[Neural]' : ''}
                </option>
              ))}
            </select>
          </div>
        )}

        <Button 
          className="w-full" 
          disabled={!selectedTextCol || !selectedVoice}
          onClick={handleStart}
        >
          Start Conversion
        </Button>
      </CardContent>
    </Card>
  );
};
