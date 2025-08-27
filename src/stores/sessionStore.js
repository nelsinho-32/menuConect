// src/stores/sessionStore.js

import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useSessionStore = defineStore('sessions', () => {

  const state = reactive({
    activeSession: null,
    isLoading: false,
    error: null
  });

  /**
   * Inicia uma nova sessão de atendimento para uma mesa.
   */
  async function startSession(sessionData) {
    try {
      const response = await apiClient('/management/sessions', {
        method: 'POST',
        body: JSON.stringify(sessionData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao iniciar a sessão.');
      }
      return data; // Retorna { sessionId: ... }
    } catch (err) {
      console.error("Erro ao iniciar sessão:", err.message);
      return Promise.reject(err.message);
    }
  }

  /**
   * Busca os detalhes completos de uma sessão ativa para uma mesa.
   */
  async function fetchActiveSessionForTable(restaurantId, tableId) {
    state.isLoading = true;
    state.error = null;
    state.activeSession = null;
    try {
      const url = `/management/sessions/table/${tableId}?restaurantId=${restaurantId}`;
      const response = await apiClient(url);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar detalhes da sessão.');
      }
      state.activeSession = data;
    } catch (err) {
      console.error("Erro ao buscar sessão ativa:", err.message);
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }
  
  function clearActiveSession() {
      state.activeSession = null;
  }

  /**
   * Adiciona um novo pedido (um ou mais itens) a uma sessão ativa.
   */
  async function addOrderToSession(sessionId, items) {
    try {
      const response = await apiClient(`/management/sessions/${sessionId}/orders`, {
        method: 'POST',
        body: JSON.stringify({ items: items })
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao adicionar pedido à sessão.');
      }
      return data;
    } catch (err) {
      console.error("Erro ao adicionar pedido à sessão:", err.message);
      return Promise.reject(err.message);
    }
  }

   async function finishSession(sessionId, paymentMethod) {
    try {
      const response = await apiClient(`/management/sessions/${sessionId}/finish`, {
        method: 'PUT',
        body: JSON.stringify({ paymentMethod: paymentMethod }) 
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao finalizar a sessão.');
      }
      return true;
    } catch (err) {
      console.error("Erro ao finalizar sessão:", err.message);
      return Promise.reject(err.message);
    }
  }

  async function startSessionFromReservation(reservationId) {
    try {
      const response = await apiClient('/management/sessions/from-reservation', {
        method: 'POST',
        body: JSON.stringify({ reservationId })
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao iniciar atendimento a partir da reserva.');
      }
      return data; // Retorna { sessionId: ... }
    } catch (err) {
      console.error("Erro ao iniciar sessão a partir da reserva:", err.message);
      return Promise.reject(err.message);
    }
  }

  return {
    state,
    startSession,
    fetchActiveSessionForTable,
    clearActiveSession,
    addOrderToSession ,
    finishSession,
    startSessionFromReservation
  };
});