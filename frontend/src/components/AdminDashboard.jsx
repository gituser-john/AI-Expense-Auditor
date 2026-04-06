import React, { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle, Clock } from 'lucide-react';

function AdminDashboard() {
  const [expenses, setExpenses] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const loadData = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8000/api/expenses");
        if (!response.ok) {
          throw new Error("Failed to load expenses from the server.");
        }
        const data = await response.json();
        setExpenses(data);
      } catch (err) {
        console.error("Failed to load expenses:", err);
        setError(err.message || "An unexpected error occurred.");
      } finally {
        setIsLoading(false);
      }
    };
    loadData();
  }, []);

  const getVerdictBadge = (verdict) => {
    switch (verdict.toLowerCase()) {
      case 'approved':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
            <CheckCircle className="w-3.5 h-3.5" /> Approved
          </span>
        );
      case 'flagged':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-amber-100 text-amber-800 border border-amber-200">
            <Clock className="w-3.5 h-3.5" /> Flagged
          </span>
        );
      case 'rejected':
        return (
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-rose-100 text-rose-800 border border-rose-200">
            <AlertCircle className="w-3.5 h-3.5" /> Rejected
          </span>
        );
      default:
        const displayVerdict = verdict.charAt(0).toUpperCase() + verdict.slice(1);
        return (
          <span className="inline-flex items-center px-2.5 py-1 rounded-full text-xs font-medium bg-slate-100 text-slate-800">
            {displayVerdict}
          </span>
        );
    }
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-slate-900"></div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto mt-8 relative">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold text-slate-900">Expense Audit Dashboard</h1>
          <p className="text-sm text-slate-500 mt-1">Review AI evaluated expense reports and verdicts.</p>
        </div>
      </div>

      {error && (
        <div className="mb-6 bg-rose-50 text-rose-800 p-4 rounded-lg flex items-start gap-3 border border-rose-200">
          <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0 text-rose-600" />
          <p className="text-sm font-medium">{error}</p>
        </div>
      )}

      <div className="bg-white border text-sm border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="py-4 px-6 font-semibold text-slate-600">Date</th>
                <th className="py-4 px-6 font-semibold text-slate-600">Merchant</th>
                <th className="py-4 px-6 font-semibold text-slate-600">Amount</th>
                <th className="py-4 px-6 font-semibold text-slate-600">Purpose</th>
                <th className="py-4 px-6 font-semibold text-slate-600">AI Verdict</th>
                <th className="py-4 px-6 font-semibold text-slate-600">Policy Citation</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200">
              {expenses.map((expense) => (
                <tr key={expense.id} className="hover:bg-slate-50/50 transition-colors">
                  <td className="py-4 px-6 whitespace-nowrap text-slate-600">{expense.date || 'N/A'}</td>
                  <td className="py-4 px-6 font-medium text-slate-900">{expense.merchant || 'Unknown'}</td>
                  <td className="py-4 px-6 font-medium text-slate-900">
                    {expense.amount != null && !isNaN(expense.amount) ? `$${Number(expense.amount).toFixed(2)}` : 'N/A'}
                  </td>
                  <td className="py-4 px-6 text-slate-600 min-w-48">{expense.business_purpose || 'N/A'}</td>
                  <td className="py-4 px-6 whitespace-nowrap">{getVerdictBadge(expense.ai_verdict || 'Unknown')}</td>
                  <td className="py-4 px-6 text-slate-500 text-xs leading-relaxed max-w-xs">{expense.citation || 'N/A'}</td>
                </tr>
              ))}
              {expenses.length === 0 && (
                <tr>
                  <td colSpan="6" className="py-8 text-center text-slate-500">No expenses found.</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
