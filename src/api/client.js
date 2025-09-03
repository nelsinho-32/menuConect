// src/api/client.js
import { useAuthStore } from '@/stores/authStore';

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Um wrapper para a API fetch que adiciona automaticamente o token de autenticação.
 * @param {string} endpoint - O endpoint da API (ex: '/favorites/restaurants').
 * @param {object} options - As opções do fetch (method, body, etc.).
 * @returns {Promise<Response>}
 */
const apiClient = (endpoint, options = {}) => {
  
 const authStore = useAuthStore();

  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  // Adiciona o token de autenticação se ele existir
  if (authStore.token) {
    defaultHeaders['Authorization'] = `Bearer ${authStore.token}`;
  }

  // Combina os cabeçalhos padrão com quaisquer cabeçalhos personalizados
  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  return fetch(`${BASE_URL}${endpoint}`, config);
};

export default apiClient;