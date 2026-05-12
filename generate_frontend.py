import os

base_dir = r"d:\02 Projects\TTS ML Model\frontend"

files = {}

files["package.json"] = """{
  "name": "csv-to-speech-frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
    "preview": "vite preview"
  },
  "dependencies": {
    "@hookform/resolvers": "^3.3.4",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-label": "^2.0.2",
    "@radix-ui/react-progress": "^1.0.3",
    "@radix-ui/react-select": "^2.0.0",
    "@radix-ui/react-slider": "^1.1.2",
    "@radix-ui/react-slot": "^1.0.2",
    "@radix-ui/react-toast": "^1.1.5",
    "axios": "^1.6.8",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "date-fns": "^3.6.0",
    "lucide-react": "^0.368.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-hook-form": "^7.51.2",
    "react-router-dom": "^6.22.3",
    "tailwind-merge": "^2.2.2",
    "tailwindcss-animate": "^1.0.7",
    "zod": "^3.22.4",
    "zustand": "^4.5.2"
  },
  "devDependencies": {
    "@types/node": "^20.12.5",
    "@types/react": "^18.2.74",
    "@types/react-dom": "^18.2.24",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.19",
    "postcss": "^8.4.38",
    "tailwindcss": "^3.4.3",
    "typescript": "^5.4.4",
    "vite": "^5.2.8"
  }
}
"""

files["vite.config.ts"] = """import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
})
"""

files["tsconfig.json"] = """{
  "compilerOptions": {
    "target": "ES2020",
    "useDefineForClassFields": true,
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "skipLibCheck": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    },
    "moduleResolution": "bundler",
    "allowImportingTsExtensions": true,
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "jsx": "react-jsx",
    "strict": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  },
  "include": ["src"]
}
"""

files["postcss.config.js"] = """export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
"""

files["tailwind.config.js"] = """/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: [
    './index.html',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    container: {
      center: true,
      padding: "2rem",
      screens: {
        "2xl": "1400px",
      },
    },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
}
"""

files["src/styles/globals.css"] = """@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --popover: 0 0% 100%;
    --popover-foreground: 222.2 84% 4.9%;
    --primary: 221.2 83.2% 53.3%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 221.2 83.2% 53.3%;
    --radius: 0.5rem;
  }

  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --card: 222.2 84% 4.9%;
    --card-foreground: 210 40% 98%;
    --popover: 222.2 84% 4.9%;
    --popover-foreground: 210 40% 98%;
    --primary: 217.2 91.2% 59.8%;
    --primary-foreground: 222.2 47.4% 11.2%;
    --secondary: 217.2 32.6% 17.5%;
    --secondary-foreground: 210 40% 98%;
    --muted: 217.2 32.6% 17.5%;
    --muted-foreground: 215 20.2% 65.1%;
    --accent: 217.2 32.6% 17.5%;
    --accent-foreground: 210 40% 98%;
    --destructive: 0 62.8% 30.6%;
    --destructive-foreground: 210 40% 98%;
    --border: 217.2 32.6% 17.5%;
    --input: 217.2 32.6% 17.5%;
    --ring: 212.7 26.8% 83.9%;
  }
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground;
  }
}
"""

files["index.html"] = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSV to Speech Platform</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
"""

files["src/lib/utils.ts"] = """import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
"""

files["src/types/index.ts"] = """export interface Job {
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
"""

files["src/store/useAppStore.ts"] = """import { create } from 'zustand'
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
  
  job: Job | null;
  setJob: (job: Job | null) => void;
  updateJobProgress: (progress: Partial<Job>) => void;
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
  
  job: null,
  setJob: (job) => set({ job }),
  updateJobProgress: (progress) => set((state) => ({
    job: state.job ? { ...state.job, ...progress } : null
  }))
}))
"""

files["src/services/api.ts"] = """import axios from 'axios';

const api = axios.create({
  baseURL: '/api',
});

export const getVoices = async () => {
  const res = await api.get('/voices');
  return res.data;
};

export const uploadCsv = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await api.post('/upload', formData);
  return res.data;
};

export const startConversion = async (jobId: string, textCol: string, voice: string) => {
  const res = await api.post('/convert', { jobId, textCol, voice });
  return res.data;
};

