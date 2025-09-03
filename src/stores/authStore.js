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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json();
        // Lança um erro com a mensagem do servidor para ser apanhado no catch.
        throw new Error(errorData.error || 'Falha ao registar.');
      }

      return true; // Sucesso
    } catch (error) {
      console.error("Erro no registo:", error);
      // Retorna a mensagem de erro para ser exibida na UI.
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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(credentials),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Falha no login.');
      }

      const data = await response.json();
      setAuthData(data.user, data.token); // Guarda os dados do usuário e o token

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
            const response = await apiClient('/profile', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token.value}` // Envia o token para autenticação
                },
                body: JSON.stringify(updatedData)
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Falha ao atualizar o perfil.');
            }

            const data = await response.json();
            // Atualiza os dados do usuário localmente com a resposta do servidor
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