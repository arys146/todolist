import axios from "axios";
import { tokenStore } from "./tokenStore";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true, // чтобы refresh-кука ходила туда-обратно
});

// подставляем access token из памяти
api.interceptors.request.use((config) => {
  const t = tokenStore.get();
  if (t) config.headers.Authorization = `Bearer ${t}`;
  return config;
});

let refreshing = false;
let waiters = [];

// дергаем /auth/refresh, который читает refresh из куки и возвращает {access_token}
async function refreshAccess() {
  if (refreshing) return new Promise((res) => waiters.push(res));
  refreshing = true;
  try {
    const { data } = await axios.post(
      "http://localhost:8000/auth/refresh",
      {},
      { withCredentials: true }
    );
    tokenStore.set(data.access_token);
    waiters.forEach((w) => w(data.access_token));
    return data.access_token;
  } catch (e) {
    tokenStore.clear();
    waiters.forEach((w) => w(null));
    throw e;
  } finally {
    refreshing = false;
    waiters = [];
  }
}

// повтор запроса после 401
api.interceptors.response.use(
  (r) => r,
  async (error) => {
    const { response, config } = error;
    if (response?.status === 401 && !config._retry) {
      config._retry = true;
      const t = await refreshAccess().catch(() => null);
      if (t) {
        config.headers.Authorization = `Bearer ${t}`;
        return api(config);
      }
    }
    return Promise.reject(error);
  }
);

export default api;