<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold mb-8">Histórico de Pedidos</h1>

        <div v-if="orderHistory.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não tem nenhum pedido no seu histórico.</p>
            <p class="text-sm text-gray-400 mt-2">Complete uma compra para que ela apareça aqui!</p>
        </div>

        <div v-else class="space-y-6">
            <div v-for="order in sortedHistory" :key="order.id" class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex justify-between items-center border-b pb-3 mb-3">
                    <div>
                        <p class="font-bold text-lg text-gray-800">Pedido de {{ formatDate(order.date) }}</p>
                        <p class="text-sm text-gray-500">ID do Pedido: #{{ order.id }}</p>
                    </div>
                    <p class="font-bold text-xl text-indigo-600">R$ {{ order.total.toFixed(2).replace('.', ',') }}</p>
                </div>
                <div class="space-y-3">
                    <div v-for="item in order.items" :key="item.cartItemId" class="text-sm text-gray-600 border-t pt-3">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center gap-3">
                                <img :src="item.imageUrl" class="w-10 h-10 rounded object-cover">
                                <div>
                                    <span class="font-semibold text-gray-800">{{ item.quantity }}x {{ item.dishName }}</span>
                                    <p class="text-xs text-gray-500">{{ item.restaurantName }}</p>
                                </div>
                            </div>
                            <span>R$ {{ (item.price * item.quantity).toFixed(2).replace('.', ',') }}</span>
                        </div>
                        
                        <div v-if="getRemovedIngredients(item)" class="text-xs text-red-600 mt-2 ml-12 bg-red-50 p-2 rounded-md">
                            <span class="font-semibold">Sem:</span> {{ getRemovedIngredients(item) }}
                        </div>
                        <div v-if="item.customization && item.customization.notes" class="text-xs text-gray-500 mt-2 ml-12 bg-gray-50 p-2 rounded-md">
                            <span class="font-semibold">Notas:</span> {{ item.customization.notes }}
                        </div>
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

// Nova função para calcular os ingredientes removidos
const getRemovedIngredients = (item) => {
    if (!item.customization) return '';
    const initialIngredients = new Set((item.description || '').split(',').map(i => i.trim()).filter(Boolean));
    const customizedIngredients = new Set((item.customization.ingredients || '').split(',').map(i => i.trim()).filter(Boolean));
    return Array.from(initialIngredients).filter(i => !customizedIngredients.has(i)).join(', ');
};
</script>