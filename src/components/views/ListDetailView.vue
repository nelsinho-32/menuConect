<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('back')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para Minhas Listas</button>
        
        <div v-if="listStore.state.isLoading" class="text-center p-10">A carregar...</div>
        <div v-else-if="listStore.state.selectedListDetails">
            <h1 class="text-3xl font-bold">{{ listStore.state.selectedListDetails.details.name }}</h1>
            <p class="text-gray-500 mb-8">{{ listStore.state.selectedListDetails.details.description }}</p>

            <div v-if="listStore.state.selectedListDetails.items.restaurants.length > 0" class="mb-12">
                <h2 class="text-2xl font-bold mb-4">Restaurantes na Lista</h2>
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    <RestaurantCard 
                        v-for="rest in listStore.state.selectedListDetails.items.restaurants" 
                        :key="rest.id" 
                        :restaurant="rest"
                        :is-favorited="userDataStore.favoriteRestaurantIds.has(rest.id)"
                        @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
                    />
                </div>
            </div>

            <div v-if="listStore.state.selectedListDetails.items.dishes.length > 0">
                <h2 class="text-2xl font-bold mb-4">Pratos na Lista</h2>
                 <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
                    <DishCard 
                        v-for="dish in listStore.state.selectedListDetails.items.dishes" 
                        :key="dish.id" 
                        :dish="dish"
                        :is-favorited="userDataStore.favoriteDishIds.has(dish.id)"
                        @open-action-modal="dish => $emit('openActionModal', dish)"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useListStore } from '@/stores/listStore';
import { useUserDataStore } from '@/stores/userDataStore';
import RestaurantCard from '../RestaurantCard.vue';
import DishCard from '../DishCard.vue';

const props = defineProps({
    listId: { type: Number, required: true }
});

defineEmits(['back', 'viewRestaurant', 'openActionModal']);

const listStore = useListStore();
const userDataStore = useUserDataStore();

onMounted(() => {
    listStore.fetchListDetails(props.listId);
});
</script>