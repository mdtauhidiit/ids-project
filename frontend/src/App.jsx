import { useState } from 'react';
import { PRESETS } from './constants/presets';
import Header from './components/Header';
import EngineSelector from './components/EngineSelector';
import PacketInputForm from './components/PacketInputForm';
import ResultsContainer from './components/ResultsContainer';

export default function App() {
  const [formData, setFormData] = useState(PRESETS.normal);
  const [selectedEngine, setSelectedEngine] = useState('compare');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: ['duration', 'same_srv_rate', 'serror_rate'].includes(name)
        ? parseFloat(value) || 0
        : ['src_bytes', 'dst_bytes', 'failed_logins'].includes(name)
        ? parseInt(value, 10) || 0
        : value
    }));
  };

  const handleLoadPreset = (key) => {
    setFormData(PRESETS[key]);
    setResults(null);
    setError(null);
  };

  const handleRunDetection = async () => {
    setLoading(true);
    setError(null);
    try {
      const endpoint =
        selectedEngine === 'compare'
          ? 'http://127.0.0.1:8000/api/detect/compare/'
          : `http://127.0.0.1:8000/api/detect/${selectedEngine}/`;

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error(`Server returned error: HTTP ${response.status}`);
      }

      const data = await response.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'Failed to connect to backend engine.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#0B0F17] text-slate-100 font-sans p-6 md:p-12">
      <div className="max-w-6xl mx-auto space-y-8">
        <Header onLoadPreset={handleLoadPreset} />

        <EngineSelector
          selectedEngine={selectedEngine}
          onSelectEngine={(engine) => {
            setSelectedEngine(engine);
            setResults(null);
          }}
        />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-6">
            <PacketInputForm
              formData={formData}
              onChange={handleInputChange}
              onSubmit={handleRunDetection}
              loading={loading}
              error={error}
            />
          </div>

          <div className="lg:col-span-6">
            <ResultsContainer
              results={results}
              loading={loading}
              selectedEngine={selectedEngine}
            />
          </div>
        </div>
      </div>
    </div>
  );
}