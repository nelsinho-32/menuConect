import { defineStore } from 'pinia';
import apiClient from '@/api/client'; // Importa o nosso assistente de API

export const useOrderStore = defineStore('orders', () => {

  /**
   * Cria um novo pedido a partir dos itens do carrinho.
   * @param {Array} cartItems - A lista de itens no carrinho.
   * @param {number} totalPrice - O preço total do pedido.
   * @param {number|null} reservationId - O ID da reserva associada, se houver.
   */
  async function createOrder(cartItems, totalPrice, reservationId = null) {
    try {
      const response = await apiClient('/orders', {
        method: 'POST',
        body: JSON.stringify({ 
          cartItems, 
          totalPrice, 
          reservationId // Envia o ID da reserva para o back-end
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao criar o pedido.');
      }
      return true; // Sucesso
    } catch (error) {
      console.error("Erro ao criar pedido:", error.message);
      return Promise.reject(error.message);
    }
  }

  return { createOrder };
});