
import { ENGINES } from '../constants/presets'
const EngineSelector = ({ selectedEngine, onSelectEngine }) => {
  return (
    <div className="flex bg-slate-900/60 p-1.5 rounded-xl border border-slate-800/80 max-w-xl">
      {ENGINES.map((engine) => (
        <button
          key={engine.id}
          type="button"
          onClick={() => onSelectEngine(engine.id)}
          className={`flex-1 py-2 text-xs font-semibold rounded-lg transition-all ${
            selectedEngine === engine.id
              ? 'bg-indigo-600 text-white shadow-sm'
              : 'text-slate-400 hover:text-slate-200'
          }`}
        >
          {engine.label}
        </button>
      ))}
    </div>
  )
}

export default EngineSelector