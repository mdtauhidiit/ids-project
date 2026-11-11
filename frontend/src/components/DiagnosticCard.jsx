import React from 'react'

const DiagnosticCard = ({ title, data }) => {
    if (!data) return null;
    const isAttack = data.anomaly_detected;
  return (
    <div className="bg-slate-900/50 border border-slate-800 p-5 rounded-xl space-y-3">
      <div className="flex justify-between items-center">
        <span className="text-sm font-semibold text-slate-300">{title}</span>
        <span
          className={`px-2.5 py-1 rounded-full text-xs font-semibold ${
            isAttack
              ? 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
              : 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
          }`}
        >
          {data.prediction}
        </span>
      </div>

      <div className="flex items-center gap-4 text-xs text-slate-400">
        <div>
          Confidence: <span className="text-slate-200 font-mono">{(data.confidence * 100).toFixed(1)}%</span>
        </div>
        {data.attack_probability !== undefined && (
          <div>
            Attack Score: <span className="text-slate-200 font-mono">{data.attack_probability}</span>
          </div>
        )}
      </div>

      {data.violations && data.violations.length > 0 && (
        <div className="mt-2 pt-2 border-t border-slate-800/80">
          <p className="text-[11px] font-semibold text-rose-400 mb-1">Triggered Signatures:</p>
          <ul className="list-disc list-inside space-y-0.5 text-[11px] text-slate-400 font-mono">
            {data.violations.map((violation, idx) => (
              <li key={idx}>{violation}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default DiagnosticCard