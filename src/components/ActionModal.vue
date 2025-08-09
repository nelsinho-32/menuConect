<template>
    <div @click.self="$emit('close-modal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-xs w-full shadow-2xl p-6 text-center relative">
            <button @click="$emit('close-modal')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <h3 class="text-xl font-bold text-gray-800 mb-4">{{ dish.dishName }}</h3>
            
            <div class="flex items-center justify-center gap-4 my-6">
                <button @click="decreaseQuantity" class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 font-bold hover:bg-gray-300 disabled:opacity-50" :disabled="quantity <= 1">-</button>
                <span class="text-2xl font-bold w-12 text-center">{{ quantity }}</span>
                <button @click="increaseQuantity" class="w-10 h-10 rounded-full bg-gray-200 text-gray-700 font-bold hover:bg-gray-300">+</button>
            </div>

            <div class="flex flex-col gap-3">
                <button @click="$emit('open-customize-modal', dish)" class="w-full bg-yellow-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-yellow-600">Personalizar Pedido</button>
                <button @click="$emit('add-to-cart', { dish, quantity })" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700">Adicionar ao Carrinho</button>
                <button @click="$emit('order-now', { dish, quantity })" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Pedir Agora</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  dish: { type: Object, required: true }
});
defineEmits(['close-modal', 'add-to-cart', 'order-now', 'open-customize-modal']);

const quantity = ref(1);

const increaseQuantity = () => { quantity.value++; };
const decreaseQuantity = () => { if (quantity.value > 1) quantity.value--; };
</script>