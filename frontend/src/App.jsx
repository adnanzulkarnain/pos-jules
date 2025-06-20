import { Outlet, Link } from 'react-router-dom'; // Ensure Link is imported
import './App.css'; // Keep App.css for now, might be useful later

function App() {
  return (
    <div>
      <nav className="bg-gray-800 p-4 text-white">
        <ul className="flex space-x-4">
          <li>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li>
            <Link to="/kasir">Kasir</Link> {/* New Link */}
          </li>
        </ul>
      </nav>
      <main className="p-4">
        <Outlet /> {/* This is where child routes like KasirPage will render */}
      </main>
      {/* Footer or other common elements */}
    </div>
  );
}

export default App;
