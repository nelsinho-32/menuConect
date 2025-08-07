import { reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useRestaurantStore = defineStore('restaurants', () => {
  
  // --- STATE (Estado) ---
  const restaurants = reactive([])

  // --- GETTERS (Dados Computados) ---
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

  // --- ACTIONS (Ações) ---
  const getInitialRestaurants = () => [
    { id: 1, name: "Terraço Lisboa Bistrô e Café", cuisine: "Bistrô & Café", imageUrl: '/src/assets/images/TerracoLisboa.webp', logoUrl: '/src/assets/images/LogoLisboa.png', galleryUrls: ['/src/assets/images/VistaPrincipalLisboa.jpg', '/src/assets/images/TerracoLisboaNoite.jpg'], menu: [], isNew: false, mapElements: [ { id: 'bar-1', label: 'Bar', x: 10, y: 10, width: 150, height: 40, fill: '#a8a29e', textColor: '#FFFFFF', rx: 5, rotation: 0, icon_svg: '<path d="M12.5 1a1 1 0 0 1 1 1v5.333a2.5 2.5 0 0 1-5 0V2a1 1 0 0 1 1-1h3zm-.5 4.333V2H9.5v3.333a1.5 1.5 0 0 0 3 0z"/><path d="M13 12.5a1 1 0 0 1 1-1h.5a1 1 0 0 1 0 2h-.5a1 1 0 0 1-1-1zm-10 0a1 1 0 0 1 1-1h.5a1 1 0 0 1 0 2H4a1 1 0 0 1-1-1zM5 6a1 1 0 0 1 1-1h5a1 1 0 0 1 0 2H6a1 1 0 0 1-1-1z"/>' } ], tables: [ { id: 1, x: 50, y: 80, width: 40, height: 40, shape: 'round', status: 'available', images: [] } ], floorPatternId: 'floor-marble' },
    { id: 2, name: "Bruttão Burger Bananeiras", cuisine: "Hamburgueria", imageUrl: '/src/assets/images/BruttaoBurguerBeco.jpg', logoUrl: '/src/assets/images/BruttaoLogo.png', galleryUrls: ['/src/assets/images/BruttaoLocal.jpg'], menu: [], isNew: false, mapElements: [], tables: [], floorPatternId: 'floor-darkwood' },
    { id: 3, name: "Açaiteria", cuisine: "Açaí & Lanches", imageUrl: '/src/assets/images/Acaiteria.jpg', logoUrl: '/src/assets/images/Acaiteria.jpg', galleryUrls: [], menu: [], isNew: false, mapElements: [], tables: [], floorPatternId: 'floor-tiles' }
  ];
  
  function saveRestaurantsToLocalStorage() {
    localStorage.setItem('menuConnectRestaurants', JSON.stringify(restaurants));
  };

  function loadRestaurantsFromLocalStorage() {
    restaurants.length = 0; // Limpa a lista antes de carregar
    const savedRestaurants = localStorage.getItem('menuConnectRestaurants');
    if (savedRestaurants) {
        restaurants.push(...JSON.parse(savedRestaurants));
    } else {
        restaurants.push(...getInitialRestaurants());
    }
    restaurants.forEach(r => {
        if (!r.menu) r.menu = [];
        if (!r.mapElements) r.mapElements = [];
        if (!r.tables) r.tables = [];
        if (!r.floorPatternId) r.floorPatternId = 'floor-marble';
    });
  };

  function addRestaurant(newRestaurantData) {
    const newId = (restaurants.length > 0 ? Math.max(...restaurants.map(r => r.id)) : 0) + 1;
    const restaurantToAdd = {
        id: newId,
        ...newRestaurantData,
        menu: [],
        isNew: true,
        mapElements: [ { id: 'bar-1', label: 'Bar', x: 10, y: 10, width: 150, height: 40, fill: '#a8a29e', textColor: '#FFFFFF', rx: 5, rotation: 0, icon_svg: '...' } ],
        tables: [],
        floorPatternId: 'floor-marble'
    };
    restaurants.push(restaurantToAdd);
    saveRestaurantsToLocalStorage();
    return restaurantToAdd;
  }

  function addDish(newDishData) {
      const parentRestaurant = restaurants.find(r => r.name === newDishData.restaurantName);
      if (!parentRestaurant) return null;

      const newDishId = (allDishes.value.length > 0 ? Math.max(...allDishes.value.map(d => parseInt(d.id) || 0)) : 0) + 1;
      const dishToAdd = {
          id: newDishId,
          name: newDishData.dishName,
          dishName: newDishData.dishName,
          restaurantName: parentRestaurant.name,
          restaurantId: parentRestaurant.id,
          price: parseFloat(newDishData.price),
          imageUrl: newDishData.imageUrl,
          category: newDishData.category,
          description: newDishData.description || 'Um novo prato delicioso.'
      };
      parentRestaurant.menu.push(dishToAdd);
      saveRestaurantsToLocalStorage();
      return dishToAdd;
  }
  
  function updateRestaurantMap(restaurantId, updatedLayout) {
      const restaurantIndex = restaurants.findIndex(r => r.id === restaurantId);
      if (restaurantIndex !== -1) {
          restaurants[restaurantIndex].mapElements = updatedLayout.mapElements;
          restaurants[restaurantIndex].tables = updatedLayout.tables;
          restaurants[restaurantIndex].floorPatternId = updatedLayout.floorPatternId;
          saveRestaurantsToLocalStorage();
      }
  }

  return { 
    restaurants, 
    allDishes, 
    featuredRestaurants,
    searchableItems,
    loadRestaurantsFromLocalStorage, 
    addRestaurant,
    addDish,
    updateRestaurantMap
  }
})