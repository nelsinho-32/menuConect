import { reactive } from 'vue';
import { defineStore } from 'pinia';
import { useAuthStore } from './authStore';
import { useRestaurantStore } from './restaurantStore'; // <-- 1. IMPORTAR A STORE DE RESTAURANTES

export const useManagementStore = defineStore('management', () => {
  const authStore = useAuthStore();
  const restaurantStore = useRestaurantStore(); // <-- 2. INICIALIZAR A STORE

  const state = reactive({
    reservations: [],
    waitlist: [],
    isLoading: false,
    financials: { dailySales: 0, mostPopularDish: "N/A" },
    error: null,
  });

  async function fetchManagementData(restaurantId = null) {
    if (!authStore.isAuthenticated) return;
    state.isLoading = true;
    state.error = null;
    try {
      let idToFetch = restaurantId || authStore.currentUser?.restaurant_id;
      if (authStore.currentUser?.role === 'admin' && !idToFetch) {
        if (restaurantStore.restaurants.length > 0) {
          idToFetch = restaurantStore.restaurants[0].id;
        } else {
          state.isLoading = false;
          return;
        }
      }
      if (!idToFetch) throw new Error("Nenhum restaurante encontrado para gerir.");

      const reservationsUrl = `http://localhost:5000/api/management/reservations?restaurant_id=${idToFetch}`;
      const waitlistUrl = `http://localhost:5000/api/management/waitlist?restaurant_id=${idToFetch}`;
      const financialsUrl = `http://localhost:5000/api/management/financials?restaurant_id=${idToFetch}`; // <-- NOVA URL

      const [resReservations, resWaitlist, resFinancials] = await Promise.all([
        fetch(reservationsUrl, { headers: { 'Authorization': `Bearer ${authStore.token}` } }),
        fetch(waitlistUrl, { headers: { 'Authorization': `Bearer ${authStore.token}` } }),
        fetch(financialsUrl, { headers: { 'Authorization': `Bearer ${authStore.token}` } }) // <-- NOVA CHAMADA
      ]);

      if (!resReservations.ok || !resWaitlist.ok || !resFinancials.ok) {
        throw new Error("Falha ao buscar os dados de gestão.");
      }

      state.reservations = await resReservations.json();
      state.waitlist = await resWaitlist.json();
      state.financials = await resFinancials.json(); // <-- SALVA OS DADOS FINANCEIROS

    } catch (err) {
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }

    async function updateTableStatus(restaurantId, tableId, newStatus) { // <-- Aceita restaurantId
    if (!authStore.token) return Promise.reject("Não autenticado");
    try {
      const response = await fetch(`http://localhost:5000/api/management/tables/${tableId}/status`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        // CORREÇÃO: Envia o restaurantId junto com o status
        body: JSON.stringify({ 
            status: newStatus,
            restaurantId: restaurantId 
        })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || 'Falha ao atualizar status da mesa.');
      
      return true;
    } catch (error) {
      console.error("Erro ao atualizar status da mesa:", error);
      return Promise.reject(error.message);
    }
  }

  return {
    state,
    fetchManagementData,
    updateTableStatus
  }
});