// src/stores/whatsappStore.js
import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import { useManagementStore } from './managementStore';

export const useWhatsappStore = defineStore('whatsapp', () => {
  const state = reactive({
    isLoading: false,
    error: null,
    lastSentResult: null
  });

  const managementStore = useManagementStore();

  async function sendMessageToCustomers(message, imageUrl = null) {
    const restaurantId = managementStore.managedRestaurantId;
    if (!restaurantId) {
        state.error = "Nenhum restaurante selecionado.";
        return Promise.reject(state.error);
    }

    state.isLoading = true;
    state.error = null;
    state.lastSentResult = null;

    try {
      const response = await apiClient('/management/whatsapp/send', {
        method: 'POST',
        body: JSON.stringify({
          restaurantId: restaurantId,
          message: message,
          imageUrl: imageUrl // Adiciona a URL da imagem ao pedido
        })
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao enviar a mensagem.');
      }
      state.lastSentResult = data;
      return data; // Retorna os destinatários e a mensagem
    } catch (err) {
      console.error("Erro ao enviar mensagem de marketing:", err.message);
      state.error = err.message;
      return Promise.reject(err.message);
    } finally {
      state.isLoading = false;
    }
  }

  return {
    state,
    sendMessageToCustomers,
  };
});