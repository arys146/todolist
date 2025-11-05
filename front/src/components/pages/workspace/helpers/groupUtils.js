import { formatYMD } from './dateUtils';

export function groupTasksByYMD(tasks) {
  const map = new Map();
  for (const t of tasks || []) {
    const key = t?.due_date ? formatYMD(t.due_date) : 'no-date';
    if (!map.has(key)) map.set(key, []);
    map.get(key).push(t);
  }
  return map;
}
