import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useLocation } from 'react-router-dom';
import EmployeeUploadPortal from './components/EmployeeUploadPortal';
import AdminDashboard from './components/AdminDashboard';
import { FileText, LayoutDashboard, ShieldCheck } from 'lucide-react';

function Navigation() {
  const location = useLocation();
  
  const navLinkClass = (path) => {
    const isActive = location.pathname === path;
    return `flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
      isActive 
        ? 'bg-slate-800 text-white' 
        : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
    }`;
  };

  return (
    <nav className="border-b border-slate-200 bg-white">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-6 w-6 text-accent text-blue-600" />
            <span className="font-bold text-lg tracking-tight text-slate-900">Expense Auditor</span>
          </div>
          
          <div className="flex space-x-2">
            <Link to="/" className={navLinkClass('/')}>
              <FileText className="w-4 h-4" />
              Upload Receipt
            </Link>
            <Link to="/admin" className={navLinkClass('/admin')}>
              <LayoutDashboard className="w-4 h-4" />
              Admin Dashboard
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
        <Navigation />
        <main className="p-4 sm:p-6 lg:p-8">
          <Routes>
            <Route path="/" element={<EmployeeUploadPortal />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
