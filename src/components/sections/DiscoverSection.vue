<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">📍 {{ title }}</h2>
        <div class="carousel-wrapper">
             <button v-if="!isScrollAtStart" @click="scroll('left')" class="carousel-arrow left-0 -translate-x-1/2">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>

            <div ref="scrollContainer" class="horizontal-scroll-container" @scroll="handleScroll">
                <RestaurantCard 
                    v-for="rest in restaurants" 
                    :key="rest.id" 
                    :restaurant="rest"
                    :is-favorited="favoriteRestaurants.has(rest.id)"
                    @toggle-favorite="restaurant => $emit('toggleFavorite', restaurant)"
                    @request-reservation="restaurant => $emit('requestReservation', restaurant)"
                    @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
                    @open-menu-modal="restaurant => $emit('openMenuModal', restaurant)"
                />
            </div>
            
            <button v-if="!isScrollAtEnd" @click="scroll('right')" class="carousel-arrow right-0 translate-x-1/2">
                 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, onUpdated } from 'vue';
import RestaurantCard from '../RestaurantCard.vue';

defineProps({
    restaurants: { type: Array, required: true },
    favoriteRestaurants: { type: Set, required: true },
    title: { type: String, default: 'Descubra Novos Lugares' }
});

defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant', 'openMenuModal']);

const scrollContainer = ref(null);
const isScrollAtStart = ref(true);
const isScrollAtEnd = ref(false);

const handleScroll = () => {
    const el = scrollContainer.value;
    if (el) {
        // Verifica se o conteúdo é maior que a área visível para decidir se mostra as setas
        const hasOverflow = el.scrollWidth > el.clientWidth;
        isScrollAtStart.value = el.scrollLeft === 0;
        isScrollAtEnd.value = !hasOverflow || Math.abs(el.scrollWidth - el.clientWidth - el.scrollLeft) < 1;
    }
};

const scroll = (direction) => {
    const el = scrollContainer.value;
    if (el) {
        const scrollAmount = el.clientWidth;
        el.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    }
};

onMounted(handleScroll);
onUpdated(handleScroll); // Re-calcula quando os itens mudam
</script>