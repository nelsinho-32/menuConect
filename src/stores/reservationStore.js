import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client'; // Importa o nosso novo assistente de API

export const useReservationStore = defineStore('reservations', () => {
  // --- STATE ---
  const userReservations = reactive({
    booked: [],
    waiting: []
  });

  // --- ACTIONS ---

  /**
   * Busca todas as reservas e filas de espera do usuário.
   */
  async function fetchAllUserReservations() {
    // Executa as duas chamadas em paralelo para maior eficiência
    await Promise.all([
      fetchMyReservations(),
      fetchMyWaitlist()
    ]);
  }

  /**
   * Busca as reservas ativas do usuário na API.
   */
  async function fetchMyReservations() {
    try {
      const response = await apiClient('/my-reservations');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar reservas.');
      }
      userReservations.booked = [...data];
    } catch (error) {
      console.error("Erro ao buscar as minhas reservas:", error.message);
      userReservations.booked = []; // Limpa em caso de erro
    }
  }

  /**
   * Busca as filas de espera do usuário na API.
   */
  async function fetchMyWaitlist() {
    try {
      const response = await apiClient('/my-waitlist');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar fila de espera.');
      }
      userReservations.waiting = [...data];
    } catch (error) {
      console.error("Erro ao buscar fila de espera:", error.message);
      userReservations.waiting = [];
    }
  }

  /**
   * Cria uma nova reserva.
   * @param {object} reservationData - Dados da reserva.
   */
  async function createReservation(reservationData) {
    try {
      const response = await apiClient('/reservations', {
        method: 'POST',
        body: JSON.stringify(reservationData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao criar reserva.');
      }
      await fetchAllUserReservations(); // Atualiza a lista
      return data; // Retorna os dados de sucesso (ex: { reservationId: ... })
    } catch (error) {
      console.error("Erro ao criar reserva:", error.message);
      return Promise.reject(error.message);
    }
  }
  
  /**
   * Atualiza o status de uma reserva (geralmente para 'confirmed').
   * @param {number} reservationId - O ID da reserva.
   * @param {string} status - O novo status.
   */
  async function updateReservationStatus(reservationId, status) {
    try {
      const response = await apiClient(`/reservations/${reservationId}/status`, {
        method: 'PUT',
        body: JSON.stringify({ status: status })
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao atualizar status.');
      }
      await fetchAllUserReservations(); // Atualiza a lista para refletir a mudança
      return true;
    } catch (error) {
      return Promise.reject(error.message);
    }
  }
  
  /**
   * Cancela (apaga) uma reserva.
   * @param {number} reservationId - O ID da reserva a ser cancelada.
   */
  async function cancelReservation(reservationId) {
    try {
        const response = await apiClient(`/reservations/${reservationId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Falha ao cancelar reserva.');
        }
        await fetchAllUserReservations(); // Atualiza a lista
        return true;
    } catch (error) {
        return Promise.reject(error.message);
    }
  }

  /**
   * Adiciona o usuário a uma fila de espera.
   * @param {number} restaurantId - O ID do restaurante.
   */
  async function joinWaitlist(restaurantId) {
    try {
        const response = await apiClient('/waitlist', {
            method: 'POST',
            body: JSON.stringify({ restaurantId })
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Falha ao entrar na fila de espera.');
        }
        await fetchMyWaitlist(); // Atualiza apenas a lista de espera
        return true;
    } catch (error) {
        return Promise.reject(error.message);
    }
  }

  /**
   * Remove o usuário de uma fila de espera.
   * @param {number} restaurantId - O ID do restaurante.
   */
  async function leaveWaitlist(restaurantId) {
    try {
        const response = await apiClient(`/waitlist/${restaurantId}`, {
            method: 'DELETE'
        });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.error || 'Falha ao sair da fila de espera.');
        }
        await fetchMyWaitlist(); // Atualiza apenas a lista de espera
        return true;
    } catch (error) {
        return Promise.reject(error.message);
    }
  }

  return {
    userReservations,
    fetchAllUserReservations,
    createReservation,
    updateReservationStatus,
    cancelReservation,
    joinWaitlist,
    leaveWaitlist
  };
});