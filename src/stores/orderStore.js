import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useOrderStore = defineStore('orders', () => {
  // --- STATE ---
  const orderHistory = reactive([]);

  // --- ACTIONS ---

  /**
   * Busca o histórico de pedidos do usuário logado na API.
   */
  async function fetchHistory() {
    try {
      const response = await apiClient('/my-orders');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar o histórico.');
      }
      // Limpa a lista antiga e preenche com os novos dados
      orderHistory.length = 0;
      orderHistory.push(...data);
    } catch (error) {
      console.error("Erro ao buscar histórico de pedidos:", error.message);
      orderHistory.length = 0; // Garante que a lista fica vazia em caso de erro
    }
  }

/**
   * Cria um novo pedido a partir dos itens do carrinho.
   */
  async function createOrder(cartItems, totalPrice, reservationId = null, splitDetails = null) {
    try {
      const response = await apiClient('/orders', {
        method: 'POST',
        body: JSON.stringify({ 
          cartItems, 
          totalPrice, 
          reservationId,
          split_details: splitDetails // Adiciona o campo para o backend
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao criar o pedido.');
      }
      await fetchHistory();
      return true;
    } catch (error) {
      console.error("Erro ao criar pedido:", error.message);
      return Promise.reject(error.message);
    }
  }

  return { 
    orderHistory,
    fetchHistory,
    createOrder 
  };
});