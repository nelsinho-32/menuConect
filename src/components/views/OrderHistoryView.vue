<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold mb-8">Histórico de Pedidos</h1>

        <div v-if="orderHistory.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não tem nenhum pedido no seu histórico.</p>
            <p class="text-sm text-gray-400 mt-2">Complete uma compra para que ela apareça aqui!</p>
        </div>

        <div v-else class="space-y-6">
            <div v-for="order in sortedHistory" :key="order.date" class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex justify-between items-center border-b pb-3 mb-3">
                    <div>
                        <p class="font-bold text-lg text-gray-800">Pedido de {{ formatDate(order.date) }}</p>
                        <p class="text-sm text-gray-500">ID do Pedido: #{{ order.id }}</p>
                    </div>
                    <p class="font-bold text-xl text-indigo-600">R$ {{ order.total.toFixed(2).replace('.', ',') }}</p>
                </div>
                <div class="space-y-2">
                    <div v-for="item in order.items" :key="item.id" class="flex items-center justify-between text-sm text-gray-600">
                        <div class="flex items-center gap-3">
                            <img :src="item.imageUrl" class="w-10 h-10 rounded object-cover">
                            <span>{{ item.quantity }}x {{ item.dishName }}</span>
                        </div>
                        <span>R$ {{ (item.price * item.quantity).toFixed(2).replace('.', ',') }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    orderHistory: { type: Array, required: true }
});

defineEmits(['backToMain']);

// Ordena o histórico do mais recente para o mais antigo
const sortedHistory = computed(() => {
    return [...props.orderHistory].sort((a, b) => new Date(b.date) - new Date(a.date));
});

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
};
</script>