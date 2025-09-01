// src/stores/listStore.js
import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';

export const useListStore = defineStore('lists', () => {
  const state = reactive({
    myLists: [],
    selectedListDetails: null, 
    isLoading: false,
    error: null
  });

  async function fetchMyLists() {
    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient('/my-lists');
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.myLists = data;
    } catch (err) {
      state.error = err.message;
      console.error("Erro ao buscar listas:", err.message);
    } finally {
      state.isLoading = false;
    }
  }

  async function createList(listData) {
    try {
      const response = await apiClient('/lists', {
        method: 'POST',
        body: JSON.stringify(listData)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      await fetchMyLists(); // Atualiza a lista após a criação
      return data;
    } catch (error) {
      console.error("Erro ao criar lista:", error.message);
      return Promise.reject(error.message);
    }
  }

  async function addItemToList(listId, item) {
    try {
      const payload = {
        restaurantId: item.type === 'restaurant' ? item.id : null,
        dishId: item.type === 'dish' ? item.id : null
      };
      const response = await apiClient(`/lists/${listId}/items`, {
        method: 'POST',
        body: JSON.stringify(payload)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      await fetchMyLists(); // Atualiza a contagem de itens
      return data;
    } catch (error) {
      console.error("Erro ao adicionar item à lista:", error.message);
      return Promise.reject(error.message);
    }
  }

   async function fetchListDetails(listId) {
    state.isLoading = true;
    state.error = null;
    state.selectedListDetails = null;
    try {
      const response = await apiClient(`/lists/${listId}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.selectedListDetails = data;
    } catch (err) {
      state.error = err.message;
      console.error("Erro ao buscar detalhes da lista:", err.message);
    } finally {
      state.isLoading = false;
    }
  }

  return {
    state,
    fetchMyLists,
    createList,
    addItemToList,
    fetchListDetails 
  };
});