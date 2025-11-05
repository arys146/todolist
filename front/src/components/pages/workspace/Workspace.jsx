import React, { useEffect, useMemo, useState, useCallback } from 'react';
import axios from 'axios';
import { X } from 'lucide-react';
import Modal from '../Modal';
import Header from './Header';
import Section from './Section';
import FloatingAddButton from './FloatingAddButton';
import CreateTaskForm from '../../forms/task/CreateTaskForm.jsx';
import CreateHabitForm from '../../forms/habit/CreateHabitForm.jsx';
import { groupTasksByYMD } from './helpers/groupUtils';
import { formatHuman, todayYMD, tomorrowYMD } from './helpers/dateUtils';
import api from "../../../api";


export default function Workspace() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [habits, setHabits] = useState([]);
  const [tasks, setTasks] = useState([]);
  const [openIds, setOpenIds] = useState(new Set());
  const [showForm, setShowForm] = useState(null); // 'task' | 'habit' | null

  const handleAddTask = () => setShowForm('task');
  const handleAddHabit = () => setShowForm('habit');
  const handleCloseForm = () => setShowForm(null);

  const fetchToday = useCallback(async (signal) => {
    setLoading(true);
    try {
      const res = await api.get("/list-today", { signal });
     
      setHabits(res?.data?.habbits ?? []);
      setTasks(res?.data?.tasks ?? []);
    } catch(error) {
      setError('Ошибка загрузки данных.' + error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    fetchToday(controller.signal);
    return () => controller.abort();
  }, [fetchToday]);

  const sections = useMemo(() => {
    const groups = groupTasksByYMD(tasks);
    const tY = todayYMD();
    const tmY = tomorrowYMD();
    const keys = Array.from(groups.keys()).filter(k => k !== 'no-date').sort();

    const out = [];
    let id = 1;
    out.push({ id: id++, title: 'Today', date: formatHuman(new Date()), tasks: groups.get(tY) ?? [], habits });
    if (groups.has(tmY))
      out.push({ id: id++, title: 'Tomorrow', date: formatHuman(tmY), tasks: groups.get(tmY), habits: [] });
    for (const k of keys)
      if (![tY, tmY].includes(k))
        out.push({ id: id++, title: formatHuman(k), date: k, tasks: groups.get(k), habits: [] });
    if (groups.has('no-date'))
      out.push({ id: id++, title: 'No due date', date: '—', tasks: groups.get('no-date'), habits: [] });

    return out;
  }, [tasks, habits]);

  const toggle = (id) => {
    setOpenIds(prev => {
      const next = new Set(prev);
      next.has(id) ? next.delete(id) : next.add(id);
      return next;
    });
  };

  const getPriorityColor = (priority) => priority >= 8 ? 'bg-red-500' : priority >= 5 ? 'bg-yellow-500' : 'bg-green-500';
  const getPriorityBorder = (priority) => priority >= 8 ? 'border-red-500/30' : priority >= 5 ? 'border-yellow-500/30' : 'border-green-500/30';

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-950 via-gray-900 to-purple-900">
      <Header onAdd={() => setIsCreateOpen(true)} />
      <div className="max-w-7xl mx-auto px-6 py-8">
        {loading ? <div className="text-gray-300">Loading…</div> :
          error ? <div className="text-red-400">{error}</div> :
          <div className='space-y-4'>
          {sections.map(s => (
            <Section
              key={s.id}
              section={s}
              isOpen={openIds.has(s.id)}
              toggle={toggle}
              getPriorityColor={getPriorityColor}
              getPriorityBorder={getPriorityBorder}
            />
          ))}</div>
        }
      </div>

      <Modal open={showForm} onClose={handleCloseForm}>
        <button
          onClick={handleCloseForm}
          className="absolute right-4 top-4 text-gray-400 hover:text-white"
        >
          <X size={28} />
        </button>
        {showForm==="task" && <CreateTaskForm setTasks={setTasks} onClose={handleCloseForm}/>}
        {showForm==="habit" && <CreateHabitForm setHabits={setHabits} onClose={handleCloseForm}/>}
      </Modal>

      {showForm === null && <FloatingAddButton
        onAddTask={handleAddTask}
        onAddHabit={handleAddHabit}
      />}
    </div>
  );
}
