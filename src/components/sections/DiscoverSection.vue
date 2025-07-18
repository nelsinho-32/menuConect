<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">📍 Descubra Novos Lugares</h2>
        <div class="horizontal-scroll-container">
            <RestaurantCard v-for="rest in restaurants" :key="rest.id" :restaurant="rest" />
        </div>
    </section>
</template>

<script setup>
import { reactive } from 'vue';
import RestaurantCard from '../RestaurantCard.vue';

const restaurants = reactive([
    { id: 1, name: "La Trattoria", cuisine: "Italiana", imageUrl: "https://placehold.co/800x600/ef4444/ffffff?text=Restaurante+Italiano" },
    { id: 2, name: "Mar Aberto", cuisine: "Frutos do Mar", imageUrl: "https://placehold.co/800x600/3b82f6/ffffff?text=Frutos+do+Mar" },
    { id: 3, name: "Pampa Grill", cuisine: "Churrascaria", imageUrl: "https://placehold.co/800x600/f97316/ffffff?text=Churrascaria" }
]);
</script>