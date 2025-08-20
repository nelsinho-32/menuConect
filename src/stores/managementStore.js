import { reactive, ref } from 'vue'; // <-- CORREÇÃO: Faltava importar 'ref'
import { defineStore } from 'pinia';
import { useAuthStore } from './authStore';
import { useRestaurantStore } from './restaurantStore';
import apiClient from '@/api/client'; // <-- CORREÇÃO: Usar o apiClient para autenticação

export const useManagementStore = defineStore('management', () => {
  const authStore = useAuthStore();
  const restaurantStore = useRestaurantStore();

  const state = reactive({
    reservations: [],
    waitlist: [],
    financials: { dailySales: 0, mostPopularDish: "N/A" },
    selectedTableDetails: null,
    isLoading: false,
    error: null,
  });

  // Guarda o ID do restaurante que está a ser visto no painel
  const managedRestaurantId = ref(null);

  /**
   * Define qual restaurante está a ser gerido e busca os seus dados.
   */
  async function setManagedRestaurant(restaurantId) {
    managedRestaurantId.value = restaurantId;
    await fetchManagementData();
  }

  /**
   * Busca os detalhes completos de uma sessão ativa ou de uma reserva para uma mesa.
   */
  async function fetchTableDetails(tableId) {
    if (!managedRestaurantId.value) return;
    state.isLoading = true;
    state.selectedTableDetails = null;
    try {
      // CORREÇÃO: A rota estava errada, agora busca os detalhes da sessão
      const url = `/management/sessions/table/${tableId}?restaurantId=${managedRestaurantId.value}`;
      const response = await apiClient(url);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.selectedTableDetails = data;
    } catch (err) {
      console.error("Erro ao buscar detalhes da mesa:", err);
      state.selectedTableDetails = { error: err.message };
    } finally {
      state.isLoading = false;
    }
  }

  /**
   * Busca todos os dados de gestão para o restaurante selecionado.
   */
  async function fetchManagementData() {
    // Usa o ID guardado na store, que foi definido por setManagedRestaurant
    const idToFetch = managedRestaurantId.value;
    if (!idToFetch) {
        // Se nenhum restaurante foi selecionado ainda, não faz nada.
        return;
    }

    state.isLoading = true;
    state.error = null;
    try {
      const reservationsUrl = `/management/reservations?restaurant_id=${idToFetch}`;
      const waitlistUrl = `/management/waitlist?restaurant_id=${idToFetch}`;
      const financialsUrl = `/management/financials?restaurant_id=${idToFetch}`;

      const [resReservations, resWaitlist, resFinancials] = await Promise.all([
        apiClient(reservationsUrl),
        apiClient(waitlistUrl),
        apiClient(financialsUrl)
      ]);

      if (!resReservations.ok || !resWaitlist.ok || !resFinancials.ok) {
        throw new Error("Falha ao buscar os dados de gestão.");
      }

      state.reservations = await resReservations.json();
      state.waitlist = await resWaitlist.json();
      state.financials = await resFinancials.json();

    } catch (err) {
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }

  /**
   * Atualiza o status de uma mesa.
   */
  async function updateTableStatus(tableId, newStatus) {
    const validStatuses = ["available", "occupied", "reserved"]; // Valores aceitos pela API
    if (!validStatuses.includes(newStatus)) {
        console.error("Status inválido:", newStatus);
        return Promise.reject("Status inválido.");
    }

    const restaurantId = managedRestaurantId.value;
    if (!restaurantId) {
        return Promise.reject("Nenhum restaurante selecionado para gerir.");
    }

    try {
        const response = await apiClient(`/management/tables/${tableId}/status`, {
            method: 'PUT',
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
    managedRestaurantId,
    setManagedRestaurant,
    fetchManagementData,
    updateTableStatus,
    fetchTableDetails
  };
});