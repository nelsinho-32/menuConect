// src/stores/usersStore.js
import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useUsersStore = defineStore('users', () => {
  const state = reactive({
    usersList: [],
    viewedUserProfile: null,
    isLoading: false,
    error: null
  });

  async function fetchAllUsers() {
    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient('/users');
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.usersList = data;
    } catch (err) {
      state.error = err.message;
      console.error("Erro ao buscar usuários:", err.message);
    } finally {
      state.isLoading = false;
    }
  }

  async function fetchUserProfile(userId) {
    state.isLoading = true;
    state.error = null;
    state.viewedUserProfile = null;
    try {
      const response = await apiClient(`/users/${userId}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.viewedUserProfile = data;
    } catch (err) {
      state.error = err.message;
      console.error("Erro ao buscar perfil do usuário:", err.message);
    } finally {
      state.isLoading = false;
    }
  }

  return {
    state,
    fetchAllUsers,
    fetchUserProfile
  };
});