
import axios from "axios";
import React, { useState, useEffect } from 'react';
import { Target, Type, FileText, Star, Calendar, Tag, Plus, X } from 'lucide-react';
import api from "../../../api";  

export default function CreateHabitForm({setHabits, onClose}) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 5,
    schedule: '0,1',
    tag_ids: []
  });
  
  const [scheduleType, setScheduleType] = useState('0'); // 0 = weekly, 1 = monthly
  const [interval, setInterval] = useState(1);
  const [selectedDays, setSelectedDays] = useState([]);
  
  const [allTags, setAllTags] = useState([]);
  const [showNewTagForm, setShowNewTagForm] = useState(false);
  const [newTag, setNewTag] = useState({ title: '', color: '#22c55e' });

  const weekDays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const monthDays = Array.from({length: 31}, (_, i) => i + 1);

  useEffect(() => {
    fetchTags();
  }, []);

  useEffect(() => {
    // Update schedule string when schedule params change
    const schedule = `${scheduleType},${interval}${selectedDays.length > 0 ? ',' + selectedDays.join(',') : ''}`;
    setFormData(prev => ({...prev, schedule}));
  }, [scheduleType, interval, selectedDays]);

  async function fetchTags() {
    try {
      const { data } = await api.get("/tags");
      setAllTags(response.data);
    } catch (error) {
      console.error("Error fetching tags:", error);
    }
  }

  async function createNewTag() {
    try {
      const response = await api.post("/tag", newTag);
      setAllTags(prev => [...prev, response.data]);
      setFormData(prev => ({
        ...prev,
        tag_ids: [...prev.tag_ids, response.data.id]
      }));
      setNewTag({ title: '', color: '#22c55e' });
      setShowNewTagForm(false);
    } catch (error) {
      console.error("Error creating tag:", error);
    }
  }

  async function createHabit(data) {
    try {
      const response = await api.post("/habit", data);
      setHabits(prev => [...prev, response.data]);
      onClose();
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const habitData = {
      ...formData,
      priority: parseInt(formData.priority)
    };

    await createHabit(habitData);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const toggleTag = (tagId) => {
    setFormData(prev => ({
      ...prev,
      tag_ids: prev.tag_ids.includes(tagId)
        ? prev.tag_ids.filter(id => id !== tagId)
        : [...prev.tag_ids, tagId]
    }));
  };

  const toggleDay = (day) => {
    setSelectedDays(prev => 
      prev.includes(day)
        ? prev.filter(d => d !== day)
        : [...prev, day].sort((a, b) => a - b)
    );
  };

  return (
    <div className="rounded-2xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar">
      <div className="px-16 pt-6">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
              <Target className="text-white" size={24} />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Create New Habit</h2>
          <p className="text-gray-300 text-sm">Build a consistent routine</p>
        </div>

        <div className="space-y-5">
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Title</label>
            <div className="relative">
              <Type className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                name="title"
                placeholder="Enter habit title"
                value={formData.title}
                onChange={handleChange}
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                required
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Description</label>
            <div className="relative">
              <FileText className="absolute left-3 top-3 text-gray-400" size={20} />
              <textarea
                name="description"
                placeholder="Enter habit description (optional)"
                value={formData.description}
                onChange={handleChange}
                rows="3"
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors resize-none"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Priority (1-10)</label>
            <div className="relative">
              <Star className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="number"
                name="priority"
                min="1"
                max="10"
                placeholder="Priority level"
                value={formData.priority}
                onChange={handleChange}
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                required
              />
            </div>
          </div>

          <div className="space-y-3">
            <label className="text-white text-sm font-medium">Schedule</label>
            
            <div className="flex gap-2">
              <button
                type="button"
                onClick={() => {setScheduleType('0'); setSelectedDays([]);}}
                className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
                  scheduleType === '0'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-900/80 text-gray-400 border border-purple-700/30'
                }`}
              >
                Weekly
              </button>
              <button
                type="button"
                onClick={() => {setScheduleType('1'); setSelectedDays([]);}}
                className={`flex-1 py-2 rounded-lg font-medium transition-colors ${
                  scheduleType === '1'
                    ? 'bg-green-500 text-white'
                    : 'bg-gray-900/80 text-gray-400 border border-purple-700/30'
                }`}
              >
                Monthly
              </button>
            </div>

            <div className="space-y-2">
              <label className="text-white text-sm font-medium">Repeat every</label>
              <div className="flex items-center gap-2">
                <input
                  type="number"
                  min="1"
                  value={interval}
                  onChange={(e) => setInterval(parseInt(e.target.value) || 1)}
                  className="w-20 px-3 py-2 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white focus:outline-none focus:border-green-500 transition-colors"
                />
                <span className="text-gray-300">{scheduleType === '0' ? 'week(s)' : 'month(s)'}</span>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-white text-sm font-medium">
                {scheduleType === '0' ? 'On days' : 'On dates'}
              </label>
              <div className="flex flex-wrap gap-2">
                {scheduleType === '0' ? (
                  weekDays.map((day, index) => (
                    <button
                      key={index}
                      type="button"
                      onClick={() => toggleDay(index + 1)}
                      className={`px-2.5 py-2 rounded-lg font-medium transition-colors ${
                        selectedDays.includes(index + 1)
                          ? 'bg-green-500 text-white border border-purple-700/30 hover:border-green-500'
                          : 'bg-gray-900/80 text-gray-400 border border-purple-700/30 hover:border-green-500'
                      }`}
                    >
                      {day}
                    </button>
                  ))
                ) : (
                  monthDays.map(day => (
                    <button
                      key={day}
                      type="button"
                      onClick={() => toggleDay(day)}
                      className={`w-10 h-10 rounded-lg font-medium transition-colors ${
                        selectedDays.includes(day)
                          ? 'bg-green-500 text-white'
                          : 'bg-gray-900/80 text-gray-400 border border-purple-700/30 hover:border-green-500'
                      }`}
                    >
                      {day}
                    </button>
                  ))
                )}
              </div>
            </div>

            <div className="bg-purple-900/20 border border-purple-700/30 rounded-lg p-3">
              <p className="text-gray-400 text-xs">
                Schedule: <span className="text-green-400 font-mono">{formData.schedule}</span>
              </p>
            </div>
          </div>

          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <label className="text-white text-sm font-medium">Tags</label>
              <button
                type="button"
                onClick={() => setShowNewTagForm(!showNewTagForm)}
                className="text-green-400 hover:text-green-300 text-sm flex items-center gap-1"
              >
                <Plus size={16} />
                New Tag
              </button>
            </div>

            <div className="flex flex-wrap gap-2">
              {allTags.map(tag => (
                <button
                  key={tag.id}
                  type="button"
                  onClick={() => toggleTag(tag.id)}
                  className={`flex items-center gap-1 px-2.5 py-1 rounded-full text-sm font-medium transition-all ${
                    formData.tag_ids.includes(tag.id)
                      ? 'ring-2 ring-green-400 opacity-100'
                      : 'opacity-60 hover:opacity-100'
                  }`}
                  style={{ backgroundColor: tag.color, color: '#fff' }}
                >
                  <Tag size={14} />
                  {tag.title}
                  {formData.tag_ids.includes(tag.id) && <X size={14} />}
                </button>
              ))}
            </div>
          </div>

          {showNewTagForm && (
            <div className="bg-gray-900/60 border border-purple-700/30 rounded-lg p-3 space-y-2">
              <div className="relative">
                <Type className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Tag name"
                  value={newTag.title}
                  onChange={(e) => setNewTag({...newTag, title: e.target.value})}
                  className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                />
              </div>
              <div className="flex items-center gap-2">
                <input
                  type="color"
                  value={newTag.color}
                  onChange={(e) => setNewTag({...newTag, color: e.target.value})}
                  className="w-10 h-10 rounded cursor-pointer bg-gray-800 border border-purple-700/30"
                />
                <button
                  type="button"
                  onClick={createNewTag}
                  className="flex-1 px-3 py-2 bg-green-500 hover:bg-green-600 text-white text-sm rounded transition-colors"
                >
                  Create Tag
                </button>
                <button
                  type="button"
                  onClick={() => setShowNewTagForm(false)}
                  className="px-3 py-2 bg-gray-700 hover:bg-gray-600 text-white text-sm rounded transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          <button 
            onClick={handleSubmit}
            className="w-full py-3 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white font-semibold rounded-lg shadow-lg transform hover:scale-105 transition-all mt-2"
          >
            Create Habit
          </button>
        </div>
      </div>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: rgba(88, 28, 135, 0.3);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: rgba(34, 197, 94, 0.5);
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: rgba(34, 197, 94, 0.7);
        }
      `}</style>
    </div>
  );
}