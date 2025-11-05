import { Calendar, ChevronRight, CheckSquare } from 'lucide-react';
import TaskList from './TaskList';
import HabitList from './HabitList';

export default function Section({ section, isOpen, toggle, getPriorityColor, getPriorityBorder }) {
  return (
    <div className="bg-purple-900/20 backdrop-blur-sm my-4 border border-purple-700/30 rounded-xl">
      <button
        onClick={() => toggle(section.id)}
        aria-expanded={isOpen}
        className="w-full flex items-center justify-between p-6"
      >
        <div className="flex items-center gap-3">
          <Calendar className="text-green-400" size={24} />
          <div className="text-left">
            <h2 className="text-2xl font-bold text-white">{section.title}</h2>
            <p className="text-gray-400 text-sm">{section.date}</p>
          </div>
        </div>
        <ChevronRight
          size={22}
          className={`text-gray-300 transition-transform duration-300 ${isOpen ? 'rotate-90' : ''}`}
        />
      </button>

      <div
        className={`transition-all duration-300 ease-in-out overflow-hidden ${isOpen ? 'max-h-[2000px] opacity-100' : 'max-h-0 opacity-0'}`}
      >
        <div className="px-6 pb-6 space-y-4">
          
          {section.tasks?.length > 0 && (<TaskList
            tasks={section.tasks}
            getPriorityColor={getPriorityColor}
            getPriorityBorder={getPriorityBorder}
          />)}
          {section.habits?.length > 0 && (
            <HabitList
              habits={section.habits}
              getPriorityColor={getPriorityColor}
              getPriorityBorder={getPriorityBorder}
            />
          )}
        </div>
      </div>
    </div>
  );
}
