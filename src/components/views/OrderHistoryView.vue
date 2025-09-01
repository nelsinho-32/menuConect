<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold mb-8">Histórico de Pedidos</h1>

        <div v-if="orderStore.orderHistory.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não fez nenhum pedido.</p>
        </div>

        <div v-else class="space-y-6">
            <div v-for="order in orderStore.orderHistory" :key="order.id" 
                 :class="['bg-white p-6 rounded-lg shadow-md transition-all', { 'border-2 border-indigo-500 bg-indigo-50': order.encontro_id }]">
                
                <div v-if="order.encontro_id" class="flex items-center gap-2 mb-4 pb-4 border-b border-indigo-200">
                    <span class="text-2xl">🎉</span>
                    <div>
                        <p class="font-bold text-indigo-800">Este pedido faz parte de um Encontro Planeado!</p>
                        <p class="text-sm text-indigo-600">Organizado e pago no dia {{ formatDate(order.created_at) }}.</p>
                    </div>
                </div>

                <div class="flex flex-col sm:flex-row justify-between sm:items-start border-b pb-4 mb-4">
                    <div>
                        <p class="font-bold text-lg text-gray-800">{{ order.restaurantName }}</p>
                        <p class="text-sm text-gray-500">Pedido #{{ order.id }}</p>
                    </div>
                    <div class="text-left sm:text-right mt-2 sm:mt-0">
                        <p class="font-bold text-xl text-indigo-600">R$ {{ parseFloat(order.total_price).toFixed(2).replace('.', ',') }}</p>
                        <p class="text-sm text-gray-500">{{ formatDate(order.created_at) }}</p>
                    </div>
                </div>
                
                <div>
                    <h4 class="font-semibold text-gray-600 mb-2">Itens:</h4>
                    <div class="space-y-4">
                        <div v-for="(item, index) in order.items" :key="index" class="flex gap-4">
                            <img :src="item.dishImage" class="w-16 h-16 rounded-md object-cover flex-shrink-0" alt="">
                            
                            <div class="flex-grow">
                                <div class="flex justify-between">
                                    <span class="font-semibold text-gray-800">{{ item.quantity }}x {{ item.dishName }}</span>
                                    <span class="font-semibold text-gray-800">R$ {{ (parseFloat(item.price_at_time) * item.quantity).toFixed(2).replace('.', ',') }}</span>
                                </div>
                                <div v-if="item.customization && item.customization.removedIngredients && item.customization.removedIngredients.length > 0" class="text-xs text-red-600 mt-1">
                                    <span>Sem: {{ item.customization.removedIngredients.join(', ') }}</span>
                                </div>
                                <div v-if="item.customization && item.customization.notes" class="text-xs text-gray-500 mt-1">
                                    <span>Nota: {{ item.customization.notes }}</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="border-t mt-4 pt-4 flex justify-end">
                    <button @click="$emit('reorder', order)" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                        Pedir Novamente
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useOrderStore } from '@/stores/orderStore';

const orderStore = useOrderStore();

defineEmits(['backToMain', 'reorder']);

// Função para formatar a data de forma amigável
const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleDateString('pt-BR', {
        day: '2-digit',
        month: 'long',
        year: 'numeric'
    });
};
</script>