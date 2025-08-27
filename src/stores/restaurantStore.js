import { reactive, computed } from 'vue';
import { defineStore } from 'pinia';
import apiClient from '@/api/client'; // Importa o nosso assistente de API

export const useRestaurantStore = defineStore('restaurants', () => {
  const restaurants = reactive([]);
  const reviews = reactive([]);

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

       // Para cada restaurante, percorre o seu menu e adiciona as informações necessárias a cada prato.
      const processedData = dataFromAPI.map(restaurant => {
        if (restaurant.menu) {
          restaurant.menu = restaurant.menu.map(dish => ({
            ...dish,
            restaurantId: restaurant.id,
            restaurantName: restaurant.name
          }));
        }
        return restaurant;
      });
      
      restaurants.length = 0;
      restaurants.push(...processedData);
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

  /**
   * Atualiza o status de uma mesa específica localmente para feedback visual imediato.
   */
  function updateTableStatus({ restaurantId, tableId, newStatus }) {
    const restaurant = restaurants.find(r => r.id === restaurantId);
    if (restaurant && restaurant.tables) {
      const table = restaurant.tables.find(t => t.id === tableId);
      if (table) {
        table.status = newStatus;
      }
    }
  }

  /**
   * Exclui um prato. Requer autenticação de empresa/admin.
   */
  async function deleteDish(dishId) {
    try {
      const response = await apiClient(`/dishes/${dishId}`, {
        method: 'DELETE',
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao excluir o prato.');
      }
      // Atualiza a lista de restaurantes para refletir a exclusão
      await fetchRestaurantsFromAPI(); 
      return true;
    } catch (error) {
      console.error("Erro ao excluir prato via API:", error.message);
      return Promise.reject(error.message);
    }
  }

  /**
   * Busca todas as avaliações para um restaurante específico.
   */
  async function fetchReviewsForRestaurant(restaurantId) {
    try {
      const response = await apiClient(`/restaurants/${restaurantId}/reviews`);
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao buscar as avaliações.');
      }
      reviews.length = 0; // Limpa a lista antiga
      reviews.push(...data); // Preenche com as novas avaliações
    } catch (error) {
      console.error("Erro ao buscar avaliações:", error.message);
    }
  }

  /**
   * Submete uma nova avaliação para um restaurante.
   */
  async function submitReview(reviewData) {
    try {
      const response = await apiClient('/reviews', {
        method: 'POST',
        body: JSON.stringify(reviewData)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || 'Falha ao submeter a avaliação.');
      }
      // Após submeter, recarrega a lista de restaurantes (para atualizar a nota média)
      // e as avaliações do restaurante específico.
      await fetchRestaurantsFromAPI();
      await fetchReviewsForRestaurant(reviewData.restaurantId);
      return true;
    } catch (error) {
      console.error("Erro ao submeter avaliação:", error.message);
      return Promise.reject(error.message);
    }
  }

  return {
    restaurants,
    reviews,
    allDishes,
    featuredRestaurants,
    searchableItems,
    fetchRestaurantsFromAPI,
    addRestaurant,
    addDish,
    updateRestaurantMap,
    updateTableStatus,
    deleteDish, 
    fetchReviewsForRestaurant,
    submitReview,  
  };
});