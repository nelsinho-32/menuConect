// src/stores/reservationStore.js

import { reactive } from 'vue';
import { defineStore } from 'pinia';
import { useAuthStore } from './authStore';

export const useReservationStore = defineStore('reservations', () => {
  const authStore = useAuthStore();

  // --- STATE ---
  // Usamos um objeto reativo para guardar as reservas do usuário.
  const userReservations = reactive({
    booked: [], // Armazenará a lista de reservas ativas
    waiting: [] // Armazenará a lista de reservas na fila de espera
    // No futuro, podemos adicionar aqui uma lista de espera.
  });

  async function fetchAllUserReservations() {
    if (!authStore.token) return;
    await fetchMyReservations();
    await fetchMyWaitlist(); // <-- Adicionado
  }

  // --- ACTIONS ---

  /**
   * Busca as reservas ativas do usuário na API.
   */
   async function fetchMyReservations() {
    if (!authStore.token) return;
    try {
      const response = await fetch('http://localhost:5000/api/my-reservations', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        // CORREÇÃO: Em vez de modificar o array, substituímos o array inteiro.
        // Isto garante que o Vue deteta a mudança de forma mais fiável.
        userReservations.booked = [...data];
      } else {
        throw new Error(data.error || 'Falha ao buscar reservas.');
      }
    } catch (error) {
      console.error("Erro ao buscar as minhas reservas:", error);
      userReservations.booked = [];
    }
  }

  /**
   * Cria uma nova reserva.
   * @param {object} reservationData - { restaurantId, tableId, bookingTime, guests }
   * @returns {Promise<boolean>} - True em caso de sucesso.
   */
  async function createReservation(reservationData) {
    if (!authStore.token) return false;
    try {
      const response = await fetch('http://localhost:5000/api/reservations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify(reservationData)
      });
      const data = await response.json();
      if (response.ok) {
        // Após criar a reserva, atualiza a lista de reservas para refletir a mudança.
        await fetchMyReservations();
        return true;
      } else {
        throw new Error(data.error || 'Falha ao criar reserva.');
      }
    } catch (error) {
      console.error("Erro ao criar reserva:", error);
      // Retorna a mensagem de erro para ser exibida na UI.
      return Promise.reject(error.message);
    }
  }

  async function confirmReservation(reservationId) {
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch(`http://localhost:5000/api/reservations/${reservationId}`, {
        method: 'PUT', // A rota agora responde a PUT
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        await fetchAllUserReservations();
        return true;
      } else { throw new Error(data.error); }
    } catch (error) {
      return Promise.reject(error.message);
    }
  }

  async function fetchMyWaitlist() {
    if (!authStore.token) return;
    try {
      const response = await fetch('http://localhost:5000/api/my-waitlist', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        userReservations.waiting = [...data];
      } else { throw new Error(data.error); }
    } catch (error) {
      console.error("Erro ao buscar fila de espera:", error);
      userReservations.waiting = [];
    }
  }

  async function joinWaitlist(restaurantId) {
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch('http://localhost:5000/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${authStore.token}` },
        body: JSON.stringify({ restaurantId })
      });
      const data = await response.json();
      if (response.ok) {
        await fetchMyWaitlist(); // Atualiza a lista após entrar na fila
        return true;
      } else { throw new Error(data.error); }
    } catch (error) {
      return Promise.reject(error.message);
    }
  }

  async function cancelReservation(reservationId) {
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch(`http://localhost:5000/api/reservations/${reservationId}`, {
        method: 'DELETE', // A rota agora responde a DELETE
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        await fetchAllUserReservations();
        return true;
      } else { throw new Error(data.error); }
    } catch (error) {
      return Promise.reject(error.message);
    }
  }

  async function leaveWaitlist(restaurantId) {
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch(`http://localhost:5000/api/waitlist/${restaurantId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        // Atualiza as listas após sair da fila
        await fetchAllUserReservations(); 
        return true;
      } else { 
        throw new Error(data.error || 'Falha ao sair da fila de espera.'); 
      }
    } catch (error) {
      return Promise.reject(error.message);
    }
  }

   /**
   * Atualiza o status de uma reserva (para 'confirmed' ou 'cancelled').
   * @param {number} reservationId - O ID da reserva.
   * @param {string} status - O novo status ('confirmed' ou 'cancelled').
   */
  async function updateReservationStatus(reservationId, status) {
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch(`http://localhost:5000/api/reservations/${reservationId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({ status: status }) // Envia o novo status no corpo do pedido
      });
      const data = await response.json();
      if (response.ok) {
        await fetchAllUserReservations(); // Atualiza a lista
        return true;
      } else {
        throw new Error(data.error || 'Falha ao atualizar o status da reserva.');
      }
    } catch (error) {
      return Promise.reject(error.message);
    }
  }

  return {
    userReservations,
    fetchAllUserReservations,
    createReservation,
    joinWaitlist,
    cancelReservation,
    leaveWaitlist,
    confirmReservation,
    updateReservationStatus
  }
});