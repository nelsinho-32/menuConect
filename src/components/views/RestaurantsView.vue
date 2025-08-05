<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold">Nossos Restaurantes Parceiros</h1>
            <button @click="$emit('openAddRestaurantModal')" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 flex items-center gap-2">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.5 6a.5.5 0 0 0-1 0v1.5H6a.5.5 0 0 0 0 1h1.5V10a.5.5 0 0 0 1 0V8.5H10a.5.5 0 0 0 0-1H8.5V6z"/>
                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10 0H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
                </svg>
                Adicionar Restaurante
            </button>
            </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <RestaurantCard 
                v-for="rest in restaurants" 
                :key="rest.id" 
                :restaurant="rest"
                :is-favorited="favoriteRestaurants.has(rest.id)"
                @toggle-favorite="restaurant => $emit('toggleFavorite', restaurant)"
                @request-reservation="restaurant => $emit('requestReservation', restaurant)"
                @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
            />
        </div>
    </div>
</template>

<script setup>
import RestaurantCard from '../RestaurantCard.vue';

defineProps({
    restaurants: { type: Array, required: true },
    favoriteRestaurants: { type: Set, required: true }
});

// Emite um evento para o componente pai (App.vue) para abrir a modal
defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant', 'openAddRestaurantModal']);
</script>