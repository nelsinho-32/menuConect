<template>
    <div @click.self="$emit('closeModal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-2xl font-bold text-gray-800">Finalizar Pedido</h3>
                <button @click="$emit('closeModal')" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
            </div>
            <div class="p-6">
                <h4 class="font-bold text-lg mb-4">Resumo do Pedido</h4>
                <div class="space-y-2 text-gray-600 mb-6 max-h-40 overflow-y-auto pr-2">
                    <div v-for="item in cart" :key="item.id" class="flex justify-between text-sm">
                        <span>{{ item.quantity }}x {{ item.dishName }}</span>
                        <span>R$ {{ (item.price * item.quantity).toFixed(2).replace('.',',') }}</span>
                    </div>
                </div>
                 <div class="flex justify-between font-bold border-t pt-2 mt-2">
                    <span>Total</span>
                    <span>R$ {{ total.toFixed(2).replace('.',',') }}</span>
                </div>

                <h4 class="font-bold text-lg mb-4 mt-6">Forma de Pagamento</h4>
                <div class="space-y-3">
                    <button @click="selectedPayment = 'pix'" :class="getButtonClass('pix')">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22h.01m-4.2-7.8-4.2 4.2m8.4-4.2 4.2 4.2M2 7.1 6.2 11m11.6-3.9 4.2-4.2M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 5.1V12"/></svg>
                        <span class="font-semibold">Pagar com Pix</span>
                    </button>
                    <button @click="selectedPayment = 'card'" :class="getButtonClass('card')">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2Zm0 2v2H4V6h16Zm0 12H4v-6h16v6Z"/></svg>
                        <span class="font-semibold">Cartão de Crédito/Débito</span>
                    </button>
                    <button @click="selectedPayment = 'cash'" :class="getButtonClass('cash')">
                        <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16Zm-2.5-3.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm5 0a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm-5-6a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Zm5 0a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0Z"/></svg>
                        <span class="font-semibold">Dinheiro</span>
                    </button>
                </div>

            </div>
            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('closeModal')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Cancelar</button>
                <button @click="$emit('paymentSuccess')" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Confirmar Pedido</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
  cart: { type: Array, required: true },
  shortcut: { type: String, default: null }
});
defineEmits(['closeModal', 'paymentSuccess']);

const selectedPayment = ref('pix');

const total = computed(() => {
    const subtotal = props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    return subtotal + 5; // Adiciona taxa de entrega
});

const getButtonClass = (method) => {
    return [
        'w-full flex items-center p-4 rounded-lg border-2 gap-3 transition-colors',
        selectedPayment.value === method ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300 hover:border-gray-400'
    ];
};

onMounted(() => {
    if (props.shortcut) {
        selectedPayment.value = props.shortcut;
    }
});
</script>