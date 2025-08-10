<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b flex justify-between items-start">
                <div>
                    <h3 class="text-2xl font-bold text-gray-800">Detalhes da Mesa {{ table.id }}</h3>
                    <span class="text-xs font-semibold px-2 py-0.5 rounded-full mt-1 inline-block" :class="getStatusBgColor(table.status)">
                        {{ getStatusText(table.status) }}
                    </span>
                </div>
                <button @click="$emit('close')" class="text-gray-400 hover:text-gray-600">&times;</button>
            </div>

            <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
                <div v-if="reservationDetails">
                    <h4 class="font-bold text-gray-700 mb-2">Reserva Ativa</h4>
                    <div class="bg-gray-50 p-4 rounded-lg flex items-center gap-4">
                        <img :src="userProfile.avatarUrl" class="w-12 h-12 rounded-full">
                        <div>
                            <p class="font-semibold text-gray-800">{{ userProfile.name }}</p>
                            <p class="text-sm text-gray-500">Ocupada há: <span class="font-mono">{{ occupationTimer }}</span></p>
                        </div>
                    </div>
                </div>

                <div>
                    <h4 class="font-bold text-gray-700 mb-2">Consumo na Mesa</h4>
                    <div v-if="ordersOnTable.length" class="space-y-2">
                        <div v-for="order in ordersOnTable" :key="order.id" class="border-b pb-2">
                             <p class="text-xs text-gray-400">Pedido #{{ order.id }}</p>
                             <div v-for="item in order.items" :key="item.cartItemId" class="flex flex-col text-sm pt-2">
                                <div class="flex justify-between items-center">
                                    <span>{{ item.quantity }}x {{ item.dishName }}</span>
                                    <span class="font-semibold">R$ {{ (item.price * item.quantity).toFixed(2).replace('.',',') }}</span>
                                </div>
                                <div v-if="getRemovedIngredients(item).length" class="text-xs text-red-500 mt-1 pl-4">
                                    <span class="font-semibold">Sem:</span> {{ getRemovedIngredients(item) }}
                                </div>
                                <div v-if="item.customization && item.customization.notes" class="text-xs text-gray-500 mt-1 pl-4">
                                    <span class="font-semibold">Notas:</span> {{ item.customization.notes }}
                                </div>
                             </div>
                        </div>
                    </div>
                    <p v-else class="text-sm text-gray-400 text-center py-4">Nenhum pedido registado para esta mesa.</p>
                </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-b-2xl">
                <h4 class="text-sm font-medium text-gray-700 mb-2">Alterar Status da Mesa</h4>
                <div class="flex gap-2">
                    <button @click="updateStatus('available')" class="flex-1 bg-green-100 text-green-800 py-2 rounded-lg font-bold hover:bg-green-200">Disponível</button>
                    <button @click="updateStatus('occupied')" class="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg font-bold hover:bg-gray-300">Ocupada</button>
                    <button @click="updateStatus('cleaning')" class="flex-1 bg-yellow-100 text-yellow-800 py-2 rounded-lg font-bold hover:bg-yellow-200">A Limpar</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
    table: { type: Object, required: true },
    reservations: { type: Object, required: true },
    orderHistory: { type: Array, required: true },
    userProfile: { type: Object, required: true }
});
const emit = defineEmits(['close', 'updateStatus']);

const occupationTimer = ref('00:00:00');
let timerInterval = null;

const reservationDetails = computed(() => {
    if (props.reservations.bookedTable && props.reservations.bookedTable.tableId === props.table.id) {
        return props.reservations.bookedTable;
    }
    return null;
});

const ordersOnTable = computed(() => {
    if (!reservationDetails.value || !reservationDetails.value.orderIds) return [];
    return props.orderHistory.filter(order => reservationDetails.value.orderIds.includes(order.id));
});

// AQUI ESTÁ A ALTERAÇÃO: Nova função para calcular ingredientes removidos
const getRemovedIngredients = (item) => {
    if (!item.customization || !item.description) return '';
    const initialIngredients = new Set((item.description).split(',').map(i => i.trim()).filter(Boolean));
    const customizedIngredients = new Set((item.customization.ingredients || '').split(',').map(i => i.trim()).filter(Boolean));
    return Array.from(initialIngredients).filter(i => !customizedIngredients.has(i)).join(', ');
};

const updateStatus = (newStatus) => {
    emit('updateStatus', { tableId: props.table.id, status: newStatus });
};

const updateTimer = () => {
    if (!reservationDetails.value) return;
    const now = new Date();
    const bookingTime = new Date(reservationDetails.value.bookingTime);
    const diff = now - bookingTime;

    const hours = Math.floor(diff / 3600000);
    const minutes = Math.floor((diff % 3600000) / 60000);
    const seconds = Math.floor((diff % 60000) / 1000);
    
    occupationTimer.value = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
};


onMounted(() => {
    updateTimer();
    timerInterval = setInterval(updateTimer, 1000);
});
onUnmounted(() => clearInterval(timerInterval));


const getStatusBgColor = (status) => {
    if (status === 'available') return 'bg-green-100 text-green-800';
    if (status === 'occupied') return 'bg-gray-200 text-gray-800';
    if (status === 'cleaning') return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
}

const getStatusText = (status) => {
    if (status === 'available') return 'Disponível';
    if (status === 'occupied') return 'Ocupada';
    if (status === 'cleaning') return 'A Limpar';
    return 'Indefinido';
}
</script>