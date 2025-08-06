<template>
    <div class="bg-white rounded-lg shadow-xl overflow-hidden">
        <img :src="reservation.restaurantImage" :alt="reservation.restaurantName" class="w-full h-48 object-cover">
        <div class="p-6">
            <span v-if="reservationStatus === 'confirmed'" class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2">
                RESERVA CONFIRMADA
            </span>
            <span v-if="reservationStatus === 'pending'" class="inline-block bg-yellow-100 text-yellow-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2 animate-pulse">
                AGUARDA CONFIRMAÇÃO
            </span>
            <span v-if="reservationStatus === 'cancelled'" class="inline-block bg-red-100 text-red-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2">
                CANCELADA
            </span>
            <span v-if="type === 'waiting'" class="inline-block bg-orange-100 text-orange-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2">
                FILA DE ESPERA
            </span>

            <h3 class="text-2xl font-bold text-gray-800">{{ reservation.restaurantName }}</h3>
            <p class="text-gray-600">Mesa {{ reservation.tableId }}</p>

            <div v-if="type === 'booked'" class="mt-4 border-t pt-4">
                <p class="text-sm font-semibold text-gray-700">Sua reserva é às:</p>
                <p class="text-lg font-bold text-indigo-600">{{ formattedBookingTime }}</p>
                <div class="mt-2">
                    <p class="text-xs text-gray-500">Tempo restante para sua reserva:</p>
                    <p class="text-sm font-mono" :class="isExpired ? 'text-gray-500' : 'text-red-600'">{{ countdown }}</p>
                </div>
            </div>

            <div v-if="type === 'waiting'" class="mt-4 border-t pt-4">
                <p class="text-sm font-semibold text-gray-700">Sua posição na fila:</p>
                <p class="text-3xl font-bold text-indigo-600">{{ reservation.position }}º lugar</p>
            </div>

            <div class="mt-6 flex flex-col gap-3">
                 <div v-if="reservationStatus === 'pending'" class="bg-yellow-50 border border-yellow-200 p-4 rounded-lg text-center">
                    <p class="text-sm font-semibold text-yellow-800">Por favor, confirme a sua presença!</p>
                    <p class="text-xs text-yellow-700 mt-1">A reserva será cancelada em {{ confirmationCountdown }} se não for confirmada.</p>
                    <button @click="confirmReservation" class="mt-3 w-full bg-green-500 text-white px-4 py-2 rounded-lg font-bold hover:bg-green-600">
                        Confirmar Presença
                    </button>
                 </div>

                 <button v-if="reservationStatus !== 'cancelled'" @click="$emit('cancel', type)" class="w-full bg-red-100 text-red-800 px-4 py-2 rounded-lg font-bold hover:bg-red-200 text-sm">
                    {{ type === 'booked' ? 'Cancelar Reserva' : 'Sair da Fila' }}
                 </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue';

const props = defineProps({
    reservation: { type: Object, required: true },
    type: { type: String, required: true }
});
const emit = defineEmits(['cancel', 'confirm']);

const countdown = ref('');
const confirmationCountdown = ref('');
const isExpired = ref(false);
const reservationStatus = ref(props.reservation.status || 'confirmed');
const hasBeenManuallyConfirmed = ref(false);
let intervalId = null;

watch(() => props.reservation.status, (newStatus) => {
  reservationStatus.value = newStatus;
  if(newStatus === 'confirmed') {
    hasBeenManuallyConfirmed.value = true;
  }
});

const formattedBookingTime = computed(() => {
    if (!props.reservation.bookingTime) return 'N/A';
    return new Date(props.reservation.bookingTime).toLocaleString('pt-BR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
});

const updateTimers = () => {
    if (!props.reservation.bookingTime) return;

    const now = new Date();
    const bookingTime = new Date(props.reservation.bookingTime);
    const diffMillis = bookingTime - now;

    if (diffMillis <= 0) {
        countdown.value = "Reserva expirada";
        isExpired.value = true;
        if (reservationStatus.value !== 'confirmed') {
             reservationStatus.value = 'cancelled';
        }
        clearInterval(intervalId);
        return;
    }
    
    const days = Math.floor(diffMillis / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diffMillis % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diffMillis % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diffMillis % (1000 * 60)) / 1000);
    countdown.value = `${days > 0 ? days + 'd ' : ''}${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;

    // --- LÓGICA DE CONFIRMAÇÃO CORRIGIDA ---
    const confirmationWindowStart = 40 * 60 * 1000; // 40 min
    const confirmationTimeout = 20 * 60 * 1000; // 20 min

    // Só entra em estado 'pending' se a reserva estiver a MAIS de 20 minutos de distância E dentro da janela de 40 min.
    if (diffMillis <= confirmationWindowStart && diffMillis > confirmationTimeout && reservationStatus.value === 'confirmed' && !hasBeenManuallyConfirmed.value) {
        reservationStatus.value = 'pending';
    }

    if (reservationStatus.value === 'pending') {
        const timeToExpire = diffMillis - confirmationTimeout;
        if (timeToExpire <= 0) {
            reservationStatus.value = 'cancelled';
            confirmationCountdown.value = 'Expirado';
        } else {
            const minutesToExpire = Math.floor(timeToExpire / (1000 * 60));
            const secondsToExpire = Math.floor((timeToExpire % (1000 * 60)) / 1000);
            confirmationCountdown.value = `${String(minutesToExpire).padStart(2, '0')}:${String(secondsToExpire).padStart(2, '0')}`;
        }
    }
};

const confirmReservation = () => {
    hasBeenManuallyConfirmed.value = true;
    reservationStatus.value = 'confirmed';
    emit('confirm', props.reservation);
};

onMounted(() => {
    if (props.type === 'booked') {
        updateTimers();
        intervalId = setInterval(updateTimers, 1000);
    }
});

onUnmounted(() => {
    clearInterval(intervalId);
});
</script>