export const deleteJob = async (jobId: string) => {
  const res = await api.delete(`/download/${jobId}`);
  return res.data;
};
"""

files["src/services/websocket.ts"] = """import { useAppStore } from '../store/useAppStore';

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
"""

files["src/providers/ThemeProvider.tsx"] = """import { createContext, useContext, useEffect, useState } from "react"

type Theme = "dark" | "light" | "system"

type ThemeProviderProps = {
  children: React.ReactNode
  defaultTheme?: Theme
  storageKey?: string
}

type ThemeProviderState = {
  theme: Theme
  setTheme: (theme: Theme) => void
}

const initialState: ThemeProviderState = {
  theme: "system",
  setTheme: () => null,
}

const ThemeProviderContext = createContext<ThemeProviderState>(initialState)

export function ThemeProvider({
  children,
  defaultTheme = "system",
  storageKey = "vite-ui-theme",
  ...props
}: ThemeProviderProps) {
  const [theme, setTheme] = useState<Theme>(
    () => (localStorage.getItem(storageKey) as Theme) || defaultTheme
  )

  useEffect(() => {
    const root = window.document.documentElement

    root.classList.remove("light", "dark")

    if (theme === "system") {
      const systemTheme = window.matchMedia("(prefers-color-scheme: dark)")
        .matches
        ? "dark"
        : "light"

      root.classList.add(systemTheme)
      return
    }

    root.classList.add(theme)
  }, [theme])

  const value = {
    theme,
    setTheme: (theme: Theme) => {
      localStorage.setItem(storageKey, theme)
      setTheme(theme)
    },
  }

  return (
    <ThemeProviderContext.Provider {...props} value={value}>
      {children}
    </ThemeProviderContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeProviderContext)
  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")
  return context
}
"""

files["src/components/ui/button.tsx"] = """import * as React from "react"
import { Slot } from "@radix-ui/react-slot"
import { cva, type VariantProps } from "class-variance-authority"
import { cn } from "@/lib/utils"

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-primary text-primary-foreground hover:bg-primary/90",
        destructive: "bg-destructive text-destructive-foreground hover:bg-destructive/90",
        outline: "border border-input bg-background hover:bg-accent hover:text-accent-foreground",
        secondary: "bg-secondary text-secondary-foreground hover:bg-secondary/80",
        ghost: "hover:bg-accent hover:text-accent-foreground",
        link: "text-primary underline-offset-4 hover:underline",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  }
)

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant, size, asChild = false, ...props }, ref) => {
    const Comp = asChild ? Slot : "button"
    return (
      <Comp
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref}
        {...props}
      />
    )
  }
)
Button.displayName = "Button"

export { Button, buttonVariants }
"""

files["src/components/ui/card.tsx"] = """import * as React from "react"
import { cn } from "@/lib/utils"

const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("rounded-lg border bg-card text-card-foreground shadow-sm", className)} {...props} />
  )
)
Card.displayName = "Card"

const CardHeader = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("flex flex-col space-y-1.5 p-6", className)} {...props} />
  )
)
CardHeader.displayName = "CardHeader"

const CardTitle = React.forwardRef<HTMLParagraphElement, React.HTMLAttributes<HTMLHeadingElement>>(
  ({ className, ...props }, ref) => (
    <h3 ref={ref} className={cn("text-2xl font-semibold leading-none tracking-tight", className)} {...props} />
  )
)
CardTitle.displayName = "CardTitle"

const CardContent = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className, ...props }, ref) => (
    <div ref={ref} className={cn("p-6 pt-0", className)} {...props} />
  )
)
CardContent.displayName = "CardContent"

