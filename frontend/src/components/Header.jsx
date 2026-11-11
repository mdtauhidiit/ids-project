
import { PRESETS } from "../constants/presets"
const Header = () => {
  return (
    <header className="border-b border-slate-800 pb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
      <div>
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-3">
          <span className="h-3 w-3 rounded-full bg-emerald-500 animate-pulse"></span>
          OmniDefense IDS
        </h1>
        <p className="text-slate-400 text-sm mt-1">Multi-Paradigm Intrusion Detection Gateway</p>
      </div>

      <div className="flex flex-wrap gap-2">
        {Object.keys(PRESETS).map((key) => (
          <button
            key={key}
            type="button"
            onClick={() => onLoadPreset(key)}
            className="px-3 py-1.5 text-xs font-medium rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition-colors uppercase tracking-wider"
          >
            {key.replace('_', ' ')}
          </button>
        ))}
      </div>
    </header>
  )
}

export default Header