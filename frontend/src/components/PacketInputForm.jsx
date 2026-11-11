

const PacketInputForm = ({ formData, onChange, onSubmit, loading, error }) => {
  return (
    <div className="bg-slate-900/40 border border-slate-800/80 p-6 rounded-2xl space-y-5">
      <h2 className="text-base font-semibold text-slate-200">Packet Vector Parameters</h2>

      <div className="grid grid-cols-2 gap-4">
        <div>
          <label className="text-xs text-slate-400 block mb-1.5">Duration (seconds)</label>
          <input
            type="number"
            step="0.1"
            name="duration"
            value={formData.duration}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 block mb-1.5">Failed Logins</label>
          <input
            type="number"
            name="failed_logins"
            value={formData.failed_logins}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 block mb-1.5">Source Bytes</label>
          <input
            type="number"
            name="src_bytes"
            value={formData.src_bytes}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 block mb-1.5">Destination Bytes</label>
          <input
            type="number"
            name="dst_bytes"
            value={formData.dst_bytes}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 block mb-1.5">Same Srv Rate (0.0 - 1.0)</label>
          <input
            type="number"
            step="0.01"
            name="same_srv_rate"
            value={formData.same_srv_rate}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div>
          <label className="text-xs text-slate-400 block mb-1.5">SYN Error Rate (0.0 - 1.0)</label>
          <input
            type="number"
            step="0.01"
            name="serror_rate"
            value={formData.serror_rate}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="col-span-2">
          <label className="text-xs text-slate-400 block mb-1.5">Connection Flag</label>
          <select
            name="flag"
            value={formData.flag}
            onChange={onChange}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:border-indigo-500"
          >
            <option value="SF">SF (Normal Established)</option>
            <option value="S0">S0 (SYN without reply)</option>
            <option value="REJ">REJ (Connection Rejected)</option>
            <option value="RSTOS0">RSTOS0 (Originator Reset)</option>
          </select>
        </div>

        <div className="col-span-2">
          <label className="text-xs text-slate-400 block mb-1.5">Raw Payload / Inspection String</label>
          <textarea
            rows="2"
            name="payload"
            value={formData.payload}
            onChange={onChange}
            placeholder="Payload string for regex evaluation"
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-2 text-xs font-mono text-slate-200 focus:outline-none focus:border-indigo-500"
          />
        </div>
      </div>

      <button
        type="button"
        onClick={onSubmit}
        disabled={loading}
        className="w-full py-3 rounded-lg bg-indigo-600 hover:bg-indigo-500 text-white font-medium text-sm transition-all shadow-lg shadow-indigo-600/20 disabled:opacity-50"
      >
        {loading ? 'Evaluating Vector...' : 'Execute Evaluation'}
      </button>

      {error && <p className="text-rose-400 text-xs mt-2">{error}</p>}
    </div>
  )
}

export default PacketInputForm