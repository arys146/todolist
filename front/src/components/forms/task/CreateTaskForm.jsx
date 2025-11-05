
import axios from "axios";
import React, { useState, useEffect } from 'react';
import { CheckSquare, Type, FileText, Star, Calendar, Tag, Plus, X } from 'lucide-react';
import api from "../../../api";

export default function CreateTaskForm({setTasks, onClose}) {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 5,
    due_date: '',
    tag_ids: []
  });
  
  const [allTags, setAllTags] = useState([]);
  const [showNewTagForm, setShowNewTagForm] = useState(false);
  const [newTag, setNewTag] = useState({ title: '', color: '#22c55e' });

  useEffect(() => {
    fetchTags();
  }, []);

  async function fetchTags() {
    try {
      const response = await api.get("/tags");
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

  async function createTask(data) {
    try {
      const response = await api.post("/task", data);
      setTasks(prev => {
        const updated = [...prev, response.data];
        return updated.sort((a, b) => new Date(a.due_date) - new Date(b.due_date));
      });
      onClose();
    } catch (error) {
      console.error("Error:", error);
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    const taskData = {
      ...formData,
      due_date: new Date(formData.due_date).toISOString(),
      priority: parseInt(formData.priority)
    };

    await createTask(taskData);
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

  return (
    <div className="rounded-2xl w-full max-h-[90vh] overflow-y-auto custom-scrollbar">
      <div className="px-16 pt-6">
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="w-12 h-12 bg-green-500 rounded-xl flex items-center justify-center">
              <CheckSquare className="text-white" size={24} />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-white mb-2">Create New Task</h2>
          <p className="text-gray-300 text-sm">Add a task to your list</p>
        </div>

        <div className="space-y-5">
          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Title</label>
            <div className="relative">
              <Type className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                name="title"
                placeholder="Enter task title"
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
                placeholder="Enter task description"
                value={formData.description}
                onChange={handleChange}
                rows="3"
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors resize-none"
                required
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

          <div className="space-y-2">
            <label className="text-white text-sm font-medium">Due Date</label>
            <div className="relative">
              <Calendar className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="datetime-local"
                name="due_date"
                value={formData.due_date}
                onChange={handleChange}
                className="w-full pl-11 pr-4 py-3 bg-gray-900/80 border border-purple-700/30 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:border-green-500 transition-colors"
                required
              />
              <Plus className="absolute right-3 top-1/2 -translate-y-1/2 text-white pointer-events-none" size={20} />

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
            Create Task
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

        input[type="datetime-local"]::-webkit-calendar-picker-indicator{
          opacity: 0;
          cursor: pointer;
          pointer-events: auto;
        }
      `}</style>
    </div>
  );
}