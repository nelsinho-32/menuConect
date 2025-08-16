// src/stores/orderStore.js

import { defineStore } from 'pinia';
import { useAuthStore } from './authStore';

export const useOrderStore = defineStore('orders', () => {
  const authStore = useAuthStore();

  async function createOrder(cartItems, totalPrice) {
    if (!authStore.token) return Promise.reject("Não autenticado");

    try {
      const response = await fetch('http://localhost:5000/api/orders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify({ cartItems, totalPrice })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao criar o pedido.');
      }
      return true; // Sucesso
    } catch (error) {
      console.error("Erro ao criar pedido:", error);
      return Promise.reject(error.message);
    }
  }

  return { createOrder };
});