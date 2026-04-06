import React, { useState } from 'react';
import { UploadCloud, FileType, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';

function EmployeeUploadPortal() {
  const [file, setFile] = useState(null);
  const [purpose, setPurpose] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [success, setSuccess] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file || !purpose) return;

    setIsSubmitting(true);
    setSuccess(null);

    // Create mock FormData
    const formData = new FormData();
    formData.append('file', file);
    formData.append('business_purpose', purpose);

    try {
      const response = await fetch("http://127.0.0.1:8000/api/upload", {
        method: 'POST',
        body: formData,
      });
      
      if (!response.ok) {
        throw new Error("Failed to upload the receipt. Please try again.");
      }
      
      const data = await response.json();
      setSuccess("Receipt uploaded successfully!");
      setFile(null);
      setPurpose('');
      setError(null);
    } catch (err) {
      console.error(err);
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6 bg-white rounded-xl shadow-sm border border-slate-200 mt-10">
      <div className="mb-8 text-center">
        <h2 className="text-2xl font-semibold text-slate-800 tracking-tight">Submit Expense</h2>
        <p className="text-slate-500 text-sm mt-1">Upload your receipt and provide the business purpose.</p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Business Purpose</label>
          <input
            type="text"
            required
            value={purpose}
            onChange={(e) => setPurpose(e.target.value)}
            className="w-full px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-accent focus:border-accent outline-none transition-all placeholder:text-slate-400"
            placeholder="e.g., Client dinner with ACME Corp"
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-slate-700 mb-2">Receipt Document</label>
          <div className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-slate-300 border-dashed rounded-lg hover:bg-slate-50 transition-colors">
            <div className="space-y-1 text-center">
              {file ? (
                <div className="flex flex-col items-center">
                  <FileType className="mx-auto h-12 w-12 text-accent" />
                  <p className="mt-1 text-sm text-slate-700 font-medium">{file.name}</p>
                  <p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
                  <button type="button" onClick={() => setFile(null)} className="mt-2 text-xs text-danger font-medium hover:underline">Remove</button>
                </div>
              ) : (
                <>
                  <UploadCloud className="mx-auto h-12 w-12 text-slate-400" />
                  <div className="flex text-sm text-slate-600 justify-center">
                    <label
                      htmlFor="file-upload"
                      className="relative cursor-pointer bg-white rounded-md font-medium text-accent hover:text-accent focus-within:outline-none focus-within:ring-2 focus-within:ring-offset-2 focus-within:ring-accent"
                    >
                      <span>Upload a file</span>
                      <input id="file-upload" name="file-upload" type="file" className="sr-only" accept=".jpg,.jpeg,.png,.pdf" onChange={handleFileChange} />
                    </label>
                    <p className="pl-1">or drag and drop</p>
                  </div>
                  <p className="text-xs text-slate-500 mt-2">PNG, JPG, PDF up to 10MB</p>
                </>
              )}
            </div>
          </div>
        </div>

        {success && (
          <div className="bg-emerald-50 text-emerald-800 p-4 rounded-lg flex items-start gap-3 border border-emerald-200">
            <CheckCircle2 className="w-5 h-5 mt-0.5 flex-shrink-0 text-emerald-600" />
            <p className="text-sm font-medium">{success}</p>
          </div>
        )}

        {error && (
          <div className="bg-rose-50 text-rose-800 p-4 rounded-lg flex items-start gap-3 border border-rose-200">
            <AlertCircle className="w-5 h-5 mt-0.5 flex-shrink-0 text-rose-600" />
            <p className="text-sm font-medium">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={!file || !purpose || isSubmitting}
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-slate-900 hover:bg-slate-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-slate-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
        >
          {isSubmitting ? (
            <span className="flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin" /> Processing...
            </span>
          ) : (
            'Submit Expense'
          )}
        </button>
      </form>
    </div>
  );
}

export default EmployeeUploadPortal;
