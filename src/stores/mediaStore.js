// src/stores/mediaStore.js
import { reactive } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client';
import { useManagementStore } from './managementStore';

export const useMediaStore = defineStore('media', () => {
  const state = reactive({
    items: [],
    isLoading: false,
    error: null,
  });

  const managementStore = useManagementStore();

  async function fetchMedia() {
    const restaurantId = managementStore.managedRestaurantId;
    if (!restaurantId) return;

    state.isLoading = true;
    state.error = null;
    try {
      const response = await apiClient(`/management/media?restaurant_id=${restaurantId}`);
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      state.items = data;
    } catch (err) {
      state.error = err.message;
    } finally {
      state.isLoading = false;
    }
  }

  async function uploadMedia(file) {
    const restaurantId = managementStore.managedRestaurantId;
    if (!restaurantId || !file) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('restaurantId', restaurantId);

    try {
      // Usamos o apiClient, que já está corrigido para lidar com FormData
      const response = await apiClient('/management/media', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error);
      
      // Adiciona a nova imagem no início da lista para feedback imediato
      state.items.unshift(data);
      return data;
    } catch (err) {
      console.error("Erro no upload:", err);
      return Promise.reject(err.message);
    }
  }

  async function deleteMedia(mediaId) {
    try {
      const response = await apiClient(`/management/media/${mediaId}`, {
        method: 'DELETE',
      });
      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error);
      }
      // Remove a imagem da lista local
      state.items = state.items.filter(item => item.id !== mediaId);
      return true;
    } catch (err) {
      console.error("Erro ao excluir:", err);
      return Promise.reject(err.message);
    }
  }

  return { state, fetchMedia, uploadMedia, deleteMedia };
});