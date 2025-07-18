<template>
    <div :class="['cart-sidebar fixed top-0 right-0 h-full w-full max-w-sm bg-white shadow-2xl z-50 flex flex-col', { 'open': isOpen }]">
        <div class="p-6 border-b flex justify-between items-center">
            <h3 class="text-2xl font-bold text-gray-800">Meu Carrinho</h3>
            <button @click="$emit('toggle-cart', false)" class="text-gray-500 hover:text-gray-800 text-3xl">&times;</button>
        </div>
        <div class="flex-grow p-6 overflow-y-auto">
            <div v-if="!cart.length"><p class="text-gray-500 text-center">Seu carrinho está vazio.</p></div>
            <div v-else>
                <div v-for="item in cart" :key="item.id" class="flex justify-between items-center mb-4">
                    <div class="flex-grow">
                        <p class="font-semibold">{{ item.dishName }}</p>
                        <p class="text-sm text-gray-500">R$ {{ parseFloat(item.price).toFixed(2).replace('.',',') }}</p>
                    </div>
                    <div class="flex items-center gap-3"><span class="font-semibold">{{ item.quantity }}x</span></div>
                </div>
            </div>
        </div>
        <div class="p-6 border-t bg-gray-50">
            <div class="flex justify-between font-bold text-lg mb-4">
                <span>Subtotal</span>
                <span>R$ {{ subtotal }}</span>
            </div>
            <button class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Finalizar Compra</button>
        </div>
    </div>
</template>
<script setup>
import { computed } from 'vue';
const props = defineProps({
  cart: {
    type: Array,
    required: true
  },
  isOpen: {
    type: Boolean,
    required: true
  }
});
defineEmits(['toggle-cart']);
const subtotal = computed(() => {
    const total = props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    return parseFloat(total).toFixed(2).replace('.', ',');
});
</script>