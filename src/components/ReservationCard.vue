<template>
    <div class="bg-white rounded-lg shadow-xl overflow-hidden">
        <img :src="reservation.restaurantImage" :alt="reservation.restaurantName" class="w-full h-48 object-cover">
        <div class="p-6">
            <span v-if="type === 'booked'" class="inline-block bg-blue-100 text-blue-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2">RESERVA CONFIRMADA</span>
            <span v-if="type === 'waiting'" class="inline-block bg-orange-100 text-orange-800 text-xs font-semibold px-2.5 py-0.5 rounded-full mb-2">FILA DE ESPERA</span>

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
                 <button v-if="type === 'booked'" @click="getNightTips" class="w-full bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg font-bold hover:bg-indigo-100 text-sm" :disabled="isTipLoading">
                    <span v-if="!isTipLoading">✨ Dicas para a Noite</span>
                    <span v-else>A procurar dicas...</span>
                 </button>
                 <button v-if="type === 'waiting'" @click="getWaitlistTip" class="w-full bg-orange-50 text-orange-700 px-4 py-2 rounded-lg font-bold hover:bg-orange-100 text-sm" :disabled="isTipLoading">
                    <span v-if="!isTipLoading">👀 Ver quem está na frente?</span>
                    <span v-else>A espreitar...</span>
                 </button>
                 <button @click="$emit('cancel', type)" class="w-full bg-red-100 text-red-800 px-4 py-2 rounded-lg font-bold hover:bg-red-200 text-sm">
                    {{ type === 'booked' ? 'Cancelar Reserva' : 'Sair da Fila' }}
                 </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { callGemini } from '../services/geminiService';

const props = defineProps({
    reservation: { type: Object, required: true },
    type: { type: String, required: true } // 'booked' ou 'waiting'
});
defineEmits(['cancel']);

const countdown = ref('');
const isTipLoading = ref(false);
const isExpired = ref(false);
let intervalId = null;

const formattedBookingTime = computed(() => {
    if (!props.reservation.bookingTime) return 'N/A';
    return new Date(props.reservation.bookingTime).toLocaleString('pt-BR', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' });
});

const updateCountdown = () => {
    if (!props.reservation.bookingTime) return;
    const now = new Date();
    const bookingTime = new Date(props.reservation.bookingTime);

    if (now >= bookingTime) {
        countdown.value = "Reserva expirada";
        isExpired.value = true;
        clearInterval(intervalId);
        return;
    }

    const diff = bookingTime - now;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((diff % (1000 * 60)) / 1000);
    
    if (days > 0) {
        countdown.value = `${days}d ${String(hours).padStart(2, '0')}h ${String(minutes).padStart(2, '0')}m`;
    } else {
        countdown.value = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }
};

async function getNightTips() {
    isTipLoading.value = true;
    const schema = { type: "OBJECT", properties: { tip: { type: "STRING" } } };
    const prompt = `Dê uma dica criativa e curta para um encontro no restaurante '${props.reservation.restaurantName}'. A dica pode ser sobre um prato, uma bebida ou a atmosfera do lugar.`;
    const result = await callGemini(prompt, schema);
    if (result && result.tip) {
        alert(`Dica do Chef: ${result.tip}`);
    } else {
        alert("Não foi possível procurar uma dica no momento.");
    }
    isTipLoading.value = false;
}

async function getWaitlistTip() {
    isTipLoading.value = true;
    const schema = { type: "OBJECT", properties: { tip: { type: "STRING" } } };
    const prompt = `Estou na fila de espera para a mesa ${props.reservation.tableId} no restaurante '${props.reservation.restaurantName}'. Crie uma descrição curta, divertida e anónima de quem poderia estar a ocupar a mesa agora (ex: 'Um casal a comemorar um aniversário', 'Alguém a planear uma surpresa').`;
    const result = await callGemini(prompt, schema);
    if (result && result.tip) {
        alert(`Quem sabe? Talvez na sua mesa esteja... ${result.tip}`);
    } else {
        alert("Não foi possível espreitar quem está na mesa agora.");
    }
    isTipLoading.value = false;
}

onMounted(() => {
    if (props.type === 'booked') {
        updateCountdown();
        intervalId = setInterval(updateCountdown, 1000);
    }
});

onUnmounted(() => {
    clearInterval(intervalId);
});
</script>