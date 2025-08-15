import { ref } from 'vue'
import { defineStore } from 'pinia'
import { useAuthStore } from './authStore'

export const useUserDataStore = defineStore('userData', () => {
  const authStore = useAuthStore();

  // --- STATE ---
  // Usamos um Set para performance, guardando apenas os IDs dos restaurantes favoritos.
  const favoriteRestaurantIds = ref(new Set());
   const favoriteDishIds = ref(new Set());

  // --- ACTIONS ---

   async function fetchAllUserData() {
    if (!authStore.token) return;
    await fetchFavoriteRestaurants();
    await fetchFavoriteDishes(); // <-- CHAMADA NOVA
  }

  // --- FUNÇÃO PARA BUSCAR PRATOS FAVORITOS ---
  async function fetchFavoriteDishes() {
    if (!authStore.token) return;
    try {
      const response = await fetch('http://localhost:5000/api/favorites/dishes', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        favoriteDishIds.value = new Set(data);
      } else { throw new Error(data.error); }
    } catch (error) {
      console.error("Erro ao buscar pratos favoritos:", error);
    }
  }

  // --- FUNÇÃO PARA ADICIONAR/REMOVER PRATO FAVORITO ---
  async function toggleFavoriteDish(dishId) {
    if (!authStore.token) return null;

    const isFavorited = favoriteDishIds.value.has(dishId);
    const url = `http://localhost:5000/api/favorites/dishes${isFavorited ? `/${dishId}` : ''}`;
    const method = isFavorited ? 'DELETE' : 'POST';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: method === 'POST' ? JSON.stringify({ dishId }) : null
      });
      
      const data = await response.json();
      if (response.ok) {
        if (isFavorited) {
          favoriteDishIds.value.delete(dishId);
          return 'removed';
        } else {
          favoriteDishIds.value.add(dishId);
          return 'added';
        }
      } else { throw new Error(data.error); }
    } catch (error) {
      console.error("Erro ao alternar prato favorito:", error);
      return null;
    }
  }

  /**
   * Busca os IDs dos restaurantes favoritos do usuário na API e preenche o nosso Set.
   */
  async function fetchFavoriteRestaurants() {
    if (!authStore.token) return;

    try {
      const response = await fetch('http://localhost:5000/api/favorites/restaurants', {
        headers: { 'Authorization': `Bearer ${authStore.token}` }
      });
      const data = await response.json();
      if (response.ok) {
        // 'data' é uma lista de IDs, ex: [1, 5, 12]
        favoriteRestaurantIds.value = new Set(data);
      } else {
        throw new Error(data.error || 'Falha ao buscar favoritos.');
      }
    } catch (error) {
      console.error("Erro ao buscar restaurantes favoritos:", error);
    }
  }

    /**
    * Adiciona ou remove um restaurante dos favoritos, comunicando com a API.
    * @param {number} restaurantId - O ID do restaurante a ser favoritado/desfavoritado.
    * @returns {Promise<'added'|'removed'|null>} - A ação realizada ou nulo em caso de erro.
    */
  async function toggleFavoriteRestaurant(restaurantId) {
    if (!authStore.token) return;

    const isFavorited = favoriteRestaurantIds.value.has(restaurantId);
    const url = `http://localhost:5000/api/favorites/restaurants${isFavorited ? `/${restaurantId}` : ''}`;
    const method = isFavorited ? 'DELETE' : 'POST';

    try {
      const response = await fetch(url, {
        method: method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        // O body só é necessário para o POST
        body: method === 'POST' ? JSON.stringify({ restaurantId }) : null
      });

      const data = await response.json();
          if (response.ok) {
            if (isFavorited) {
              favoriteRestaurantIds.value.delete(restaurantId);
              return 'removed';
            } else {
              favoriteRestaurantIds.value.add(restaurantId);
              return 'added';
            }
          } else {
            throw new Error(data.error || 'Falha ao atualizar favorito.');
          }
        } catch (error) {
          console.error("Erro ao alternar favorito:", error);
          return null; // Retorna nulo em caso de erro
        }
  }

  return {
    favoriteRestaurantIds, 
    favoriteDishIds, 
    fetchAllUserData, 
    fetchFavoriteRestaurants,
    fetchFavoriteDishes, 
    toggleFavoriteRestaurant,
    toggleFavoriteDish,
  }
})