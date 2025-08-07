<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-8 gap-4">
            <h1 class="text-3xl font-bold">Todos os Nossos Pratos</h1>
            <button v-if="userStore.isCompanyUser()" @click="$emit('openAddDishModal')" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 flex items-center gap-2 self-start md:self-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                    <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                </svg>
                Adicionar Prato
            </button>
        </div>

        <div class="mb-8 flex flex-wrap gap-2 border-b border-gray-200 pb-4">
            <button
                @click="selectedCategory = 'Todos'"
                :class="['filter-button', selectedCategory === 'Todos' ? 'active' : '']">
                Todos
            </button>
            <button
                v-for="category in uniqueCategories"
                :key="category"
                @click="selectedCategory = category"
                :class="['filter-button', selectedCategory === category ? 'active' : '']">
                {{ category }}
            </button>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <DishCard 
                v-for="dish in filteredDishes" 
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
import { ref, computed } from 'vue';
import DishCard from '../DishCard.vue';
import { useUserStore } from '@/stores/userStore';

const userStore = useUserStore();

const props = defineProps({
    dishes: { type: Array, required: true },
    favoriteDishes: { type: Set, required: true }
});

defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions', 'openAddDishModal']);

// --- INÍCIO: NOVA LÓGICA DE FILTRAGEM ---

const selectedCategory = ref('Todos');

// Cria uma lista de categorias únicas a partir dos pratos existentes
const uniqueCategories = computed(() => {
    // Usamos categorias fixas para manter a ordem, mas filtramos para mostrar apenas as que existem
    const fixedOrder = ['Entradas', 'Prato Principal', 'Sobremesas', 'Bebidas', 'Novidades'];
    const existingCategories = new Set(props.dishes.map(dish => dish.category));
    return fixedOrder.filter(category => existingCategories.has(category));
});

// Filtra os pratos com base na categoria selecionada
const filteredDishes = computed(() => {
    if (selectedCategory.value === 'Todos') {
        return props.dishes;
    }
    return props.dishes.filter(dish => dish.category === selectedCategory.value);
});
// --- FIM: NOVA LÓGICA DE FILTRAGEM ---

</script>

<style scoped>
/* Os estilos dos botões já existem no main.css, não é preciso adicionar nada aqui */
.filter-button {
    @apply px-4 py-2 text-sm font-semibold text-gray-700 bg-white border border-gray-300 rounded-full hover:bg-gray-100 transition-colors;
}

.filter-button.active {
    @apply bg-indigo-600 text-white border-indigo-600;
}
</style>