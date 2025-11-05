import { CheckSquare, ChevronRight } from 'lucide-react';
import { TZ } from './helpers/dateUtils';
import api from "../../../api";

export default function TaskList({ tasks, getPriorityColor, getPriorityBorder }) {
    async function checkTask(val, task_id) {
        try {
            
            if (val){
                const response =  await api.put("/complete_task/" + task_id);
            }else{
                const response =  await api.put("/uncomplete_task/" + task_id);
            }
            
        } catch (error) {
            console.error("Error:", error);
        }
    }

    async function handleCheckboxChange (e, task_id){
        
        const val = e.target.checked;
        await checkTask(val, task_id);
    }

  return (
    <div className="space-y-3">
        <h3 className="text-lg font-semibold text-white flex items-center gap-2">
            <CheckSquare className="text-green-400" size={20} /> Tasks
          </h3>
        {tasks.map(task => (
        <div
          key={task.id}
          className={`bg-gray-900/60 border ${getPriorityBorder(task.priority)} rounded-lg p-4 hover:bg-gray-900/80 transition-colors`}
        >
          <div className="flex items-start gap-3">
            <input
              type="checkbox"
              className="mt-1 w-5 h-5 rounded border-purple-700/30 bg-gray-800 cursor-pointer"
              onChange={(e)=>handleCheckboxChange(e, task.id)}
              defaultChecked={Boolean(task.status)}
            />
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-1">
                <h4 className="text-white font-medium">{task.title}</h4>
                <span className={`${getPriorityColor(task.priority)} text-white text-xs px-2 py-1 rounded uppercase font-semibold`}>
                  {task.priority}
                </span>
                {task.due_date && (
                  <span className="text-xs text-gray-400">
                    {new Intl.DateTimeFormat('en-US', {
                      timeZone: TZ,
                      year: 'numeric',
                      month: 'short',
                      day: '2-digit',
                      hour: '2-digit',
                      minute: '2-digit',
                    }).format(new Date(task.due_date))}
                  </span>
                )}
              </div>
              {task.description && (
                <p className="text-gray-400 text-sm">{task.description}</p>
              )}
            </div>
            <ChevronRight className="text-gray-600" size={20} />
          </div>
        </div>
      ))}
    </div>
  );
}
