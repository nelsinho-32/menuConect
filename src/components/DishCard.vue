<template>
    <div class="dish-card w-64 md:w-72 relative" :class="{'opacity-60': !dish.is_available}">
        <div v-if="!dish.is_available" class="absolute top-3 left-3 bg-red-500 text-white text-xs font-bold px-2 py-1 rounded-full z-10">
            ESGOTADO
        </div>
        <img class="h-40 w-full object-cover" :src="dish.imageUrl" :alt="'Imagem de ' + dish.dishName">
        
        <button 
            @click.stop="$emit('toggleFavorite', dish)" 
            title="Adicionar aos favoritos" 
            class="absolute top-3 right-3 bg-white/70 backdrop-blur-sm p-2 rounded-full transition-colors duration-200 hover:bg-white"
        >
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" 
                 :fill="isFavorited ? '#ef4444' : 'none'" 
                 :stroke="isFavorited ? '#ef4444' : '#4b5563'" 
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="transition-all duration-200"
            >
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
        </button>

        <div class="p-4 flex flex-col flex-grow">
            <h3 class="text-lg font-bold text-gray-900 truncate">{{ dish.dishName }}</h3>
            <p class="text-gray-500 text-sm mt-1">{{ dish.restaurantName }}</p>
            <div class="mt-auto pt-4 flex justify-between items-center">
                <p class="text-xl font-extrabold brand-text">R$ {{ formatCurrency(dish.price) }}</p>
                <div class="flex gap-2">
                    <button @click="$emit('openDineOptions', dish)" title="Opções de consumo" class="reserve-button bg-gray-200 text-gray-600 p-2 rounded-lg font-semibold hover:bg-gray-300 transition-colors" :disabled="!dish.is_available">📅</button>
                    <button @click="$emit('openActionModal', dish)" title="Pedir ou adicionar ao carrinho" class="action-icon-button bg-indigo-600 text-white p-2 rounded-lg font-semibold hover:bg-indigo-700 transition-colors" :disabled="!dish.is_available">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
const props = defineProps({
  dish: {
    type: Object,
    required: true
  },
  isFavorited: {
    type: Boolean,
    default: false
  }
});
defineEmits(['openActionModal', 'toggleFavorite', 'openDineOptions']);
const formatCurrency = (value) => {
    return parseFloat(value).toFixed(2).replace('.', ',');
};
</script>