import { Plus, ClipboardList, Target } from 'lucide-react';
import { useState, useEffect, useRef } from 'react';
// если у тебя есть CreateHabitForm — импортни его сюда

export default function FloatingAddButton({ onAddTask, onAddHabit }) {
  const [open, setOpen] = useState(false);
  const wrapRef = useRef(null);
  // Закрываем при любом клике в документе
  useEffect(() => {
    
    if (!open) return;

    const onDocClick = (e) => {
      if (wrapRef.current && !wrapRef.current.contains(e.target)) {
        setOpen(false);
      }
    };
    document.addEventListener('click', onDocClick);

    return () => document.removeEventListener('click', onDocClick);
  }, [open]);

  // Нажатия на дочерние кнопки
  const handleAddTask = (e) => {
    e.stopPropagation();
    onAddTask?.();
    
    setOpen(false);
  };

  const handleAddHabit = (e) => {
    e.stopPropagation();
    onAddHabit?.();
    setOpen(false);
  };

  return (
    <div ref={wrapRef} className="fixed bottom-6 right-6 flex flex-col items-end gap-2 z-50">
      {/* раскрывающиеся кнопки */}
      <div
        className={`flex flex-col items-end gap-2 mb-2 transition-all duration-300 ${
          open ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4 pointer-events-none'
        }`}
      >
        <button
          onClick={handleAddTask}
          className="flex items-center justify-between w-full gap-1 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-full shadow-lg transition-colors"
        >
          <ClipboardList size={18} />
          Add Task
        </button>
        <button
          onClick={handleAddHabit}
          className="flex items-center justify-between gap-1 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-full shadow-lg transition-colors"
        >
          <Target size={18} />
          Add Habit
        </button>
      </div>

      {/* основная круглая кнопка */}
      <button
        onClick={() => setOpen(!open)}
        className={`
          w-14 h-14 flex items-center justify-center rounded-full shadow-lg
          bg-green-500 transition-all duration-300 hover:scale-110
          ${open ? 'rotate-45' : ''}
        `}>
        <Plus size={28} />
      </button>
    </div>
  );
}
