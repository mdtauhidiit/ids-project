
import DiagnosticCard from './DiagnosticCard';

const ResultsContainer = ({ results, loading, selectedEngine }) => {
  return (
    <div className="space-y-4">
      <h2 className="text-base font-semibold text-slate-200">Diagnostics & Verdict</h2>

      {!results && !loading && (
        <div className="h-64 border border-dashed border-slate-800 rounded-2xl flex items-center justify-center text-slate-500 text-sm">
          Awaiting input execution.
        </div>
      )}

      {loading && (
        <div className="h-64 border border-dashed border-indigo-500/30 rounded-2xl flex flex-col items-center justify-center text-slate-400 text-sm space-y-3">
          <div className="w-6 h-6 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Processing network features...</span>
        </div>
      )}

      {results && !loading && (
        <div className="space-y-3">
          {selectedEngine === 'compare' ? (
            <>
              <DiagnosticCard title="Rule-Based Engine" data={results.rule_based} />
              <DiagnosticCard title="Machine Learning (Random Forest)" data={results.machine_learning} />
              <DiagnosticCard title="Deep Learning (PyTorch MLP)" data={results.deep_learning} />
            </>
          ) : (
            <DiagnosticCard title={results.method} data={results} />
          )}
        </div>
      )}
    </div>
  )
}

export default ResultsContainer