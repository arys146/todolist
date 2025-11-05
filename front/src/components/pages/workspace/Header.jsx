import { CheckSquare } from 'lucide-react';

export default function Header({ onAdd }) {
  return (
    <div className="bg-purple-900/30 backdrop-blur-sm border-b border-purple-700/30">
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <CheckSquare className="text-green-400" size={32} />
            <h1 className="text-3xl font-bold text-white">My Tasks & Habits</h1>
          </div>
          {/* <button
            onClick={onAdd}
            className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg font-medium transition-colors"
          >
            + Add New
          </button> */}
        </div>
      </div>
    </div>
  );
}