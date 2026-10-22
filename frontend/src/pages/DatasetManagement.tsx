import { useState, useEffect } from 'react';
import { Upload, AlertCircle, CheckCircle2, Database } from 'lucide-react';

interface Dataset {
  id: number;
  name: string;
  source: string;
  is_synthetic: boolean;
  num_tests: number;
  num_executions: number;
  created_at: string;
}

export default function DatasetManagement() {
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [uploading, setUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [error, setError] = useState<string>('');
  const [dragActive, setDragActive] = useState(false);

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/datasets/');
      if (response.ok) {
        const data = await response.json();
        setDatasets(data);
      }
    } catch (err) {
      console.error('Failed to load datasets:', err);
    }
  };

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  };

  const handleFileUpload = async (file: File) => {
    if (!file.name.endsWith('.csv')) {
      setError('Please upload a CSV file');
      return;
    }

    setUploading(true);
    setError('');
    setUploadResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('name', file.name.replace('.csv', ''));

    try {
      const response = await fetch('http://localhost:8000/api/v1/datasets/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const result = await response.json();
        setUploadResult(result);
        loadDatasets(); // Reload dataset list
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Upload failed');
      }
    } catch (err) {
      setError('Failed to upload file. Make sure the backend is running.');
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dataset Management</h1>
        <p className="text-gray-600 mt-2">Upload and manage test execution datasets</p>
      </div>

      {/* Upload Area */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Upload Dataset</h2>
        
        <div
          className={`border-2 border-dashed rounded-lg p-12 text-center ${
            dragActive ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
          } ${uploading ? 'opacity-50 pointer-events-none' : ''}`}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            {uploading ? 'Uploading...' : 'Drop CSV file here or click to browse'}
          </p>
          <p className="text-sm text-gray-600 mb-4">
            CSV format with test execution history
          </p>
          <input
            type="file"
            accept=".csv"
            onChange={handleFileSelect}
            className="hidden"
            id="file-upload"
            disabled={uploading}
          />
          <label
            htmlFor="file-upload"
            className="inline-block px-4 py-2 bg-blue-600 text-white rounded-lg cursor-pointer hover:bg-blue-700"
          >
            Select File
          </label>
        </div>

        {/* Upload Result */}
        {uploadResult && (
          <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
            <div className="flex items-start">
              <CheckCircle2 className="h-5 w-5 text-green-600 mt-0.5 mr-3" />
              <div className="flex-1">
                <h3 className="font-semibold text-green-900">Upload Successful!</h3>
                <div className="mt-2 text-sm text-green-800 space-y-1">
                  <p>Dataset: <strong>{uploadResult.dataset_name}</strong></p>
                  <p>Tests: <strong>{uploadResult.num_tests}</strong></p>
                  <p>Executions: <strong>{uploadResult.num_executions}</strong></p>
                  {uploadResult.is_synthetic && (
                    <p className="text-yellow-700 font-medium">⚠️ Synthetic Data</p>
                  )}
                </div>
                {uploadResult.warnings && uploadResult.warnings.length > 0 && (
                  <div className="mt-2">
                    <p className="text-sm text-yellow-700">
                      Warnings: {uploadResult.warnings.length}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
            <div className="flex items-start">
              <AlertCircle className="h-5 w-5 text-red-600 mt-0.5 mr-3" />
              <div>
                <h3 className="font-semibold text-red-900">Upload Failed</h3>
                <p className="text-sm text-red-800 mt-1">{error}</p>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Dataset List */}
      <div className="bg-white rounded-lg shadow">
        <div className="px-6 py-4 border-b border-gray-200">
          <h2 className="text-xl font-semibold">Uploaded Datasets</h2>
        </div>
        <div className="p-6">
          {datasets.length === 0 ? (
            <div className="text-center py-12 text-gray-500">
              <Database className="mx-auto h-12 w-12 mb-4 opacity-50" />
              <p>No datasets uploaded yet</p>
              <p className="text-sm mt-1">Upload a CSV file to get started</p>
            </div>
          ) : (
            <div className="space-y-4">
              {datasets.map((dataset) => (
                <div
                  key={dataset.id}
                  className="border border-gray-200 rounded-lg p-4 hover:border-blue-300 transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2">
                        <h3 className="font-semibold text-gray-900">{dataset.name}</h3>
                        {dataset.is_synthetic && (
                          <span className="px-2 py-0.5 text-xs bg-yellow-100 text-yellow-800 rounded">
                            SYNTHETIC
                          </span>
                        )}
                      </div>
                      <div className="mt-2 grid grid-cols-3 gap-4 text-sm text-gray-600">
                        <div>
                          <span className="font-medium">Tests:</span> {dataset.num_tests}
                        </div>
                        <div>
                          <span className="font-medium">Executions:</span> {dataset.num_executions}
                        </div>
                        <div>
                          <span className="font-medium">Source:</span> {dataset.source}
                        </div>
                      </div>
                      <div className="mt-1 text-xs text-gray-500">
                        Uploaded: {new Date(dataset.created_at).toLocaleString()}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* CSV Format Help */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
        <h3 className="font-semibold text-blue-900 mb-2">CSV Format Requirements</h3>
        <div className="text-sm text-blue-800 space-y-1">
          <p><strong>Required fields:</strong> test_id, execution_id, timestamp, outcome</p>
          <p><strong>Optional fields:</strong> project_id, duration, retry_count, error_message, environment, etc.</p>
          <p><strong>Example:</strong> test_id,execution_id,timestamp,outcome,duration</p>
          <p className="mt-2 text-xs">
            See documentation for complete schema and example datasets
          </p>
        </div>
      </div>
    </div>
  );
}
