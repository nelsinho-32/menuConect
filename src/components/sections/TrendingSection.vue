<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">🔥 Em Alta</h2>
        <div class="horizontal-scroll-container">
            <DishCard 
                v-for="dish in trendingDishes" 
                :key="dish.id" 
                :dish="dish"
                :is-favorited="favoriteDishes.has(dish.id)"
                @open-action-modal="dish => $emit('openActionModal', dish)"
                @toggle-favorite="dish => $emit('toggleFavorite', dish)"
            />
        </div>
    </section>
</template>

<script setup>
import { reactive } from 'vue';
import DishCard from '../DishCard.vue';

defineProps({
    favoriteDishes: {
        type: Set,
        required: true
    }
});
defineEmits(['openActionModal', 'toggleFavorite']);

const trendingDishes = reactive([
    { id: 1, restaurantName: "Cantina da Nona", dishName: "Lasanha à Bolonhesa", price: "45.50", imageUrl: "https://placehold.co/600x400/f87171/ffffff?text=Lasanha" },
    { id: 2, restaurantName: "Sushi House", dishName: "Combinado Salmão (20pç)", price: "79.90", imageUrl: "https://placehold.co/600x400/60a5fa/ffffff?text=Sushi" },
    { id: 3, restaurantName: "Burger Queen", dishName: "X-Tudo Monstro", price: "38.00", imageUrl: "https://placehold.co/600x400/fbbf24/ffffff?text=Hamb%C3%BArguer" }
]);
</script>