import { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import { AlertTriangle, CheckCircle2, AlertCircle, TrendingUp, Activity } from 'lucide-react';

interface Prediction {
  test_id: string;
  prediction: string;
  flakiness_score: number;
  confidence: number;
  execution_count: number;
  failure_rate: number;
  transition_rate: number;
  features: Record<string, number>;
  recommendations: Array<{
    priority: string;
    message: string;
    action: string;
  }>;
}

interface AnalysisResult {
  summary: {
    total_tests: number;
    flaky_tests: number;
    stable_tests: number;
    insufficient_data: number;
    model_type: string;
    feature_importance: Record<string, number>;
  };
  predictions: Prediction[];
}

interface Dataset {
  id: number;
  name: string;
  num_tests: number;
  num_executions: number;
  is_synthetic: boolean;
}

export default function TestAnalysis() {
  const [searchParams] = useSearchParams();
  const urlDatasetId = searchParams.get('dataset');
  
  const [datasets, setDatasets] = useState<Dataset[]>([]);
  const [selectedDatasetId, setSelectedDatasetId] = useState<string>(urlDatasetId || '');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<AnalysisResult | null>(null);
  const [error, setError] = useState('');
  const [modelType, setModelType] = useState('random_forest');

  useEffect(() => {
    loadDatasets();
  }, []);

  const loadDatasets = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/datasets/');
      if (response.ok) {
        const data = await response.json();
        setDatasets(data);
        // Auto-select first dataset if none selected
        if (data.length > 0 && !selectedDatasetId) {
          setSelectedDatasetId(data[0].id.toString());
        }
      }
    } catch (err) {
      console.error('Failed to load datasets:', err);
    }
  };

  const runAnalysis = async () => {
    if (!selectedDatasetId) {
      setError('No dataset selected');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const response = await fetch(
        `http://localhost:8000/api/v1/predictions/analyze/${selectedDatasetId}?model_type=${modelType}`,
        { method: 'POST' }
      );

      if (response.ok) {
        const data = await response.json();
        setResults(data);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Analysis failed');
      }
    } catch (err) {
      setError('Failed to run analysis. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const getPredictionColor = (prediction: string) => {
    switch (prediction) {
      case 'FLAKY': return 'text-yellow-700 bg-yellow-100 border-yellow-300';
      case 'NOT_FLAKY': return 'text-green-700 bg-green-100 border-green-300';
      case 'INSUFFICIENT_DATA': return 'text-gray-700 bg-gray-100 border-gray-300';
      default: return 'text-gray-700 bg-gray-100 border-gray-300';
    }
  };

  const getPredictionIcon = (prediction: string) => {
    switch (prediction) {
      case 'FLAKY': return <AlertTriangle className="h-5 w-5" />;
      case 'NOT_FLAKY': return <CheckCircle2 className="h-5 w-5" />;
      case 'INSUFFICIENT_DATA': return <AlertCircle className="h-5 w-5" />;
      default: return null;
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Flaky Test Analysis</h1>
        <p className="text-gray-600 mt-2">AI-powered flaky test detection and root cause analysis</p>
      </div>

      {/* Analysis Controls */}
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-semibold mb-4">Run Analysis</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Dataset
            </label>
            <select
              value={selectedDatasetId}
              onChange={(e) => setSelectedDatasetId(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="">-- Select Dataset --</option>
              {datasets.map((dataset) => (
                <option key={dataset.id} value={dataset.id}>
                  {dataset.name} ({dataset.num_tests} tests, {dataset.num_executions} executions)
                </option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              ML Model
            </label>
            <select
              value={modelType}
              onChange={(e) => setModelType(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="baseline">Baseline (Rule-based)</option>
              <option value="logistic">Logistic Regression</option>
              <option value="random_forest">Random Forest (Recommended)</option>
              <option value="gradient_boosting">Gradient Boosting</option>
            </select>
          </div>
        </div>
        <button
          onClick={runAnalysis}
          disabled={loading || !selectedDatasetId}
          className="w-full px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed font-medium"
        >
          {loading ? 'Analyzing...' : 'Run Analysis'}
        </button>
        
        {datasets.length === 0 && (
          <p className="mt-4 text-sm text-yellow-700 bg-yellow-50 border border-yellow-200 rounded p-3">
            Please upload a dataset first in Dataset Management
          </p>
        )}
      </div>

      {/* Error */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <p className="text-red-800">{error}</p>
        </div>
      )}

      {/* Results */}
      {results && (
        <>
          {/* Summary */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-semibold mb-4">Analysis Summary</h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="text-2xl font-bold text-gray-900">{results.summary.total_tests}</div>
                <div className="text-sm text-gray-600">Total Tests</div>
              </div>
              <div className="bg-yellow-50 rounded-lg p-4 border border-yellow-200">
                <div className="text-2xl font-bold text-yellow-700">{results.summary.flaky_tests}</div>
                <div className="text-sm text-yellow-700">Flaky Tests</div>
              </div>
              <div className="bg-green-50 rounded-lg p-4 border border-green-200">
                <div className="text-2xl font-bold text-green-700">{results.summary.stable_tests}</div>
                <div className="text-sm text-green-700">Stable Tests</div>
              </div>
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="text-2xl font-bold text-gray-700">{results.summary.insufficient_data}</div>
                <div className="text-sm text-gray-600">Insufficient Data</div>
              </div>
            </div>

            {/* Feature Importance */}
            {Object.keys(results.summary.feature_importance).length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3 flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Top Contributing Features
                </h3>
                <div className="space-y-2">
                  {Object.entries(results.summary.feature_importance).slice(0, 5).map(([feature, importance]) => (
                    <div key={feature} className="flex items-center">
                      <div className="w-40 text-sm text-gray-700">{feature}</div>
                      <div className="flex-1 bg-gray-200 rounded-full h-4">
                        <div
                          className="bg-blue-600 h-4 rounded-full"
                          style={{ width: `${importance * 100}%` }}
                        />
                      </div>
                      <div className="w-16 text-right text-sm text-gray-600">
                        {(importance * 100).toFixed(1)}%
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Predictions */}
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold">Test Predictions</h2>
            </div>
            <div className="p-6 space-y-4">
              {results.predictions.slice(0, 20).map((prediction) => (
                <div
                  key={prediction.test_id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <h3 className="font-semibold text-gray-900">{prediction.test_id}</h3>
                        <span className={`px-3 py-1 rounded-full text-sm font-medium border flex items-center space-x-1 ${getPredictionColor(prediction.prediction)}`}>
                          {getPredictionIcon(prediction.prediction)}
                          <span>{prediction.prediction}</span>
                        </span>
                      </div>

                      <div className="mt-3 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                        <div>
                          <span className="text-gray-600">Flakiness Score:</span>
                          <span className="ml-2 font-semibold">{(prediction.flakiness_score * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Executions:</span>
                          <span className="ml-2 font-semibold">{prediction.execution_count}</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Failure Rate:</span>
                          <span className="ml-2 font-semibold">{(prediction.failure_rate * 100).toFixed(1)}%</span>
                        </div>
                        <div>
                          <span className="text-gray-600">Transitions:</span>
                          <span className="ml-2 font-semibold">{(prediction.transition_rate * 100).toFixed(1)}%</span>
                        </div>
                      </div>

                      {/* Recommendations */}
                      {prediction.recommendations.length > 0 && (
                        <div className="mt-4 space-y-2">
                          {prediction.recommendations.map((rec, idx) => (
                            <div
                              key={idx}
                              className={`p-3 rounded-lg border text-sm ${
                                rec.priority === 'HIGH' ? 'bg-red-50 border-red-200' :
                                rec.priority === 'MEDIUM' ? 'bg-yellow-50 border-yellow-200' :
                                'bg-blue-50 border-blue-200'
                              }`}
                            >
                              <div className="flex items-start">
                                <Activity className="h-4 w-4 mt-0.5 mr-2 flex-shrink-0" />
                                <div className="flex-1">
                                  <p className="font-medium">{rec.message}</p>
                                  <p className="text-xs mt-1 opacity-80">→ {rec.action}</p>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              ))}

              {results.predictions.length > 20 && (
                <p className="text-center text-gray-600 text-sm">
                  Showing top 20 results. Total: {results.predictions.length} tests analyzed.
                </p>
              )}
            </div>
          </div>
        </>
      )}
    </div>
  );
}
