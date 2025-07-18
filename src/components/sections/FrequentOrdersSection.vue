<template>
     <section class="mb-12">
        <h2 class="section-title mb-6">⭐ Meus Pedidos Frequentes</h2>
        <div class="horizontal-scroll-container">
             <DishCard 
                v-for="dish in frequentDishes" 
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

const frequentDishes = reactive([
    { id: 6, restaurantName: "Burger Queen", dishName: "Batata Frita com Cheddar", price: "22.00", imageUrl: "https://placehold.co/600x400/fca5a5/ffffff?text=Batata+Frita" },
    { id: 7, restaurantName: "Açaí Power", dishName: "Copo de Açaí 500ml", price: "25.00", imageUrl: "https://placehold.co/600x400/c084fc/ffffff?text=A%C3%A7a%C3%AD" },
    { id: 8, restaurantName: "Padaria Pão Quente", dishName: "Pão na Chapa com Requeijão", price: "8.50", imageUrl: "https://placehold.co/600x400/fdba74/ffffff?text=P%C3%A3o" }
]);
</script>