import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import DatasetManagement from './pages/DatasetManagement';
import TestAnalysis from './pages/TestAnalysis';

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              FlakeGuard AI
            </h1>
            <p className="text-sm text-gray-600 mt-1">
              Explainable AI for Flaky Test Detection
            </p>
          </div>
        </header>
        
        <div className="max-w-7xl mx-auto px-4 py-4">
          <Navigation />
        </div>
        
        <main className="max-w-7xl mx-auto px-4 py-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/datasets" element={<DatasetManagement />} />
            <Route path="/analysis" element={<TestAnalysis />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

function Navigation() {
  const location = useLocation();
  
  const links = [
    { path: '/', label: 'Dashboard' },
    { path: '/datasets', label: 'Dataset Management' },
    { path: '/analysis', label: 'Flaky Test Analysis' },
  ];
  
  return (
    <nav className="flex space-x-4">
      {links.map(link => (
        <Link
          key={link.path}
          to={link.path}
          className={`px-4 py-2 rounded-lg ${
            location.pathname === link.path
              ? 'bg-blue-100 text-blue-700 font-medium'
              : 'text-gray-600 hover:bg-gray-100'
          }`}
        >
          {link.label}
        </Link>
      ))}
    </nav>
  );
}

function Dashboard() {
  return (
    <div className="space-y-6">
      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-2xl font-semibold text-gray-900 mb-4">
          Welcome to FlakeGuard AI
        </h2>
        <p className="text-gray-700 mb-4">
          An Explainable AI Framework for Flaky Test Detection, Failure Prediction, 
          and Root Cause Analysis in CI/CD Pipelines
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
          <Link to="/datasets" className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition">
            <h3 className="font-semibold text-lg mb-2">📂 Dataset Management</h3>
            <p className="text-sm text-gray-600">
              Upload and manage test execution datasets
            </p>
          </Link>
          
          <Link to="/analysis" className="border border-blue-200 rounded-lg p-4 bg-blue-50 hover:border-blue-400 transition">
            <h3 className="font-semibold text-lg mb-2">🤖 Flaky Test Analysis</h3>
            <p className="text-sm text-blue-700">
              AI-powered detection and root cause analysis
            </p>
          </Link>
          
          <div className="border border-gray-200 rounded-lg p-4 opacity-50">
            <h3 className="font-semibold text-lg mb-2">📊 Reports</h3>
            <p className="text-sm text-gray-600">
              Experiment results and exports (Coming soon)
            </p>
          </div>
        </div>
      </div>
      
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">Getting Started</h3>
        <ol className="list-decimal list-inside space-y-2 text-blue-800">
          <li>Go to <Link to="/datasets" className="underline font-medium">Dataset Management</Link> and upload the synthetic CSV</li>
          <li>Click <Link to="/analysis?dataset=1" className="underline font-medium">Flaky Test Analysis</Link> to detect flaky tests</li>
          <li>Select a model type (Random Forest recommended)</li>
          <li>View predictions, flakiness scores, and recommendations</li>
        </ol>
      </div>
      
      <div className="bg-white shadow rounded-lg p-6">
        <h3 className="font-semibold text-lg mb-4">Backend Status</h3>
        <div className="flex items-center space-x-2">
          <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-gray-700">Backend API: Connected</span>
        </div>
        <p className="text-sm text-gray-600 mt-2">
          API URL: <code className="bg-gray-100 px-2 py-1 rounded">http://localhost:8000</code>
        </p>
      </div>
    </div>
  );
}

export default App;
