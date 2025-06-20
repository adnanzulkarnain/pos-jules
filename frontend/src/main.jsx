import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './index.css';
import App from './App.jsx';
import Dashboard from './pages/Dashboard.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />}>
          {/* Child route for Dashboard */}
          <Route path="dashboard" element={<Dashboard />} />
          {/* You could add an index route here if App needs a default child: */}
          {/* <Route index element={<SomeDefaultComponentForApp />} /> */}
        </Route>
      </Routes>
    </BrowserRouter>
  </StrictMode>
);
