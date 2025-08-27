<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-8 gap-4">
            <div>
                <h1 class="text-3xl font-bold">Análise de Vendas</h1>
                <p v-if="managedRestaurant" class="text-gray-500">
                    A exibir dados de: <span class="font-semibold text-indigo-600">{{ managedRestaurant.name }}</span>
                </p>
            </div>

            <div class="flex flex-wrap items-end gap-4">
                <div v-if="authStore.currentUser?.role === 'admin'">
                    <label for="restaurant-selector-analytics" class="block text-sm font-medium text-gray-700">Ver dados de:</label>
                    <select id="restaurant-selector-analytics" 
                            :value="managementStore.managedRestaurantId" 
                            @change="onRestaurantChange"
                            class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                        <option v-for="restaurant in restaurantStore.restaurants" :key="restaurant.id" :value="restaurant.id">
                            {{ restaurant.name }}
                        </option>
                    </select>
                </div>
                <div class="flex items-center gap-2 bg-gray-100 p-1 rounded-lg">
                    <button @click="changePeriod('last7days')" :class="getButtonClass('last7days')">Últimos 7 dias</button>
                    <button @click="changePeriod('last30days')" :class="getButtonClass('last30days')">Últimos 30 dias</button>
                    <button @click="changePeriod('monthToDate')" :class="getButtonClass('monthToDate')">Este Mês</button>
                </div>
            </div>
            </div>

        <div v-if="analyticsStore.state.isLoading" class="text-center py-20">
            <p class="text-gray-500">A carregar dados de análise...</p>
        </div>
        <div v-else-if="analyticsStore.state.error" class="text-center py-20 bg-red-50 text-red-700 rounded-lg">
            <p>{{ analyticsStore.state.error }}</p>
        </div>
        <div v-else>
            <div class="bg-white p-6 rounded-2xl shadow-lg mb-8">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Histórico de Vendas (R$)</h2>
                <div v-if="salesChartData.labels.length > 0" style="height: 350px;">
                    <BarChart :chart-data="salesChartData" />
                </div>
                <div v-else class="text-center text-gray-400 py-12">
                    <p>Sem dados de vendas para o período selecionado.</p>
                </div>
            </div>

            <div class="bg-white p-6 rounded-2xl shadow-lg">
                <h2 class="text-xl font-bold text-gray-800 mb-4">Pratos Mais Rentáveis</h2>
                <div v-if="analyticsStore.state.topDishes.length > 0" class="space-y-3">
                    <div v-for="(dish, index) in analyticsStore.state.topDishes" :key="dish.dishName" class="flex items-center justify-between p-3 rounded-lg" :class="index % 2 === 0 ? 'bg-gray-50' : ''">
                        <div class="flex items-center">
                            <span class="font-bold text-gray-500 w-8">{{ index + 1 }}.</span>
                            <span class="font-semibold text-gray-800">{{ dish.dishName }}</span>
                        </div>
                        <div class="text-right">
                            <p class="font-bold text-indigo-600">R$ {{ dish.total_revenue.toFixed(2).replace('.', ',') }}</p>
                            <p class="text-xs text-gray-500">{{ dish.total_quantity_sold }} vendidos</p>
                        </div>
                    </div>
                </div>
                 <div v-else class="text-center text-gray-400 py-12">
                    <p>Sem dados de pratos para o período selecionado.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed, watch } from 'vue';
import { useAnalyticsStore } from '@/stores/analyticsStore';
import { useManagementStore } from '@/stores/managementStore';
import { useRestaurantStore } from '@/stores/restaurantStore';
import { useAuthStore } from '@/stores/authStore'; // Importa a store de autenticação
import BarChart from '../BarChart.vue';

const analyticsStore = useAnalyticsStore();
const managementStore = useManagementStore();
const restaurantStore = useRestaurantStore();
const authStore = useAuthStore(); // Inicializa a store de autenticação

const activePeriod = ref('last7days');

const managedRestaurant = computed(() => {
    return restaurantStore.restaurants.find(r => r.id === managementStore.managedRestaurantId);
});

// INÍCIO DA CORREÇÃO: Função para lidar com a mudança no seletor
const onRestaurantChange = (event) => {
    const newId = parseInt(event.target.value);
    if (newId) {
        // Esta ação da managementStore irá atualizar o ID,
        // e o 'watch' abaixo tratará de buscar os novos dados de análise.
        managementStore.setManagedRestaurant(newId);
    }
};

onMounted(() => {
    // Busca os dados iniciais com base no restaurante já selecionado na store
    if (managementStore.managedRestaurantId) {
        analyticsStore.fetchAnalyticsData(activePeriod.value);
    }
});

// Observa se o ID do restaurante gerido muda e busca novos dados
watch(() => managementStore.managedRestaurantId, (newId) => {
    if (newId) {
        analyticsStore.fetchAnalyticsData(activePeriod.value);
    }
});
// FIM DA CORREÇÃO

const changePeriod = (period) => {
    activePeriod.value = period;
    analyticsStore.fetchAnalyticsData(period);
};

const getButtonClass = (period) => {
    return [
        'px-4 py-2 text-sm font-semibold rounded-md transition-colors',
        activePeriod.value === period ? 'bg-indigo-600 text-white' : 'text-gray-600 hover:bg-gray-200'
    ];
};

const salesChartData = computed(() => {
    const history = analyticsStore.state.salesHistory;
    return {
        labels: history.map(item => new Date(item.date + 'T00:00:00').toLocaleDateString('pt-BR', { day: '2-digit', month: 'short' })),
        datasets: [
            {
                label: 'Vendas Totais',
                backgroundColor: '#4f46e5',
                borderColor: '#4f46e5',
                data: history.map(item => item.total_sales),
                borderRadius: 4,
            }
        ]
    };
});
</script>