import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});
api.interceptors.response.use((response) => response, (error) => {
  if (error.response?.status === 401) {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    if (!window.location.pathname.startsWith('/login')) window.location.assign('/login');
  }
  return Promise.reject(error);
});

export const authApi = {
  login: (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
};
export const doctorApi = {
  getAll: (search) => api.get('/doctors', { params: search ? { search } : {} }),
  create: (data) => api.post('/doctors', data),
};
export const interactionApi = {
  getAll: () => api.get('/interactions'),
  getById: (id) => api.get(`/interactions/${id}`),
  create: (data) => api.post('/interactions', data),
  update: (id, data) => api.patch(`/interactions/${id}`, data),
};
export const chatApi = {
  createSession: () => api.post('/chat/sessions'),
  send: (sessionId, message) => api.post(`/chat/sessions/${sessionId}/messages`, { message }),
};
export const analyticsApi = {
  getSummary: () => api.get('/analytics/summary'),
};
export default api;
