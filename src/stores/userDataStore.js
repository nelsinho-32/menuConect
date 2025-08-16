import { ref } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client'; // Importa o nosso novo assistente de API

export const useUserDataStore = defineStore('userData', () => {
  // --- STATE ---
  const favoriteRestaurantIds = ref(new Set());
  const favoriteDishIds = ref(new Set());

  // --- ACTIONS ---

  /**
   * Busca todos os dados de preferência do usuário (restaurantes e pratos favoritos).
   */
  async function fetchAllUserData() {
    // Executa as duas chamadas em paralelo para maior eficiência
    await Promise.all([
      fetchFavoriteRestaurants(),
      fetchFavoriteDishes()
    ]);
  }

  /**
   * Busca os IDs dos restaurantes favoritos do usuário na API.
   */
  async function fetchFavoriteRestaurants() {
    try {
      const response = await apiClient('/favorites/restaurants');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar restaurantes favoritos.');
      }
      favoriteRestaurantIds.value = new Set(data);
    } catch (error) {
      console.error("Erro em fetchFavoriteRestaurants:", error.message);
    }
  }

  /**
   * Busca os IDs dos pratos favoritos do usuário na API.
   */
  async function fetchFavoriteDishes() {
    try {
      const response = await apiClient('/favorites/dishes');
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar pratos favoritos.');
      }
      favoriteDishIds.value = new Set(data);
    } catch (error) {
      console.error("Erro em fetchFavoriteDishes:", error.message);
    }
  }

  /**
   * Adiciona ou remove um restaurante dos favoritos.
   * @param {number} restaurantId - O ID do restaurante.
   * @returns {Promise<'added'|'removed'|null>}
   */
  async function toggleFavoriteRestaurant(restaurantId) {
    const isFavorited = favoriteRestaurantIds.value.has(restaurantId);
    const method = isFavorited ? 'DELETE' : 'POST';
    const endpoint = isFavorited ? `/favorites/restaurants/${restaurantId}` : '/favorites/restaurants';

    try {
      const response = await apiClient(endpoint, {
        method: method,
        body: method === 'POST' ? JSON.stringify({ restaurantId }) : null
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.error || 'Falha ao alternar favorito.');
      }

      if (isFavorited) {
        favoriteRestaurantIds.value.delete(restaurantId);
        return 'removed';
      } else {
        favoriteRestaurantIds.value.add(restaurantId);
        return 'added';
      }
    } catch (error) {
      console.error("Erro em toggleFavoriteRestaurant:", error.message);
      return null;
    }
  }

  /**
   * Adiciona ou remove um prato dos favoritos.
   * @param {number} dishId - O ID do prato.
   * @returns {Promise<'added'|'removed'|null>}
   */
  async function toggleFavoriteDish(dishId) {
    const isFavorited = favoriteDishIds.value.has(dishId);
    const method = isFavorited ? 'DELETE' : 'POST';
    const endpoint = isFavorited ? `/favorites/dishes/${dishId}` : '/favorites/dishes';
    
    try {
        const response = await apiClient(endpoint, {
            method: method,
            body: method === 'POST' ? JSON.stringify({ dishId }) : null
        });

        if (!response.ok) {
            const data = await response.json();
            throw new Error(data.error || 'Falha ao alternar favorito.');
        }

        if (isFavorited) {
            favoriteDishIds.value.delete(dishId);
            return 'removed';
        } else {
            favoriteDishIds.value.add(dishId);
            return 'added';
        }
    } catch (error) {
        console.error("Erro em toggleFavoriteDish:", error.message);
        return null;
    }
  }

  return {
    favoriteRestaurantIds,
    favoriteDishIds,
    fetchAllUserData,
    toggleFavoriteRestaurant,
    toggleFavoriteDish
  };
});