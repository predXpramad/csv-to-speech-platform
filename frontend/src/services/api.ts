import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export const getVoices = async () => {
  const res = await api.get('/voices');
  const data = res.data;
  const flatVoices: any[] = [];
  if (data.languages) {
    data.languages.forEach((lang: any) => {
      lang.voices.forEach((voice: any) => {
        flatVoices.push({
          Name: voice.display_name,
          ShortName: voice.voice_name,
          Gender: voice.gender,
          Locale: lang.locale
        });
      });
    });
  } else {
    return data;
  }
  return flatVoices;
};

export const uploadCsv = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload', formData);
  return res.data;
};

export const startConversion = async (jobId: string, textCol: string, voice: string, startRow?: number, endRow?: number) => {
  const payload: any = { jobId, textCol, voice };
  if (startRow) payload.startRow = startRow;
  if (endRow) payload.endRow = endRow;
  const res = await api.post('/convert', payload);
  return res.data;
};

export const stopConversion = async (jobId: string) => {
  const res = await api.post(`/stop/${jobId}`);
  return res.data;
};

export const deleteJob = async (jobId: string) => {
  const res = await api.delete(`/download/${jobId}`);
  return res.data;
};
