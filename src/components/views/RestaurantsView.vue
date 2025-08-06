<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-8 gap-4">
            <h1 class="text-3xl font-bold">Nossos Restaurantes Parceiros</h1>
            <button v-if="userStore.isCompanyUser()" @click="$emit('openAddRestaurantModal')" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 flex items-center gap-2 self-start md:self-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8.5 6a.5.5 0 0 0-1 0v1.5H6a.5.5 0 0 0 0 1h1.5V10a.5.5 0 0 0 1 0V8.5H10a.5.5 0 0 0 0-1H8.5V6z"/>
                    <path d="M2 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V2zm10 0H4a1 1 0 0 0-1 1v12a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V2a1 1 0 0 0-1-1z"/>
                </svg>
                Adicionar Restaurante
            </button>
        </div>

        <div class="mb-8 flex flex-wrap gap-2">
            <button
                @click="selectedCuisine = 'Todos'"
                :class="['filter-button', selectedCuisine === 'Todos' ? 'active' : '']">
                Todos
            </button>
            <button
                v-for="cuisine in uniqueCuisines"
                :key="cuisine"
                @click="selectedCuisine = cuisine"
                :class="['filter-button', selectedCuisine === cuisine ? 'active' : '']">
                {{ cuisine }}
            </button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <RestaurantCard 
                v-for="rest in filteredRestaurants" 
                :key="rest.id" 
                :restaurant="rest"
                :is-favorited="favoriteRestaurants.has(rest.id)"
                @toggle-favorite="restaurant => $emit('toggleFavorite', restaurant)"
                @request-reservation="restaurant => $emit('requestReservation', restaurant)"
                @view-restaurant="restaurant => $emit('viewRestaurant', restaurant)"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import RestaurantCard from '../RestaurantCard.vue';
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();

const props = defineProps({
    restaurants: { type: Array, required: true },
    favoriteRestaurants: { type: Set, required: true }
});

defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant', 'openAddRestaurantModal']);

// --- INÍCIO: NOVA LÓGICA DE FILTRAGEM ---

// 1. Guarda a cozinha selecionada. Começa com "Todos".
const selectedCuisine = ref('Todos');

// 2. Cria uma lista de tipos de cozinha únicos a partir dos restaurantes existentes.
const uniqueCuisines = computed(() => {
    const cuisines = props.restaurants.map(r => r.cuisine);
    return [...new Set(cuisines)]; // O Set remove duplicados
});

// 3. Cria uma lista de restaurantes filtrada com base na seleção.
const filteredRestaurants = computed(() => {
    if (selectedCuisine.value === 'Todos') {
        return props.restaurants; // Se for "Todos", retorna a lista completa
    }
    return props.restaurants.filter(r => r.cuisine === selectedCuisine.value);
});

// --- FIM: NOVA LÓGICA DE FILTRAGEM ---
</script>

<style scoped>
/* INÍCIO: ESTILOS PARA OS BOTÕES DE FILTRO */
.filter-button {
    @apply px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-full hover:bg-gray-100 transition-colors;
}

.filter-button.active {
    @apply bg-indigo-600 text-white border-indigo-600;
}
/* FIM: ESTILOS PARA OS BOTÕES DE FILTRO */
</style>