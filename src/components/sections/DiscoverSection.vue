<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">📍 Descubra Novos Lugares</h2>
        <div class="horizontal-scroll-container">
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
    </section>
</template>
<script setup>
import RestaurantCard from '../RestaurantCard.vue';

defineProps({
    restaurants: { type: Array, required: true },
    favoriteRestaurants: { type: Set, required: true }
});
defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant']);
</script>