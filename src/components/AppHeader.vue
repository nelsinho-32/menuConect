<template>
  <header class="bg-white shadow-sm sticky top-0 z-40">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-2">
        <div class="flex items-center gap-2">
          <div class="relative" ref="menuContainerRef">
            <button @click="isMenuOpen = !isMenuOpen" class="p-2 rounded-full hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="text-gray-600">
                <line x1="4" x2="20" y1="12" y2="12" />
                <line x1="4" x2="20" y1="6" y2="6" />
                <line x1="4" x2="20" y1="18" y2="18" />
              </svg>
            </button>
            <div v-if="isMenuOpen"
              class="absolute top-12 left-0 bg-white w-64 rounded-lg shadow-xl border border-gray-100 py-2 z-50">
              <button @click="navigate('myReservations')"
                class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">📅</span> Minhas Reservas
              </button>
              <button @click="navigate('favoriteRestaurants')"
                class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">⭐</span> Restaurantes Favoritos
              </button>
              <button @click="navigate('favoriteDishes')"
                class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">❤️</span> Comidas Favoritas
              </button>
              <button @click="navigate('orderHistory')"
                class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">🧾</span> Histórico de Pedidos
              </button>
              <button v-if="userStore.isCompanyUser()" @click="navigate('tableManagement')"
                class="w-full text-left flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">📊</span> Gestão de Mesas
              </button>
              <div class="border-t my-2"></div>
              <a href="#" class="flex items-center px-4 py-2 text-red-600 hover:bg-red-50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3">
                  <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" />
                  <polyline points="16 17 21 12 16 7" />
                  <line x1="21" y1="12" x2="9" y2="12" />
                </svg>
                Sair
              </a>
            </div>
          </div>
          <button @click="navigate('home')" class="flex-shrink-0">
            <img :src="logo" alt="Menu Connect Logo" class="h-12 w-auto">
          </button>
        </div>

        <nav class="hidden lg:flex items-center gap-6">
          <button @click="navigate('home')"
            :class="['font-semibold', activeView === 'home' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Home</button>
          <button @click="navigate('restaurants')"
            :class="['font-semibold', activeView === 'restaurants' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Restaurantes</button>
          <button @click="navigate('dishes')"
            :class="['font-semibold', activeView === 'dishes' ? 'text-indigo-600' : 'text-gray-600 hover:text-indigo-600']">Comidas</button>
        </nav>

        <div class="flex items-center gap-4">
          <div class="relative w-full max-w-xs hidden md:block" ref="searchContainerRef">
            <input type="text" v-model="searchQuery" @focus="isSearchFocused = true" placeholder="Buscar..."
              class="w-full bg-gray-100 border border-gray-200 rounded-full py-2 pl-10 pr-4 text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500">
            <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="text-gray-400">
                <circle cx="11" cy="11" r="8" />
                <path d="m21 21-4.3-4.3" />
              </svg>
            </div>
            <div v-if="isSearchFocused && filteredResults.length > 0"
              class="absolute top-full mt-2 w-full bg-white rounded-lg shadow-xl border max-h-80 overflow-y-auto z-50">
              <ul>
                <li v-for="item in filteredResults" :key="item.type + item.id"
                  @mousedown.prevent="handleResultClick(item)"
                  class="px-4 py-3 hover:bg-indigo-50 cursor-pointer border-b last:border-b-0">
                  <p class="font-bold text-gray-800">{{ item.name || item.dishName }}</p>
                  <p class="text-sm text-gray-500">{{ item.restaurantName || item.cuisine }}</p>
                </li>
              </ul>
            </div>
          </div>

          <div class="relative" ref="friendsChatContainerRef">
            <button @click="$emit('toggleFriendsChat')" title="Chat de Amigos" class="relative cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                class="text-gray-600 hover:text-indigo-600" viewBox="0 0 16 16">
                <path
                  d="M14 1a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1h-2.5a2 2 0 0 0-1.6.8L8 14.333 6.1 11.8a2 2 0 0 0-1.6-.8H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v8a2 2 0 0 0 2 2h2.5a1 1 0 0 1 .8.4l1.9 2.533a1 1 0 0 0 1.6 0l1.9-2.533a1 1 0 0 1 .8-.4H14a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z" />
              </svg>
            </button>
            <FriendsChatPanel :is-open="isFriendsChatOpen" :friends="friends" />
          </div>

          <div class="relative" ref="notificationsContainerRef">
            <button @click="$emit('toggleNotifications')" title="Notificações" class="relative cursor-pointer">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor"
                class="text-gray-600 hover:text-indigo-600" viewBox="0 0 16 16">
                <path
                  d="M8 16a2 2 0 0 0 2-2H6a2 2 0 0 0 2 2zM8 1.918l-.797.161A4.002 4.002 0 0 0 4 6c0 .628-.134 2.197-.459 3.742-.16.767-.376 1.566-.663 2.258h10.244c-.287-.692-.502-1.49-.663-2.258C12.134 8.197 12 6.628 12 6a4.002 4.002 0 0 0-3.203-3.92L8 1.917zM14.22 12c.223.447.481.801.78 1H1c.299-.199.557-.553.78-1C2.68 10.2 3 8.52 3 6c0-2.42 1.72-4.44 4.005-4.901a1 1 0 1 1 1.99 0A5.002 5.002 0 0 1 13 6c0 2.52.32 4.2.922 6z" />
              </svg>
              <span v-if="notifications.length > 0"
                class="absolute -top-1 -right-1 bg-red-500 text-white text-xs font-bold rounded-full h-4 w-4 flex items-center justify-center text-[10px]">{{
                  notifications.length }}</span>
            </button>
            <NotificationsPanel :is-open="isNotificationsOpen" :notifications="notifications" />
          </div>

          <button @click="navigate('cart')" class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="text-gray-600 hover:text-indigo-600">
              <circle cx="9" cy="21" r="1" />
              <circle cx="20" cy="21" r="1" />
              <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6" />
            </svg>
            <span v-if="cartItemCount > 0"
              class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">{{
                cartItemCount }}</span>
          </button>
          <div class="relative group">
            <button @click="navigate('userProfile')"
              class="relative w-9 h-9 rounded-full flex items-center justify-center focus:outline-none">
              <img :src="user.avatarUrl"
                class="w-full h-full rounded-full object-cover ring-2 ring-indigo-200 group-hover:ring-indigo-400 transition-all">
            </button>
            <div
              class="absolute top-full right-0 mt-2 w-72 bg-white rounded-lg shadow-xl border p-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none group-hover:pointer-events-auto z-50">
              <div class="flex items-center gap-4">
                <img :src="user.avatarUrl" class="w-16 h-16 rounded-full">
                <div>
                  <p class="font-bold text-gray-800">{{ user.name }}</p>
                  <p class="text-sm text-gray-500">{{ user.email }}</p>
                </div>
              </div>
            </div>
          </div>

          <button @click="chatStore.openChat('Ajuda Geral')" title="Abrir Chat de Suporte"
            class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" fill="currentColor"
              class="text-gray-600 hover:text-indigo-600" viewBox="0 0 16 16">
              <path
                d="M8 15c4.418 0 8-3.134 8-7s-3.582-7-8-7-8 3.134-8 7c0 1.76.743 3.37 1.97 4.6-.097 1.016-.417 2.13-.771 2.966-.079.186.074.394.273.362 2.256-.37 3.597-.938 4.18-1.234A9.06 9.06 0 0 0 8 15z" />
            </svg>
          </button>

          <div class="flex items-center gap-2 rounded-full bg-gray-100 p-1 text-sm border">
            <button @click="userStore.setUserRole('cliente')"
              :class="[userStore.userRole === 'cliente' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600', 'px-3 py-1 rounded-full font-semibold transition-all']">
              Cliente
            </button>
            <button @click="userStore.setUserRole('empresa')"
              :class="[userStore.userRole === 'empresa' ? 'bg-indigo-600 text-white shadow' : 'text-gray-600', 'px-3 py-1 rounded-full font-semibold transition-all']">
              Empresa
            </button>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, watch, onBeforeUnmount, computed, onMounted } from 'vue';
