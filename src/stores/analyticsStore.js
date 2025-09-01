import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import { useManagementStore } from './managementStore';

export const useAnalyticsStore = defineStore('analytics', () => {
  // --- STATE ---
  const state = reactive({
    salesHistory: [],
    topDishes: [],
    // Adicione um novo estado para a análise de sentimento
    sentimentAnalysis: { sentiments: [], topics: {} },
    isLoading: false,
    error: null
  });

  const managementStore = useManagementStore();

  // --- ACTIONS ---
  async function fetchAnalyticsData(period = 'last7days') {
    const restaurantId = managementStore.managedRestaurantId;
    if (!restaurantId) {
      state.error = "Nenhum restaurante selecionado para análise.";
      return;
    }

    state.isLoading = true;
    state.error = null;

    try {
      const response = await apiClient(`/management/analytics?restaurant_id=${restaurantId}&period=${period}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar os dados de análise.');
      }

      state.salesHistory = data.sales_history;
      state.topDishes = data.top_dishes;
      // Preenche o novo estado com os dados da API
      state.sentimentAnalysis = data.sentiment_analysis || { sentiments: [], topics: {} };

    } catch (err) {
      console.error("Erro ao buscar dados de análise:", err.message);
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }

  return {
    state,
    fetchAnalyticsData
  };
});