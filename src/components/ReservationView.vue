<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold">Reservar em {{ restaurant.name }}</h1>
        <p class="text-gray-500 mb-8">Selecione uma mesa no mapa abaixo.</p>

        <div class="bg-white p-6 rounded-lg shadow-lg relative overflow-hidden">
            <div class="absolute top-4 right-4 flex flex-col md:flex-row gap-4 text-xs z-10">
                <div class="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-2 py-1 rounded-full"><div class="w-4 h-4 rounded bg-green-400"></div> Disponível</div>
                <div class="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-2 py-1 rounded-full"><div class="w-4 h-4 rounded bg-gray-400"></div> Ocupada</div>
                <div class="flex items-center gap-2 bg-white/70 backdrop-blur-sm px-2 py-1 rounded-full"><div class="w-4 h-4 rounded bg-blue-400"></div> Sua Reserva</div>
            </div>
            
            <svg viewBox="0 0 400 300" class="w-full h-auto rounded">
                <defs>
                    <pattern id="floorPattern" patternUnits="userSpaceOnUse" width="50" height="50" patternTransform="rotate(45)">
                        <rect width="50" height="50" fill="#f3e8d8" />
                        <path d="M 0 0 L 50 0" stroke="#d1c0a8" stroke-width="0.5"/>
                        <path d="M 0 25 L 50 25" stroke="#d1c0a8" stroke-width="0.5"/>
                    </pattern>
                    <filter id="dropShadow" x="-20%" y="-20%" width="140%" height="140%">
                        <feGaussianBlur in="SourceAlpha" stdDeviation="1"/>
                        <feOffset dx="1" dy="1" result="offsetblur"/>
                        <feComponentTransfer>
                            <feFuncA type="linear" slope="0.3"/>
                        </feComponentTransfer>
                        <feMerge> 
                            <feMergeNode/>
                            <feMergeNode in="SourceGraphic"/> 
                        </feMerge>
                    </filter>
                </defs>

                <rect width="100%" height="100%" fill="url(#floorPattern)" />
                
                <rect x="10" y="10" width="150" height="30" fill="#a8a29e" rx="5" filter="url(#dropShadow)"/>
                <text x="85" y="30" text-anchor="middle" font-size="10" fill="white" class="font-semibold">BAR</text>
                <rect x="300" y="10" width="90" height="80" fill="#e7e5e4" rx="5" filter="url(#dropShadow)"/>
                <text x="345" y="55" text-anchor="middle" font-size="10" fill="#57534e" class="font-semibold">COZINHA</text>
                
                <g v-for="table in tables" :key="table.id" @click="selectTable(table)" class="cursor-pointer group" filter="url(#dropShadow)">
                    <rect 
                        :x="table.x" :y="table.y" :width="table.width" :height="table.height" 
                        :rx="table.shape === 'round' ? '50%' : '3'"
                        :fill="getTableColor(table)"
                        :class="{'hover:stroke-indigo-500 hover:stroke-2': table.status !== 'occupied'}"
                        class="transition-all"
                    />
                    <text :x="table.x + table.width / 2" :y="table.y + table.height / 2 + 4" text-anchor="middle" font-size="10" fill="white" class="font-bold pointer-events-none">{{ table.id }}</text>
                    
                    <text v-if="table.hasWaitlist" :x="table.x + table.width - 5" :y="table.y + 10" font-size="10">⏳</text>
                </g>
            </svg>
        </div>

        <TableActionModal v-if="selectedTable && isActionModalOpen" 
            :table="selectedTable" 
            :user-reservations="userReservations"
            :restaurant="restaurant"
            @close="isActionModalOpen = false" 
            @book="openBookingView" 
            @join-waitlist="joinWaitlist"
            @cancel="cancelReservation"
        />
        <BookingModal v-if="selectedTable && isBookingModalOpen" :table="selectedTable" :restaurant="restaurant" @close="isBookingModalOpen = false" @confirm-booking="confirmBooking" />
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import TableActionModal from './TableActionModal.vue';
import BookingModal from './BookingModal.vue';

const props = defineProps({ 
    restaurant: { type: Object, required: true },
    userReservations: { type: Object, required: true }
});
const emit = defineEmits(['backToMain', 'bookTable', 'joinWaitlist', 'cancelReservation']);

const tables = reactive([
    { id: 1, x: 20, y: 80, width: 30, height: 30, shape: 'square', status: 'available', hasWaitlist: false },
    { id: 2, x: 70, y: 80, width: 30, height: 30, shape: 'square', status: 'occupied', hasWaitlist: true },
    { id: 3, x: 120, y: 80, width: 30, height: 30, shape: 'square', status: 'available', hasWaitlist: false },
    { id: 4, x: 20, y: 130, width: 50, height: 30, shape: 'rect', status: 'available', hasWaitlist: false },
    { id: 5, x: 90, y: 130, width: 50, height: 30, shape: 'rect', status: 'occupied', hasWaitlist: false },
    { id: 6, x: 200, y: 80, width: 40, height: 40, shape: 'round', status: 'available', hasWaitlist: false },
    { id: 7, x: 260, y: 80, width: 40, height: 40, shape: 'round', status: 'occupied', hasWaitlist: true },
    { id: 8, x: 200, y: 140, width: 80, height: 40, shape: 'rect', status: 'available', hasWaitlist: false },
    { id: 9, x: 50, y: 200, width: 60, height: 60, shape: 'round', status: 'available', hasWaitlist: false },
]);

const selectedTable = ref(null);
const isActionModalOpen = ref(false);
const isBookingModalOpen = ref(false);

const getTableColor = (table) => {
    if (props.userReservations.bookedTable?.tableId === table.id) return '#60a5fa'; // Azul (Sua Reserva)
    if (table.status === 'available') return '#4ade80'; // Verde (Disponível)
    return '#a8a29e'; // Cinza (Ocupada)
};

const selectTable = (table) => {
    selectedTable.value = table;
    isActionModalOpen.value = true;
};

const openBookingView = () => {
    isActionModalOpen.value = false;
    isBookingModalOpen.value = true;
};

const confirmBooking = (bookingDetails) => {
    emit('bookTable', { ...bookingDetails, restaurant: props.restaurant, table: selectedTable.value });
    isBookingModalOpen.value = false;
};

const joinWaitlist = () => {
    emit('joinWaitlist', { restaurant: props.restaurant, table: selectedTable.value });
    isActionModalOpen.value = false;
};

const cancelReservation = () => {
    emit('cancelReservation');
    isActionModalOpen.value = false;
};
</script>