import { Target, ChevronRight } from 'lucide-react';

export default function HabitList({ habits, getPriorityColor, getPriorityBorder }) {
  return (
    <div>
      <h3 className="text-lg font-semibold text-white mb-4 flex items-center gap-2">
        <Target className="text-green-400" size={20} />
        Habits
      </h3>

      
        <div className="space-y-3">
          {habits.map(habit => (
            <div
              key={habit.id}
              className={`bg-gray-900/60 border ${getPriorityBorder(habit.priority)} rounded-lg p-4 hover:bg-gray-900/80 transition-colors`}
            >
              <div className="flex items-start gap-3">
                <input
                  type="checkbox"
                  className="mt-1 w-5 h-5 rounded border-purple-700/30 bg-gray-800 cursor-pointer"
                  defaultChecked={Boolean(habit.is_checked)}
                />
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <h4 className="text-white font-medium">{habit.title}</h4>
                    <span className={`${getPriorityColor(habit.priority)} text-white text-xs px-2 py-1 rounded uppercase font-semibold`}>
                      {habit.priority}
                    </span>
                    {habit.schedule && (
                      <span className="text-xs text-gray-400">{habit.schedule}</span>
                    )}
                  </div>
                  {habit.description && (
                    <p className="text-gray-400 text-sm">{habit.description}</p>
                  )}
                </div>
                <ChevronRight className="text-gray-600" size={20} />
              </div>
            </div>
          ))}
        </div>
    </div>
  );
}
