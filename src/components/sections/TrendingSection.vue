<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">🔥 Em Alta</h2>
        <div class="carousel-wrapper">
            <button v-if="!isScrollAtStart" @click="scroll('left')" class="carousel-arrow left-0 -translate-x-1/2">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>

            <div ref="scrollContainer" class="horizontal-scroll-container" @scroll="handleScroll">
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

            <button v-if="!isScrollAtEnd" @click="scroll('right')" class="carousel-arrow right-0 translate-x-1/2">
                 <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted, onUpdated } from 'vue';
import DishCard from '../DishCard.vue';

defineProps({
    trendingDishes: { type: Array, required: true },
    favoriteDishes: { type: Set, required: true }
});
defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions']);

const scrollContainer = ref(null);
const isScrollAtStart = ref(true);
const isScrollAtEnd = ref(false);

const handleScroll = () => {
    const el = scrollContainer.value;
    if (el) {
        isScrollAtStart.value = el.scrollLeft === 0;
        isScrollAtEnd.value = Math.abs(el.scrollWidth - el.clientWidth - el.scrollLeft) < 1;
    }
};

const scroll = (direction) => {
    const el = scrollContainer.value;
    if (el) {
        // AQUI ESTÁ A CORREÇÃO: Move a largura total da área visível
        const scrollAmount = el.clientWidth;
        el.scrollBy({ left: direction === 'left' ? -scrollAmount : scrollAmount, behavior: 'smooth' });
    }
};

onMounted(handleScroll);
onUpdated(handleScroll);
</script>