<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold mb-8">⭐ Meus Restaurantes Favoritos</h1>

        <div v-if="favoriteRestaurants.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não adicionou nenhum restaurante aos seus favoritos.</p>
            <p class="text-sm text-gray-400 mt-2">Clique na estrela ⭐ nos cartões dos restaurantes para os adicionar aqui!</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <RestaurantCard 
                v-for="rest in favoriteRestaurants" 
                :key="rest.id" 
                :restaurant="rest"
                :is-favorited="true"
                @toggle-favorite="restaurant => $emit('toggleFavorite', restaurant)"
                @request-reservation="restaurant => $emit('requestReservation', restaurant)"
                @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
                @open-menu-modal="restaurant => $emit('openMenuModal', restaurant)"
            />
        </div>
    </div>
</template>

<script setup>
import RestaurantCard from '../RestaurantCard.vue';

defineProps({
    favoriteRestaurants: { type: Array, required: true }
});

defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant', 'backToMain', 'openMenuModal']);
</script>