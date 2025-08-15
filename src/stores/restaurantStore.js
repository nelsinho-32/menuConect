// src/stores/restaurantStore.js (VERSÃO ATUALIZADA)

import { useAuthStore } from './authStore';
import { reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRestaurantStore = defineStore('restaurants', () => {

  const restaurants = reactive([])


  const allDishes = computed(() => {
    return restaurants.flatMap(r => r.menu ? r.menu.map(item => ({...item, restaurantName: r.name, restaurantId: r.id})) : []);
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

  async function updateRestaurantMap(restaurantId, layoutData) {
  const authStore = useAuthStore(); // Precisa de acesso à authStore
  if (!authStore.token) return Promise.reject("Não autenticado");

  try {
    const response = await fetch(`http://localhost:5000/api/restaurants/${restaurantId}/map`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${authStore.token}`
      },
      body: JSON.stringify(layoutData)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Falha ao salvar o mapa.');
    return true;
  } catch (error) {
    console.error("Erro ao salvar o mapa:", error);
    return Promise.reject(error.message);
  }
}

  // ---- ALTERAÇÃO PRINCIPAL AQUI ----
  // A função agora é 'async' para poder esperar pela resposta da API.
  async function fetchRestaurantsFromAPI() {
    try {
      // Faz o pedido GET para a nossa API Flask que está a correr na porta 5000.
      const response = await fetch('http://localhost:5000/api/restaurants');
      if (!response.ok) {
        throw new Error('A resposta da rede não foi bem-sucedida.');
      }
      const data = await response.json();

      // Limpa a lista atual e preenche com os dados vindos da API.
      restaurants.length = 0;
      restaurants.push(...data);

      // Simula menus e outros dados que ainda não estão no back-end
      // (vamos adicionar isto ao back-end mais tarde!)
      restaurants.forEach(r => {
          if (!r.menu) r.menu = [];
          if (!r.mapElements) r.mapElements = [];
          if (!r.tables) r.tables = [];
          if (!r.floorPatternId) r.floorPatternId = 'floor-marble';
      });

    } catch (error) {
      console.error("Falha ao buscar restaurantes da API:", error);
      // Opcional: Carregar dados de fallback se a API falhar
    }
  };
  // ------------------------------------

  // Funções para adicionar e atualizar continuarão a funcionar,
  // mas por agora só atualizam o estado no frontend.
  // Nos próximos passos, faremos com que elas também chamem a API.

  // ---- NOVA VERSÃO DA FUNÇÃO addRestaurant ----
async function addRestaurant(newRestaurantData) {
  try {
    // Envia os dados do novo restaurante para a API via método POST
    const response = await fetch('http://localhost:5000/api/restaurants', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newRestaurantData),
    });

    if (!response.ok) {
      throw new Error('Falha ao adicionar o restaurante.');
    }

    const result = await response.json();

    // Cria o objeto completo do restaurante com o ID retornado pela API
    const restaurantToAdd = {
      ...newRestaurantData,
      id: result.id, // Usa o ID que o back-end nos deu!
      menu: [],
      isNew: true,
      mapElements: [ { id: 'bar-1', label: 'Bar', x: 10, y: 10, width: 150, height: 40, fill: '#a8a29e', textColor: '#FFFFFF', rx: 5, rotation: 0, icon_svg: '...' } ],
      tables: [],
      floorPatternId: 'floor-marble'
    };

    // Adiciona o novo restaurante à lista no frontend para atualização imediata da UI
    restaurants.push(restaurantToAdd);
    return restaurantToAdd;

  } catch (error) {
    console.error("Erro ao adicionar restaurante via API:", error);
    return null; // Retorna null para indicar que houve um erro
  }
}

  async function addDish(newDishData) {
  try {
    const response = await fetch('http://localhost:5000/api/dishes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newDishData),
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || 'Falha ao adicionar o prato.');
    }

    const result = await response.json();

    // Encontra o restaurante no estado local para adicionar o prato
    const parentRestaurant = restaurants.find(r => r.name === newDishData.restaurantName);
    if (parentRestaurant) {
        const dishToAdd = {
          ...newDishData,
          id: result.id,
          name: newDishData.dishName, // Garante que a propriedade 'name' existe
          price: parseFloat(newDishData.price) // Garante que o preço é um número
        };
        if (!parentRestaurant.menu) {
            parentRestaurant.menu = [];
        }
        parentRestaurant.menu.push(dishToAdd);
        return dishToAdd;
    }
    return null;

  } catch (error) {
    console.error("Erro ao adicionar prato via API:", error);
    return null;
  }
}

  

  function updateTableStatus({ restaurantId, tableId, newStatus }) {
    const restaurant = restaurants.find(r => r.id === restaurantId);
    if (restaurant && restaurant.tables) {
        const table = restaurant.tables.find(t => t.id === tableId);
        if (table) {
            table.status = newStatus;
            // saveRestaurantsToLocalStorage();
        }
    }
  }

  return {
    restaurants,
    allDishes,
    featuredRestaurants,
    searchableItems,
    fetchRestaurantsFromAPI, // Expondo a nova função
    addRestaurant,
    addDish,
    updateRestaurantMap,
    updateTableStatus,
  }
})