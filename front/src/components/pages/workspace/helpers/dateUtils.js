// Таймзона
export const TZ = 'Asia/Almaty';

export function formatYMD(dateLike) {
  const d = new Date(dateLike);
  const parts = new Intl.DateTimeFormat('en-CA', {
    timeZone: TZ,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  }).formatToParts(d);
  const y = parts.find(p => p.type === 'year')?.value ?? '0000';
  const m = parts.find(p => p.type === 'month')?.value ?? '01';
  const day = parts.find(p => p.type === 'day')?.value ?? '01';
  return `${y}-${m}-${day}`;
}

export function formatHuman(dateLike) {
  return new Intl.DateTimeFormat('en-US', {
    timeZone: TZ,
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  }).format(new Date(dateLike));
}

export function todayYMD() {
  return formatYMD(Date.now());
}

export function tomorrowYMD() {
  const t = new Date();
  const parts = new Intl.DateTimeFormat('en-US', {
    timeZone: TZ,
    year: 'numeric',
    month: 'numeric',
    day: 'numeric',
  }).formatToParts(t);
  const y = Number(parts.find(p => p.type === 'year')?.value);
  const m = Number(parts.find(p => p.type === 'month')?.value);
  const d = Number(parts.find(p => p.type === 'day')?.value);
  const localMidnight = new Date(Date.UTC(y, m - 1, d));
  const plus1 = new Date(localMidnight.getTime() + 24 * 60 * 60 * 1000);
  return formatYMD(plus1);
}
