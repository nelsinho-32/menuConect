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
                @open-dine-options="dish => $emit('openDineOptions', dish)"
                @toggle-favorite="dish => $emit('toggleFavorite', dish)"
            />
        </div>
    </section>
</template>

<script setup>
import DishCard from '../DishCard.vue';

defineProps({
    trendingDishes: { type: Array, required: true },
    favoriteDishes: { type: Set, required: true }
});
defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions']);
</script>