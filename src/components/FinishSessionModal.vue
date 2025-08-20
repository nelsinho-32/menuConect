<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl">
            <div class="p-6 border-b text-center">
                <h3 class="text-2xl font-bold text-gray-800">Finalizar Atendimento</h3>
                <p class="text-gray-500">Mesa {{ session.table_id }}</p>
            </div>
            <div class="p-6 space-y-4">
                <div class="text-center bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Total da Conta</p>
                    <p class="text-4xl font-bold text-gray-800">R$ {{ total.toFixed(2).replace('.', ',') }}</p>
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700">Forma de Pagamento</label>
                    <select v-model="selectedPayment" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                        <option>Dinheiro</option>
                        <option>Cartão de Crédito</option>
                        <option>Cartão de Débito</option>
                        <option>Pix</option>
                    </select>
                </div>
                <div class="pt-4 flex gap-3">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Voltar</button>
                    <button @click="$emit('confirm', selectedPayment)" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Confirmar Pagamento</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
const props = defineProps({
    session: { type: Object, required: true },
    consumption: { type: Array, required: true }
});
defineEmits(['close', 'confirm']);
const selectedPayment = ref('Dinheiro');
const total = computed(() => props.consumption.reduce((sum, item) => sum + (item.price_at_time * item.quantity), 0));
</script>