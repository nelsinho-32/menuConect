<template>
  <header class="bg-white shadow-sm sticky top-0 z-40">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-2">
        <!-- Esquerda: Menu Hambúrguer, Logo -->
        <div class="flex items-center gap-2">
          <div class="relative" ref="menuContainerRef">
            <button @click="isMenuOpen = !isMenuOpen" class="p-2 rounded-full hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
            </button>
            <div v-if="isMenuOpen" class="absolute top-12 left-0 bg-white w-64 rounded-lg shadow-xl border border-gray-100 py-2 z-50">
              <button @click="navigate('myReservations')" class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">📅</span> Minhas Reservas
              </button>
              <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">⭐</span> Restaurantes Favoritos
              </a>
              <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">❤️</span> Comidas Favoritas
              </a>
              <div class="border-t my-2"></div>
              <a href="#" class="flex items-center px-4 py-2 text-red-600 hover:bg-red-50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                Sair
              </a>
            </div>
          </div>
          <button @click="navigate('home')" class="flex items-center space-x-2 flex-shrink-0">
            <h1 class="text-2xl font-bold text-gray-900">Menu <span class="brand-text">Connect</span></h1>
          </button>
        </div>

        <!-- Centro: Navegação Principal (Desktop) -->
        <nav class="hidden lg:flex items-center gap-6">
            <button @click="navigate('home')" :class="['font-semibold', activeView === 'home' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Home</button>
            <button @click="navigate('restaurants')" :class="['font-semibold', activeView === 'restaurants' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Restaurantes</button>
            <button @click="navigate('dishes')" :class="['font-semibold', activeView === 'dishes' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Comidas</button>
        </nav>
        
        <!-- Direita: Pesquisa, Ícones -->
        <div class="flex items-center gap-4">
          <div class="relative w-full max-w-xs hidden md:block" ref="searchContainerRef">
              <input type="text" v-model="searchQuery" @focus="isSearchFocused = true" placeholder="Buscar..." class="w-full bg-gray-100 border border-gray-200 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
              <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
              </div>
              <div v-if="isSearchFocused && filteredResults.length > 0" class="absolute top-full mt-2 w-full bg-white rounded-lg shadow-xl border max-h-80 overflow-y-auto z-50">
                  <ul>
                      <li v-for="item in filteredResults" :key="item.type + item.id" @mousedown.prevent="handleResultClick(item)" class="px-4 py-3 hover:bg-indigo-50 cursor-pointer border-b last:border-b-0">
                          <p class="font-bold text-gray-800">{{ item.name || item.dishName }}</p>
                          <p class="text-sm text-gray-500">{{ item.restaurantName || item.cuisine }}</p>
                      </li>
                  </ul>
              </div>
          </div>
          <button @click="navigate('cart')" class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600 hover:text-indigo-600"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            <span v-if="cartItemCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">{{ cartItemCount }}</span>
          </button>
          <div class="relative group">
            <button @click="navigate('userProfile')" class="relative w-9 h-9 rounded-full flex items-center justify-center focus:outline-none">
              <img :src="user.avatarUrl" class="w-full h-full rounded-full object-cover ring-2 ring-indigo-200 group-hover:ring-indigo-400 transition-all">
            </button>
            <div class="absolute top-full right-0 mt-2 w-72 bg-white rounded-lg shadow-xl border p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none group-hover:pointer-events-auto z-50">
                <div class="flex items-center gap-4">
                    <img :src="user.avatarUrl" class="w-16 h-16 rounded-full">
                    <div>
                        <p class="font-bold text-gray-800">{{ user.name }}</p>
                        <p class="text-sm text-gray-500">{{ user.email }}</p>
                    </div>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
<script setup>
import { ref, watch, onBeforeUnmount, computed, onMounted } from 'vue';

const props = defineProps({
  cartItemCount: { type: Number, default: 0 },
  user: { type: Object, required: true },
  searchableItems: { type: Array, default: () => [] },
  activeView: { type: String, default: 'home' }
});
const emit = defineEmits(['navigate', 'search-navigate']);

const isMenuOpen = ref(false);
const menuContainerRef = ref(null);
const searchContainerRef = ref(null);
const searchQuery = ref('');
const isSearchFocused = ref(false);

const navigate = (viewName) => {
    emit('navigate', viewName);
    isMenuOpen.value = false;
};

const filteredResults = computed(() => {
    if (searchQuery.value.length < 2) return [];
    const lowerCaseQuery = searchQuery.value.toLowerCase();
    return props.searchableItems.filter(item => 
        (item.name && item.name.toLowerCase().includes(lowerCaseQuery)) ||
        (item.dishName && item.dishName.toLowerCase().includes(lowerCaseQuery))
    );
});

const handleResultClick = (item) => {
    emit('search-navigate', item);
    searchQuery.value = '';
    isSearchFocused.value = false;
};

const handleClickOutside = (event) => {
  if (menuContainerRef.value && !menuContainerRef.value.contains(event.target)) {
    isMenuOpen.value = false;
  }
  if (searchContainerRef.value && !searchContainerRef.value.contains(event.target)) {
    isSearchFocused.value = false;
  }
};

onMounted(() => {
    document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>