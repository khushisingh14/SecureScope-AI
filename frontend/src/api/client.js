import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api",
  timeout: 30000
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("securescope_token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("securescope_token");
      window.dispatchEvent(new Event("securescope:logout"));
    }
    return Promise.reject(error);
  }
);

export function getApiError(error, fallback = "Request failed") {
  const detail = error?.response?.data?.detail;
  if (Array.isArray(detail)) return detail.map((item) => item.msg || item.message || String(item)).join(", ");
  if (detail) return String(detail);
  if (error?.message) return error.message;
  return fallback;
}

export function asArray(value) {
  return Array.isArray(value) ? value : [];
}

export default api;
