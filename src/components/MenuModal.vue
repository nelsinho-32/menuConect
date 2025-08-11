<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-4xl w-full shadow-2xl relative max-h-[90vh] flex flex-col">
            <button @click="$emit('close')" class="absolute -top-4 -right-4 bg-white rounded-full p-1 text-gray-700 hover:text-red-500 z-10">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
            <div class="p-6 border-b text-center">
                <h3 class="text-2xl font-bold text-gray-800">Cardápio de {{ restaurant.name }}</h3>
            </div>

            <div class="p-6 overflow-y-auto">
                <RestaurantMenu 
                    :menu="restaurant.menu" 
                    @open-action-modal="dish => $emit('openActionModal', dish)"
                />
            </div>
        </div>
    </div>
</template>

<script setup>
import RestaurantMenu from './RestaurantMenu.vue';

defineProps({
    restaurant: { type: Object, required: true }
});
defineEmits(['close', 'openActionModal']);
</script>