<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-8 gap-4">
            <div>
                <h1 class="text-3xl font-bold">Painel de Gestão</h1>
                <p v-if="managedRestaurant" class="text-gray-500">
                    Visão geral em tempo real para: <span class="font-semibold text-indigo-600">{{
                        managedRestaurant.name }}</span>
                </p>
            </div>
            <div v-if="authStore.currentUser?.role === 'admin'">
                <label for="restaurant-selector" class="block text-sm font-medium text-gray-700">Ver dados de:</label>
                <select id="restaurant-selector" v-model="selectedRestaurantId" @change="onRestaurantChange"
                    class="mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md">
                    <option v-for="restaurant in restaurantStore.restaurants" :key="restaurant.id"
                        :value="restaurant.id">
                        {{ restaurant.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-indigo-500">
                <p class="text-sm font-semibold text-gray-500">Mesas Ocupadas</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">{{ occupiedTablesCount }} / {{ totalTablesCount }}
                </p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-orange-500">
                <p class="text-sm font-semibold text-gray-500">Clientes na Fila</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">{{ managementStore.state.waitlist.length }}</p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-green-500">
                <p class="text-sm font-semibold text-gray-500">Reservas Ativas</p>
                <p class="text-4xl font-extrabold text-gray-800 mt-2">{{ managementStore.state.reservations.length }}
                </p>
            </div>
            <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-pink-500">
                <p class="text-sm font-semibold text-gray-500">Próxima Reserva</p>
                <p class="text-2xl font-bold text-gray-800 mt-2 truncate">{{ nextReservationTime }}</p>
            </div>
        </div>

        <div class="mt-8 grid grid-cols-1 lg:grid-cols-3 gap-8">
            <div class="lg:col-span-2 bg-white p-6 rounded-lg shadow-lg">
                <h2 class="text-2xl font-bold mb-4">Mapa do Salão</h2>
                <p class="text-sm text-gray-500 mb-4">Clique numa mesa para alterar o seu estado.</p>
                <div v-if="managedRestaurant" class="bg-gray-50 p-2 rounded-lg">
                    <svg viewBox="0 0 400 300" class="w-full h-auto rounded">
                        <defs>
                            <pattern id="floor-marble" patternUnits="userSpaceOnUse" width="60" height="60">
                                <rect width="60" height="60" fill="#f8fafc" />
                                <path d="M60 0 L0 60 M30 0 L0 30 M90 0 L0 90" stroke="#e2e8f0" stroke-width="1" />
                            </pattern>
                            <pattern id="floor-darkwood" patternUnits="userSpaceOnUse" width="80" height="20">
                                <rect width="80" height="20" fill="#4a5568" />
                                <line x1="0" y1="10" x2="80" y2="10" stroke="#2d3748" stroke-width="0.5" />
                            </pattern>
                            <pattern id="floor-tiles" patternUnits="userSpaceOnUse" width="40" height="40">
                                <rect width="40" height="40" fill="#e2e8f0" />
                                <rect width="20" height="20" fill="#cbd5e0" />
                                <rect x="20" y="20" width="20" height="20" fill="#cbd5e0" />
                            </pattern>
                        </defs>
                        <rect width="100%" height="100%"
                            :fill="`url(#${managedRestaurant.floorPatternId || 'floor-marble'})`" />
                        <g v-for="element in managedRestaurant.mapElements" :key="element.id"
                            :transform="`rotate(${element.rotation}, ${element.x + element.width / 2}, ${element.y + element.height / 2})`">
                            <rect :x="element.x" :y="element.y" :width="element.width" :height="element.height"
                                :fill="element.fill" :rx="element.rx || 0" />
                        </g>
                        <g v-for="table in managedRestaurant.tables" :key="table.id" @click="openStatusModal(table)"
                            class="cursor-pointer group">
                            <rect :x="table.x" :y="table.y" :width="table.width" :height="table.height"
                                :rx="table.shape === 'round' ? '50%' : '3'" :fill="getTableColor(table)"
                                class="transition-opacity group-hover:opacity-80" />
                            <text :x="table.x + table.width / 2" :y="table.y + table.height / 2 + 4"
                                text-anchor="middle" font-size="10" fill="white"
                                class="font-bold pointer-events-none">{{ table.id }}</text>
                        </g>
                    </svg>
                </div>
            </div>
            <div class="lg:col-span-1 space-y-6">
                <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-green-500">
                    <p class="text-sm font-semibold text-gray-500">Vendas do Dia</p>
                    <p class="text-4xl font-extrabold text-gray-800 mt-2">R$ {{
                        managementStore.state.financials.dailySales.toFixed(2).replace('.', ',') }}</p>
                </div>

                <div class="bg-white p-6 rounded-2xl shadow-lg border-l-4 border-pink-500">
                    <p class="text-sm font-semibold text-gray-500">Prato Popular</p>
                    <p class="text-2xl font-bold text-gray-800 mt-2 truncate">{{
                        managementStore.state.financials.mostPopularDish }}</p>
                </div>
            </div>
        </div>



        <div v-if="selectedTable" @click.self="selectedTable = null"
            class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
            <div class="bg-white rounded-lg p-6 w-full max-w-sm">
                <h3 class="font-bold text-lg mb-4">Alterar Status da Mesa {{ selectedTable.id }}</h3>
                <div class="flex flex-col gap-3">
                    <button @click="changeTableStatus('available')"
                        class="w-full py-2 px-4 bg-green-500 text-white font-semibold rounded-lg hover:bg-green-600">Disponível</button>
                    <button @click="changeTableStatus('occupied')"
                        class="w-full py-2 px-4 bg-gray-500 text-white font-semibold rounded-lg hover:bg-gray-600">Ocupada</button>
                    <button @click="changeTableStatus('cleaning')"
                        class="w-full py-2 px-4 bg-yellow-500 text-white font-semibold rounded-lg hover:bg-yellow-600">A
                        Limpar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'; // <-- A CORREÇÃO ESTÁ AQUI
import { useManagementStore } from '@/stores/managementStore';
import { useRestaurantStore } from '@/stores/restaurantStore';
import { useAuthStore } from '@/stores/authStore';

const managementStore = useManagementStore();
const restaurantStore = useRestaurantStore();
const authStore = useAuthStore();

const selectedRestaurantId = ref(null);
const selectedTable = ref(null);

const managedRestaurant = computed(() => {
    const idToFind = selectedRestaurantId.value || authStore.currentUser?.restaurant_id;
    if (!idToFind) return restaurantStore.restaurants.length > 0 ? restaurantStore.restaurants[0] : null;
    return restaurantStore.restaurants.find(r => r.id === idToFind);
});

const occupiedTablesCount = computed(() => managedRestaurant.value?.tables.filter(t => t.status === 'occupied').length || 0);
const totalTablesCount = computed(() => managedRestaurant.value?.tables.length || 0);
const nextReservationTime = computed(() => {
    if (!managementStore.state.reservations || managementStore.state.reservations.length === 0) return "Nenhuma";
    const nextBooking = managementStore.state.reservations[0].booking_time;
    return new Date(nextBooking).toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
});

const getTableColor = (table) => {
    const colors = { available: '#4ade80', occupied: '#a8a29e', cleaning: '#facc15' };
    return colors[table.status] || '#a8a29e';
};

const openStatusModal = (table) => { selectedTable.value = table; };

const changeTableStatus = async (newStatus) => {
    // Garante que managedRestaurant existe antes de tentar usá-lo
    if (!selectedTable.value || !managedRestaurant.value) return;
    try {
        // Passa o ID do restaurante gerido atualmente
        await managementStore.updateTableStatus(managedRestaurant.value.id, selectedTable.value.id, newStatus);

        // Atualiza a lista de restaurantes para obter o novo mapa
        await restaurantStore.fetchRestaurantsFromAPI();
        selectedTable.value = null; // Fecha o modal
    } catch (error) {
        console.error("Erro ao alterar status:", error);
        // showToast(error, 'error');
    }
};

const onRestaurantChange = () => {
    managementStore.fetchManagementData(selectedRestaurantId.value);
};

onMounted(() => {
    if (authStore.currentUser?.role === 'admin' && restaurantStore.restaurants.length > 0) {
        selectedRestaurantId.value = restaurantStore.restaurants[0].id;
    }
    managementStore.fetchManagementData(selectedRestaurantId.value || authStore.currentUser?.restaurant_id);
});
</script>