import React from 'react';
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
