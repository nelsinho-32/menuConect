<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <FrequentOrdersSection 
            v-if="favoritedDishesList.length > 0"
            title="Meus Pratos Favoritos"
            :dishes="favoritedDishesList"
            :favorite-dishes="favoriteDishes"
            @open-action-modal="dish => $emit('openActionModal', dish)"
            @open-dine-options="dish => $emit('openDineOptions', dish)"
            @toggle-favorite="dish => $emit('toggleDishFavorite', dish)" 
        />
        <TrendingSection 
            :trending-dishes="trendingDishes"
            :favorite-dishes="favoriteDishes"
            @open-action-modal="dish => $emit('openActionModal', dish)"
            @open-dine-options="dish => $emit('openDineOptions', dish)"
            @toggle-favorite="dish => $emit('toggleDishFavorite', dish)"
        />
        <DiscoverSection 
            v-if="newRestaurants.length > 0"
            title="Descubra Novos Lugares"
            :restaurants="newRestaurants"
            :favorite-restaurants="favoriteRestaurants"
            @toggle-favorite="restaurant => $emit('toggleRestaurantFavorite', restaurant)"
            @request-reservation="restaurant => $emit('requestReservation', restaurant)"
            @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
            @open-menu-modal="restaurant => $emit('openMenuModal', restaurant)"
        />
        <AIFavoriteSection @open-payment-modal="() => $emit('openPaymentModal')"/>
        <AICreateDish :all-dishes="allDishes" />
    </div>
</template>

<script setup>
import { computed } from 'vue';
import TrendingSection from '../sections/TrendingSection.vue';
import DiscoverSection from '../sections/DiscoverSection.vue';
import FrequentOrdersSection from '../sections/FrequentOrdersSection.vue';
import AIFavoriteSection from '../sections/AIFavoriteSection.vue';
import AICreateDish from '../sections/AICreateDish.vue';

const props = defineProps({
    restaurants: Array,
    trendingDishes: Array,
    frequentDishes: Array, // Este prop já não é usado, mas mantemo-lo para evitar erros
    favoriteDishes: Set,
    favoriteRestaurants: Set,
    allDishes: Array,
    newRestaurants: Array,
});

defineEmits([
    'openActionModal', 
    'openDineOptions',
    'toggleDishFavorite', 
    'toggleRestaurantFavorite', 
    'requestReservation', 
    'viewRestaurant', 
    'openPaymentModal',
    'openMenuModal'
]);

const favoritedDishesList = computed(() => {
    return props.allDishes
        .filter(dish => props.favoriteDishes.has(dish.id))
        .slice(0, 8);
});

// AQUI ESTÁ A ALTERAÇÃO: Nova propriedade para limitar os restaurantes
const discoverRestaurants = computed(() => {
    return props.restaurants.slice(0, 6);
});
</script>