import axios from 'axios';

// Create axios instance
export const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const authAPI = {
  login: (email: string, password: string) =>
    api.post('/api/v1/auth/login', { email, password }),
  register: (userData: any) =>
    api.post('/api/v1/auth/register', userData),
  me: () => api.get('/api/v1/auth/me'),
  refresh: () => api.post('/api/v1/auth/refresh'),
};

export const startupAPI = {
  create: (startupData: any) =>
    api.post('/api/v1/generation/startup', startupData),
  getAll: () => api.get('/api/v1/startups'),
  getById: (id: string) => api.get(`/api/v1/startups/${id}`),
  update: (id: string, startupData: any) =>
    api.put(`/api/v1/startups/${id}`, startupData),
  delete: (id: string) => api.delete(`/api/v1/startups/${id}`),
};

export const pitchDeckAPI = {
  generate: (request: any) =>
    api.post('/api/v1/generation/pitch-deck', request),
  getStatus: (id: string) =>
    api.get(`/api/v1/generation/pitch-deck/${id}/status`),
  getAll: () => api.get('/api/v1/pitch-decks'),
  getById: (id: string) => api.get(`/api/v1/pitch-decks/${id}`),
  update: (id: string, pitchDeckData: any) =>
    api.put(`/api/v1/pitch-decks/${id}`, pitchDeckData),
  delete: (id: string) => api.delete(`/api/v1/pitch-decks/${id}`),
  duplicate: (id: string) => api.post(`/api/v1/pitch-decks/${id}/duplicate`),
};

export const slideAPI = {
  generate: (slideType: string, startupId: string, customPrompt?: string) =>
    api.post(`/api/v1/generation/slide/${slideType}`, { startup_id: startupId, custom_prompt: customPrompt }),
  update: (id: string, slideData: any) =>
    api.put(`/api/v1/slides/${id}`, slideData),
  delete: (id: string) => api.delete(`/api/v1/slides/${id}`),
  reorder: (pitchDeckId: string, slideOrder: string[]) =>
    api.put(`/api/v1/pitch-decks/${pitchDeckId}/reorder`, { slide_order: slideOrder }),
};

export const marketResearchAPI = {
  generate: (startupId: string) =>
    api.post(`/api/v1/generation/market-research/${startupId}`),
};

export const financialModelAPI = {
  generate: (startupId: string) =>
    api.post(`/api/v1/generation/financial-model/${startupId}`),
};

export const templateAPI = {
  getAll: () => api.get('/api/v1/templates'),
  getById: (id: string) => api.get(`/api/v1/templates/${id}`),
  create: (templateData: any) =>
    api.post('/api/v1/templates', templateData),
  update: (id: string, templateData: any) =>
    api.put(`/api/v1/templates/${id}`, templateData),
  delete: (id: string) => api.delete(`/api/v1/templates/${id}`),
};

export const exportAPI = {
  exportPPTX: (pitchDeckId: string) =>
    api.post(`/api/v1/export/pptx/${pitchDeckId}`),
  exportPDF: (pitchDeckId: string) =>
    api.post(`/api/v1/export/pdf/${pitchDeckId}`),
  exportGoogleSlides: (pitchDeckId: string) =>
    api.post(`/api/v1/export/google-slides/${pitchDeckId}`),
};

export const analysisAPI = {
  analyze: (pitchDeckId: string) =>
    api.post(`/api/v1/analysis/${pitchDeckId}`),
  getFeedback: (pitchDeckId: string) =>
    api.get(`/api/v1/analysis/${pitchDeckId}/feedback`),
  optimize: (pitchDeckId: string, suggestions: any) =>
    api.post(`/api/v1/analysis/${pitchDeckId}/optimize`, suggestions),
};

export const userAPI = {
  getProfile: () => api.get('/api/v1/users/profile'),
  updateProfile: (profileData: any) =>
    api.put('/api/v1/users/profile', profileData),
  updateSubscription: (subscriptionData: any) =>
    api.put('/api/v1/users/subscription', subscriptionData),
};

export default api; 