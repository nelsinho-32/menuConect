<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 class="text-3xl font-bold mb-8">Nossos Restaurantes Parceiros</h1>
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
defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant']);
</script>