import { create } from 'zustand'
import { Job, Voice } from '../types'

interface AppState {
  file: File | null;
  headers: string[];
  setFile: (file: File | null) => void;
  setHeaders: (headers: string[]) => void;
  
  voices: Voice[];
  setVoices: (voices: Voice[]) => void;
  
  selectedTextCol: string;
  setSelectedTextCol: (col: string) => void;
  
  selectedVoice: string;
  setSelectedVoice: (voice: string) => void;
  
  selectedLanguage: string;
  setSelectedLanguage: (lang: string) => void;
  
  job: Job | null;
  setJob: (job: Job | null) => void;
  updateJobProgress: (progress: Partial<Job>) => void;
  
  resetApp: () => void;
}

export const useAppStore = create<AppState>((set) => ({
  file: null,
  headers: [],
  setFile: (file) => set({ file }),
  setHeaders: (headers) => set({ headers }),
  
  voices: [],
  setVoices: (voices) => set({ voices }),
  
  selectedTextCol: '',
  setSelectedTextCol: (col) => set({ selectedTextCol: col }),
  
  selectedVoice: '',
  setSelectedVoice: (voice) => set({ selectedVoice: voice }),
  
  selectedLanguage: '',
  setSelectedLanguage: (lang) => set({ selectedLanguage: lang, selectedVoice: '' }),
  
  job: null,
  setJob: (job) => set({ job }),
  updateJobProgress: (progress) => set((state) => ({
    job: state.job ? { ...state.job, ...progress } : null
  })),
  
  resetApp: () => set({
    file: null,
    headers: [],
    selectedTextCol: '',
    selectedLanguage: '',
    selectedVoice: '',
    job: null
  })
}))
