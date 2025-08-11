<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-6 gap-2">
            <div>
                <h1 class="text-3xl font-bold">Dashboard de Gestão</h1>
                <p class="text-gray-500">Uma visão geral do seu negócio em tempo real.</p>
            </div>
            <div>
                 <select v-model="selectedRestaurantId" class="border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    <option :value="null" disabled>Selecione um restaurante</option>
                    <option v-for="restaurant in restaurantStore.restaurants" :key="restaurant.id" :value="restaurant.id">
                        {{ restaurant.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-indigo-500">
                <p class="text-sm font-semibold text-gray-500">Mesas Ocupadas</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">{{ occupiedTables }} / {{ totalTables }}</p>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-orange-500">
                <p class="text-sm font-semibold text-gray-500">Clientes na Fila</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">{{ waitingListCount }}</p>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-green-500">
                <p class="text-sm font-semibold text-gray-500">Vendas do Dia (Simulado)</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">R$ {{ dailySales.toFixed(2).replace('.', ',') }}</p>
            </div>
            
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-pink-500">
                <p class="text-sm font-semibold text-gray-500">Prato Popular (Simulado)</p>
                <p class="text-2xl font-bold text-gray-800 mt-2 truncate">{{ mostPopularDish }}</p>
            </div>
        </div>

        <div class="mt-8">
            <button @click="$emit('navigateTo', 'tableManagement')" class="bg-indigo-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-indigo-700">
                Ir para a Gestão de Mesas
            </button>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRestaurantStore } from '@/stores/restaurantStore';

const props = defineProps({
    reservations: { type: Object, required: true },
    orderHistory: { type: Array, required: true }
});

defineEmits(['navigateTo']);

const restaurantStore = useRestaurantStore();
const selectedRestaurantId = ref(restaurantStore.restaurants.length > 0 ? restaurantStore.restaurants[0].id : null);

const selectedRestaurant = computed(() => {
    return restaurantStore.restaurants.find(r => r.id === selectedRestaurantId.value);
});

// Métricas Computadas
const occupiedTables = computed(() => {
    if (!selectedRestaurant.value || !selectedRestaurant.value.tables) return 0;
    return selectedRestaurant.value.tables.filter(t => t.status === 'occupied').length;
});

const totalTables = computed(() => {
    return selectedRestaurant.value ? selectedRestaurant.value.tables.length : 0;
});

const waitingListCount = computed(() => {
    return props.reservations.waitingForTable ? 1 : 0; // Simples, pode ser expandido
});

const dailySales = computed(() => {
    // Simulação: Pega o total dos 3 últimos pedidos do histórico
    return props.orderHistory.slice(-3).reduce((sum, order) => sum + order.total, 0);
});

const mostPopularDish = computed(() => {
    if (props.orderHistory.length === 0) return "Nenhum pedido hoje";
    // Simulação: Pega o primeiro prato do último pedido
    const lastOrder = props.orderHistory[props.orderHistory.length - 1];
    return lastOrder.items[0]?.dishName || "N/A";
});

</script>