<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl">
            <div class="p-6 border-b text-center">
                <h3 class="text-2xl font-bold text-gray-800">Dividir a Conta</h3>
                <p class="text-gray-500">Total do Pedido: R$ {{ total.toFixed(2).replace('.', ',') }}</p>
            </div>
            <div class="p-6 space-y-4">
                <div>
                    <label for="split-count" class="block text-sm font-medium text-gray-700">Dividir igualmente por:</label>
                    <input type="number" id="split-count" v-model.number="numberOfPeople" min="1" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>
                <div v-if="splitAmount > 0" class="text-center bg-indigo-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-500">Valor por pessoa</p>
                    <p class="text-3xl font-bold text-indigo-600">R$ {{ splitAmount.toFixed(2).replace('.', ',') }}</p>
                </div>
            </div>
            <div class="p-4 bg-gray-100 border-t flex justify-end gap-3">
                 <button @click="$emit('close')" class="bg-white border border-gray-300 text-gray-700 font-bold py-2 px-6 rounded-lg hover:bg-gray-50">Cancelar</button>
                <button @click="confirmSplit" class="bg-green-500 text-white font-bold py-2 px-6 rounded-lg hover:bg-green-600">Confirmar Divisão</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
    total: { type: Number, required: true }
});

const emit = defineEmits(['close', 'confirm']);

const numberOfPeople = ref(2);

const splitAmount = computed(() => {
    if (props.total > 0 && numberOfPeople.value > 0) {
        return props.total / numberOfPeople.value;
    }
    return 0;
});

const confirmSplit = () => {
    emit('confirm', {
        type: 'equal',
        people: numberOfPeople.value,
        amountPerPerson: splitAmount.value
    });
};
</script>