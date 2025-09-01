// src/stores/friendStore.js
import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useFriendStore = defineStore('friends', () => {
  // --- STATE ---
  const state = reactive({
    friends: [],
    pendingRequests: [],
    isLoading: false,
    error: null
  });

  // --- ACTIONS ---

  /**
   * Busca todos os dados de amizades do usuário.
   */
  async function fetchFriendsData() {
    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient('/friends');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar dados de amigos.');
      }
      state.friends = data.friends;
      state.pendingRequests = data.pendingRequests;
    } catch (err) {
      state.error = err.message;
      console.error("Erro ao buscar amigos:", err.message);
    } finally {
      state.isLoading = false;
    }
  }

  /**
   * Envia um pedido de amizade para um usuário.
   * @param {number} friendId - O ID do usuário a ser adicionado.
   */
  async function sendFriendRequest(friendId) {
    try {
      const response = await apiClient(`/friends/request/${friendId}`, { method: 'POST' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      // Opcional: Atualizar o estado local para feedback imediato
      return { success: true, message: data.message };
    } catch (error) {
      console.error("Erro ao enviar pedido de amizade:", error.message);
      return Promise.reject(error.message);
    }
  }

  /**
   * Aceita um pedido de amizade.
   * @param {number} requesterId - O ID do usuário que enviou o pedido.
   */
  async function acceptFriendRequest(requesterId) {
    try {
      const response = await apiClient(`/friends/accept/${requesterId}`, { method: 'PUT' });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      // Atualiza a lista de amigos e remove o pedido pendente
      await fetchFriendsData(); 
      return { success: true, message: data.message };
    } catch (error) {
      console.error("Erro ao aceitar pedido:", error.message);
      return Promise.reject(error.message);
    }
  }

  return {
    state,
    fetchFriendsData,
    sendFriendRequest,
    acceptFriendRequest
  };
});