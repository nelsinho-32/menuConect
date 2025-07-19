<template>
    <div @click.self="$emit('closeModal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-2xl font-bold text-gray-800">Finalizar Pedido</h3>
                <button @click="$emit('closeModal')" class="text-gray-400 hover:text-gray-600">&times;</button>
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
                    <button @click="selectedPayment = 'pix'" :class="['payment-option-button w-full flex items-center p-4 rounded-lg border-2', selectedPayment === 'pix' ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300']">
                        <span class="font-semibold">Pagar com Pix</span>
                    </button>
                    <button @click="selectedPayment = 'card'" :class="['payment-option-button w-full flex items-center p-4 rounded-lg border-2', selectedPayment === 'card' ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300']">
                        <span class="font-semibold">Cartão de Crédito/Débito</span>
                    </button>
                    <button @click="selectedPayment = 'cash'" :class="['payment-option-button w-full flex items-center p-4 rounded-lg border-2', selectedPayment === 'cash' ? 'border-indigo-600 bg-indigo-50' : 'border-gray-300']">
                        <span class="font-semibold">Dinheiro</span>
                    </button>
                </div>

                <!-- Detalhes do Pagamento PIX -->
                <div v-if="selectedPayment === 'pix'" class="mt-6">
                    <div class="flex justify-center mb-4">
                        <img src="https://placehold.co/200x200/ffffff/000000?text=QR+CODE" alt="QR Code PIX" class="rounded-lg">
                    </div>
                    <div class="bg-gray-100 p-3 rounded-lg">
                        <p class="text-sm text-gray-500 text-left mb-1">Pix Copia e Cola:</p>
                        <div class="flex items-center">
                            <input id="pix-code" type="text" readonly value="00020126580014br.gov.bcb.pix0136..." class="w-full bg-transparent text-sm text-gray-700 truncate">
                            <button class="ml-2 text-indigo-600 hover:text-indigo-800 flex-shrink-0">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('closeModal')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Cancelar</button>
                <button class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Confirmar Pedido</button>
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
defineEmits(['closeModal']);

const selectedPayment = ref('pix');

const total = computed(() => {
    const subtotal = props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    return subtotal + 5; // Adiciona taxa de entrega
});

onMounted(() => {
    if (props.shortcut) {
        selectedPayment.value = props.shortcut;
    }
});
</script>