import logo from '@/assets/images/LogoMarcaMenu.png';
import { useUserStore } from '@/stores/userStore';
import { useChatStore } from '@/stores/chatStore';
import NotificationsPanel from './NotificationsPanel.vue'; // Importar
import FriendsChatPanel from './FriendsChatPanel.vue';

const chatStore = useChatStore();
const userStore = useUserStore();

const props = defineProps({
  cartItemCount: { type: Number, default: 0 },
  user: { type: Object, required: true },
  searchableItems: { type: Array, default: () => [] },
  activeView: { type: String, default: 'home' },
  isNotificationsOpen: { type: Boolean, default: false },
  isFriendsChatOpen: { type: Boolean, default: false },
  notifications: { type: Array, default: () => [] },
  friends: { type: Array, default: () => [] }
});
const emit = defineEmits(['navigate', 'search-navigate', 'toggleNotifications', 'toggleFriendsChat']);

const isMenuOpen = ref(false);
const menuContainerRef = ref(null);
const searchContainerRef = ref(null);
const searchQuery = ref('');
const isSearchFocused = ref(false);
const notificationsContainerRef = ref(null);
const friendsChatContainerRef = ref(null);

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
  if (notificationsContainerRef.value && !notificationsContainerRef.value.contains(event.target)) {
    if (props.isNotificationsOpen) emit('toggleNotifications');
  }
  if (friendsChatContainerRef.value && !friendsChatContainerRef.value.contains(event.target)) {
    if (props.isFriendsChatOpen) emit('toggleFriendsChat');
  }
};

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>