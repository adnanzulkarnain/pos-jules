import { Outlet } from 'react-router-dom';
import './App.css'; // Keep App.css for now, might be useful later

function App() {
  return (
    <div>
      <p>POS Frontend Ready</p>
      <Outlet />
    </div>
  );
}

export default App;