export { Card, CardHeader, CardTitle, CardContent }
"""

files["src/components/features/tts/UploadZone.tsx"] = """import React, { useState } from 'react';
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
      // Mock Data temporarily for demo if backend is not ready
      // const data = await uploadCsv(file);
      const data = { headers: ['id', 'text', 'speaker'], jobId: 'job-123', totalRows: 15 };
      
      setFile(file);
      setHeaders(data.headers);
      setJob({
        jobId: data.jobId,
        status: 'pending',
        progress: 0,
        totalRows: data.totalRows,
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
"""

files["src/components/features/tts/ConversionForm.tsx"] = """import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { startConversion } from '@/services/api';
import { connectWebSocket } from '@/services/websocket';

export const ConversionForm = () => {
  const { headers, voices, selectedTextCol, setSelectedTextCol, selectedVoice, setSelectedVoice, job, updateJobProgress } = useAppStore();

  const handleStart = async () => {
    if (!job || !selectedTextCol || !selectedVoice) return;
    
    try {
      // await startConversion(job.jobId, selectedTextCol, selectedVoice);
      // connectWebSocket(job.jobId);
      
      // Simulate progress for UI demo
      updateJobProgress({ status: 'processing', progress: 10, processedRows: 1 });
      setTimeout(() => updateJobProgress({ progress: 50, processedRows: 7 }), 1000);
      setTimeout(() => updateJobProgress({ progress: 100, processedRows: 15, status: 'completed' }), 2000);
      
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

        <div className="space-y-2">
          <label className="text-sm font-medium">Voice</label>
          <select 
            className="flex h-10 w-full items-center justify-between rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background"
            value={selectedVoice} 
            onChange={(e) => setSelectedVoice(e.target.value)}
          >
            <option value="">Select voice...</option>
            {voices.map(v => <option key={v.ShortName} value={v.ShortName}>{v.Name} ({v.Locale})</option>)}
          </select>
        </div>

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
"""

files["src/components/features/tts/ProgressDashboard.tsx"] = """import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';

export const ProgressDashboard = () => {
  const { job } = useAppStore();
  if (!job) return null;

  return (
    <Card className="w-full max-w-2xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Conversion Progress</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <div className="flex justify-between text-sm mb-1">
            <span>Status: <span className="font-semibold capitalize">{job.status}</span></span>
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
        </div>
      </CardContent>
    </Card>
  );
};
"""

files["src/components/features/tts/DownloadCard.tsx"] = """import React from 'react';
import { useAppStore } from '@/store/useAppStore';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Trash } from 'lucide-react';
import { deleteJob } from '@/services/api';

export const DownloadCard = () => {
  const { job, setJob, setFile } = useAppStore();
  if (!job || job.status !== 'completed') return null;

  const handleDelete = async () => {
    try {
      // await deleteJob(job.jobId);
      setJob(null);
      setFile(null);
    } catch(err) {
      console.error(err);
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
"""

files["src/layouts/MainLayout.tsx"] = """import React from 'react';
import { useTheme } from '@/providers/ThemeProvider';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';

export const MainLayout = ({ children }: { children: React.ReactNode }) => {
  const { theme, setTheme } = useTheme();

  return (
    <div className="min-h-screen bg-background flex flex-col">
      <header className="border-b px-6 py-4 flex items-center justify-between sticky top-0 bg-background/80 backdrop-blur z-10">
        <h1 className="text-xl font-bold tracking-tight">CSV-to-Speech Platform</h1>
        <Button 
          variant="ghost" 
          size="icon" 
          onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
        >
          {theme === 'dark' ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
      </header>
      <main className="flex-1 p-6 container max-w-5xl mx-auto">
        {children}
      </main>
      <footer className="border-t py-6 text-center text-sm text-muted-foreground">
        Powered by EdgeTTS & FastAPI
      </footer>
    </div>
  );
};
"""

files["src/pages/Dashboard.tsx"] = """import React, { useEffect } from 'react';
import { UploadZone } from '@/components/features/tts/UploadZone';
import { ConversionForm } from '@/components/features/tts/ConversionForm';
import { ProgressDashboard } from '@/components/features/tts/ProgressDashboard';
import { DownloadCard } from '@/components/features/tts/DownloadCard';
import { useAppStore } from '@/store/useAppStore';

export const Dashboard = () => {
  const { file, job, setVoices } = useAppStore();

  useEffect(() => {
    // Mock voices
    setVoices([
      { Name: 'Guy', ShortName: 'en-US-GuyNeural', Gender: 'Male', Locale: 'en-US' },
      { Name: 'Aria', ShortName: 'en-US-AriaNeural', Gender: 'Female', Locale: 'en-US' }
    ]);
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
"""

files["src/App.tsx"] = """import React from 'react';
import { ThemeProvider } from '@/providers/ThemeProvider';
import { MainLayout } from '@/layouts/MainLayout';
import { Dashboard } from '@/pages/Dashboard';

function App() {
  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <MainLayout>
        <Dashboard />
      </MainLayout>
    </ThemeProvider>
  );
}

export default App;
"""

files["src/main.tsx"] = """import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './styles/globals.css';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
"""

import sys

for rel_path, content in files.items():
    full_path = os.path.join(base_dir, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Generated all files successfully.")
