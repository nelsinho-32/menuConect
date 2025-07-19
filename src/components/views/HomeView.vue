<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <FrequentOrdersSection 
            :frequent-dishes="frequentDishes"
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
            :restaurants="restaurants"
            :favorite-restaurants="favoriteRestaurants"
            @toggle-favorite="restaurant => $emit('toggleRestaurantFavorite', restaurant)"
            @request-reservation="restaurant => $emit('requestReservation', restaurant)"
            @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
        />
        <AIFavoriteSection @open-payment-modal="() => $emit('openPaymentModal')"/>
        <AICreateDish :all-dishes="allDishes" />
    </div>
</template>
<script setup>
import TrendingSection from '../sections/TrendingSection.vue';
import DiscoverSection from '../sections/DiscoverSection.vue';
import FrequentOrdersSection from '../sections/FrequentOrdersSection.vue';
import AIFavoriteSection from '../sections/AIFavoriteSection.vue';
import AICreateDish from '../sections/AICreateDish.vue';

defineProps({
    restaurants: Array,
    trendingDishes: Array,
    frequentDishes: Array,
    favoriteDishes: Set,
    favoriteRestaurants: Set,
    allDishes: Array
});

defineEmits([
    'openActionModal', 
    'openDineOptions',
    'toggleDishFavorite', 
    'toggleRestaurantFavorite', 
    'requestReservation', 
    'viewRestaurant', 
    'openPaymentModal'
]);
</script>