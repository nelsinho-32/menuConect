// src/stores/authStore.js

import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import apiClient from '@/api/client';

export const useAuthStore = defineStore('auth', () => {
  // --- STATE ---
  // Tenta carregar os dados do usuário do localStorage ao iniciar.
  const user = ref(JSON.parse(localStorage.getItem('menuConnectUser')) || null);
  const token = ref(localStorage.getItem('menuConnectToken') || null);

  // --- GETTERS ---
  const isAuthenticated = computed(() => !!token.value);
  const currentUser = computed(() => user.value);

  // --- ACTIONS ---

  /**
   * Guarda o estado de autenticação no localStorage.
   */
  function setAuthData(userData, userToken) {
    user.value = userData;
    token.value = userToken;
    localStorage.setItem('menuConnectUser', JSON.stringify(userData));
    localStorage.setItem('menuConnectToken', userToken);
  }

  function clearAuthData() {
    user.value = null;
    token.value = null;
    localStorage.removeItem('menuConnectUser');
    localStorage.removeItem('menuConnectToken');
  }

  /**
   * Tenta carregar o usuário do localStorage no arranque da aplicação.
   */
  function tryAutoLogin() {
    const storedToken = localStorage.getItem('menuConnectToken');
    const storedUser = localStorage.getItem('menuConnectUser');
    if (storedToken && storedUser) {
      token.value = storedToken;
      user.value = JSON.parse(storedUser);
    }
  }

  /**
   * Tenta registar um novo usuário.
   * @param {object} credentials - { name, email, password, role }
   * @returns {Promise<boolean>} - True se o registo for bem-sucedido.
   */
  async function register(credentials) {
    try {
        const response = await apiClient('/register', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Falha ao registar.');
        }
        return true;
    } catch (error) {
        console.error("Erro no registo:", error);
        return Promise.reject(error.message);
    }
}

  /**
   * Tenta fazer login de um usuário.
   * @param {object} credentials - { email, password }
   */
  async function login(credentials) {
    try {
        const response = await apiClient('/login', {
            method: 'POST',
            body: JSON.stringify(credentials),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Falha no login.');
        }
        const data = await response.json();
        setAuthData(data.user, data.token);
    } catch (error) {
        console.error("Erro no login:", error);
        return Promise.reject(error.message);
    }
}

  /**
   * Faz logout do usuário.
   */
  function logout() {
    clearAuthData();
    // Opcional: redirecionar para a página de login. Faremos isso no App.vue.
  }

  /**
       * Atualiza o perfil do usuário logado.
       * @param {object} updatedData - Os novos dados do perfil.
       */
      async function updateProfile(updatedData) {
    if (!token.value) {
        return Promise.reject("Nenhum token encontrado.");
    }
    try {
        // apiClient já inclui o token, então não precisamos adicioná-lo aqui
        const response = await apiClient('/profile', {
            method: 'PUT',
            body: JSON.stringify(updatedData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Falha ao atualizar o perfil.');
        }

        const data = await response.json();
        setAuthData(data.user, token.value);
        return data.user;

    } catch (error) {
        console.error("Erro ao atualizar perfil:", error);
        return Promise.reject(error.message);
    }
}

  return {
    user,
    token,
    isAuthenticated,
    currentUser,
    register,
    login,
    logout,
    updateProfile,
    tryAutoLogin,
  }
})