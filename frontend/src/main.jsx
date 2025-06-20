import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import Dashboard from './pages/Dashboard.jsx';
import KasirPage from './pages/KasirPage.jsx'; // New import

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          <Route index element={<Dashboard />} /> {/* Dashboard as index */}
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="kasir" element={<KasirPage />} /> {/* New Route */}
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
