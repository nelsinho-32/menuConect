<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Iniciar Atendimento</h3>
                <p class="text-gray-500">Mesa: <span class="font-bold text-indigo-600">{{ table.id }}</span></p>
            </div>
            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
                <div>
                    <label for="guests" class="block text-sm font-medium text-gray-700">Nº de Pessoas</label>
                    <input type="number" id="guests" v-model.number="sessionData.guests" required min="1" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>
                <div>
                    <label for="customerNames" class="block text-sm font-medium text-gray-700">Nomes dos Clientes (Opcional)</label>
                    <input type="text" id="customerNames" v-model="customerNamesInput" placeholder="Ex: Nelsinho, Maria, João" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    <p class="text-xs text-gray-400 mt-1">Separe os nomes por vírgula.</p>
                </div>
                <div class="pt-4 flex gap-3">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Iniciar</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const props = defineProps({
    table: { type: Object, required: true }
});

const emit = defineEmits(['close', 'startSession']);

const sessionData = reactive({
    guests: 1,
    customerNames: []
});
const customerNamesInput = ref('');

const handleSubmit = () => {
    // Transforma a string de nomes numa lista, removendo espaços em branco
    sessionData.customerNames = customerNamesInput.value
        .split(',')
        .map(name => name.trim())
        .filter(name => name.length > 0);
        
    emit('startSession', { ...sessionData, tableId: props.table.id });
};
</script>