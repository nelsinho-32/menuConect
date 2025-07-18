<template>
  <header class="bg-white shadow-sm sticky top-0 z-40">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <!-- Logo e Menu Principal -->
        <div class="flex items-center space-x-4">
          <div class="relative" ref="menuContainerRef">
            <button @click="isMenuOpen = !isMenuOpen" class="p-2 rounded-full hover:bg-gray-100">
              <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>
            </button>
            <!-- Dropdown do Menu -->
            <div v-if="isMenuOpen" class="absolute top-12 left-0 bg-white w-64 rounded-lg shadow-xl border border-gray-100 py-2 z-50">
              <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">❤️</span> Restaurantes Favoritos
              </a>
              <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">⭐</span> Comidas Favoritas
              </a>
              <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">📅</span> Minhas Reservas
              </a>
               <a href="#" class="flex items-center px-4 py-2 text-gray-700 hover:bg-indigo-50">
                <span class="mr-3">📍</span> Descobrir
              </a>
              <div class="border-t my-2"></div>
              <a href="#" class="flex items-center px-4 py-2 text-red-600 hover:bg-red-50">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="mr-3"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
                Sair
              </a>
            </div>
          </div>
          <div class="flex items-center space-x-2">
            <h1 class="text-2xl font-bold text-gray-900 hidden sm:block">Menu <span class="brand-text">Connect</span></h1>
          </div>
        </div>

        <!-- Barra de Pesquisa Centralizada -->
        <div class="hidden lg:flex flex-1 justify-center px-8">
            <div class="relative w-full max-w-md">
                <input type="text" placeholder="Buscar por prato ou restaurante..." class="w-full bg-gray-100 border border-gray-200 rounded-full py-2 pl-10 pr-4 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-transparent">
                <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-400"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>
                </div>
            </div>
        </div>

        <!-- Ícones da Direita -->
        <div class="flex items-center gap-6">
          <div @click="$emit('toggle-cart', true)" class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600 hover:text-indigo-600"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            <span v-if="cartItemCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">{{ cartItemCount }}</span>
          </div>
          <div class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600 hover:text-indigo-600"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
<script setup>
import { ref, watch, onBeforeUnmount } from 'vue';

defineProps({
  cartItemCount: {
    type: Number,
    required: true
  }
});
defineEmits(['toggle-cart']);

const isMenuOpen = ref(false);
const menuContainerRef = ref(null);

const handleClickOutside = (event) => {
  if (menuContainerRef.value && !menuContainerRef.value.contains(event.target)) {
    isMenuOpen.value = false;
  }
};

watch(isMenuOpen, (isOpen) => {
  if (isOpen) {
    document.addEventListener('click', handleClickOutside);
  } else {
    document.removeEventListener('click', handleClickOutside);
  }
});

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>