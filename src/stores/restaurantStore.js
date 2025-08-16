import { reactive, computed } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client'; // Importa o nosso assistente de API

export const useRestaurantStore = defineStore('restaurants', () => {
  const restaurants = reactive([]);

  const allDishes = computed(() => {
    return restaurants.flatMap(r => r.menu || []);
  });

  const featuredRestaurants = computed(() => restaurants.filter(r => !r.isNew));

  const searchableItems = computed(() => {
    const items = [];
    restaurants.forEach(r => {
        items.push({ type: 'restaurant', ...r });
        if (r.menu) {
            r.menu.forEach(item => {
                items.push({ type: 'dish', ...item, restaurantName: r.name, restaurantId: r.id });
            });
        }
    });
    return items;
  });

  /**
   * Busca os dados públicos dos restaurantes. Não precisa de autenticação.
   */
  async function fetchRestaurantsFromAPI() {
    try {
      const response = await fetch('http://localhost:5000/api/restaurants');
      if (!response.ok) throw new Error('A resposta da rede não foi bem-sucedida.');
      const dataFromAPI = await response.json();
      
      restaurants.length = 0;
      restaurants.push(...dataFromAPI);
    } catch (error) {
      console.error("Falha ao buscar restaurantes da API:", error);
    }
  }

  /**
   * Adiciona um novo restaurante. Requer autenticação de admin.
   */
  async function addRestaurant(newRestaurantData) {
    try {
      const response = await apiClient('/restaurants', {
        method: 'POST',
        body: JSON.stringify(newRestaurantData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao adicionar o restaurante.');
      }
      await fetchRestaurantsFromAPI(); // Atualiza a lista
      return data;
    } catch (error) {
      console.error("Erro ao adicionar restaurante via API:", error.message);
      return Promise.reject(error.message);
    }
  }

  /**
   * Adiciona um novo prato. Requer autenticação de empresa/admin.
   */
  async function addDish(newDishData) {
    try {
      const response = await apiClient('/dishes', {
        method: 'POST',
        body: JSON.stringify(newDishData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao adicionar o prato.');
      }
      await fetchRestaurantsFromAPI(); // Atualiza a lista completa para refletir o novo prato
      return data;
    } catch (error) {
      console.error("Erro ao adicionar prato via API:", error.message);
      return Promise.reject(error.message);
    }
  }
  
  // A sua função updateRestaurantMap para salvar no banco de dados.
  async function updateRestaurantMap(restaurantId, layoutData) {
    try {
        const response = await apiClient(`/restaurants/${restaurantId}/map`, {
            method: 'PUT',
            body: JSON.stringify(layoutData)
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Falha ao salvar o mapa.');
        return true;
    } catch (error) {
        console.error("Erro ao salvar o mapa:", error.message);
        return Promise.reject(error.message);
    }
  }

  return {
    restaurants,
    allDishes,
    featuredRestaurants,
    searchableItems,
    fetchRestaurantsFromAPI,
    addRestaurant,
    addDish,
    updateRestaurantMap
  };
});