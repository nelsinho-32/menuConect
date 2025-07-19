<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 class="text-3xl font-bold mb-8">Todos os Nossos Pratos</h1>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <DishCard 
                v-for="dish in dishes" 
                :key="dish.id" 
                :dish="dish"
                :is-favorited="favoriteDishes.has(dish.id)"
                @open-action-modal="dish => $emit('openActionModal', dish)"
                @open-dine-options="dish => $emit('openDineOptions', dish)"
                @toggle-favorite="dish => $emit('toggleFavorite', dish)"
            />
        </div>
    </div>
</template>
<script setup>
import DishCard from '../DishCard.vue';
defineProps({
    dishes: { type: Array, required: true },
    favoriteDishes: { type: Set, required: true }
});
defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions']);
</script>