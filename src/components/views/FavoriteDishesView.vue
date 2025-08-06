<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold mb-8">❤️ Minhas Comidas Favoritas</h1>

        <div v-if="favoriteDishes.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não adicionou nenhum prato aos seus favoritos.</p>
            <p class="text-sm text-gray-400 mt-2">Clique no coração ❤️ nos cartões de comida para os adicionar aqui!</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <DishCard 
                v-for="dish in favoriteDishes" 
                :key="dish.id" 
                :dish="dish"
                :is-favorited="true"
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
    favoriteDishes: { type: Array, required: true }
});

defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions', 'backToMain']);
</script>