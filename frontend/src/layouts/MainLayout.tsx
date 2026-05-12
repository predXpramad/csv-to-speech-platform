import React from 'react';
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
