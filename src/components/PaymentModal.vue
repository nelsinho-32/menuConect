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
                <div class="space-y-1 text-sm border-t pt-2 mt-2">
                    <div class="flex justify-between">
                        <span>Subtotal</span>
                        <span>R$ {{ subtotal.toFixed(2).replace('.',',') }}</span>
                    </div>
                    <div class="flex justify-between" :class="deliveryFee > 0 ? 'text-gray-600' : 'text-green-600'">
                        <span>Taxa de Entrega</span>
                        <span>R$ {{ deliveryFee.toFixed(2).replace('.',',') }}</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg text-gray-800 border-t pt-2 mt-2">
                        <span>Total</span>
                        <span>R$ {{ total.toFixed(2).replace('.',',') }}</span>
                    </div>
                </div>

                <h4 class="font-bold text-lg mb-4 mt-6">Forma de Pagamento</h4>
                <div class="space-y-3">
                    <button @click="selectedPayment = 'pix'" :class="getButtonClass('pix')">
                        <span class="font-semibold">Pagar com Pix</span>
                    </button>
                    <button @click="selectedPayment = 'card'" :class="getButtonClass('card')">
                        <span class="font-semibold">Cartão de Crédito/Débito</span>
                    </button>
                    <button @click="selectedPayment = 'local'" :class="getButtonClass('local')" class="payment-option-button w-full flex items-center p-4 rounded-lg border-2">
                        <span class="font-semibold">Pagar no Estabelecimento</span>
                    </button>
                </div>
            </div>
            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('closeModal')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                <button @click="$emit('paymentSuccess')" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Confirmar Pedido</button>
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

const subtotal = computed(() => {
    return props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

// AQUI ESTÁ A LÓGICA ATUALIZADA
const deliveryFee = computed(() => {
    const deliveryRestaurants = new Set();
    props.cart.forEach(item => {
        if (item.dineOption === 'delivery' || !item.dineOption) {
            deliveryRestaurants.add(item.restaurantId);
        }
    });
    return deliveryRestaurants.size * 5.00;
});

const total = computed(() => subtotal.value + deliveryFee.value);

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