import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import { useManagementStore } from './managementStore';

export const usePromotionStore = defineStore('promotions', () => {
  // --- STATE ---
  const state = reactive({
    promotions: [],
    isLoading: false,
    error: null
  });

  const managementStore = useManagementStore();

  // --- ACTIONS ---

  /**
   * Busca todas as promoções (ativas e inativas) para o restaurante a ser gerido.
   */
  async function fetchPromotions() {
    const restaurantId = managementStore.managedRestaurantId;
    if (!restaurantId) return;

    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient(`/management/promotions?restaurant_id=${restaurantId}`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar as promoções.');
      }
      state.promotions = data;
    } catch (err) {
      console.error("Erro ao buscar promoções:", err.message);
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }

  /**
   * Cria uma nova promoção.
   * @param {object} promotionData - Os dados da nova promoção.
   */
  async function createPromotion(promotionData) {
    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient('/management/promotions', {
        method: 'POST',
        body: JSON.stringify(promotionData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao criar a promoção.');
      }
      // Após criar com sucesso, atualiza a lista de promoções
      await fetchPromotions();
      return true; // Sucesso
    } catch (err) {
      console.error("Erro ao criar promoção:", err.message);
      state.error = err.message;
      return Promise.reject(err.message);
    } finally {
      state.isLoading = false;
    }
  }

  return {
    state,
    fetchPromotions,
    createPromotion
  };
});