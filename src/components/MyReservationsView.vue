<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para
            a página principal</button>
        <h1 class="text-3xl font-bold">Minhas Reservas</h1>

        <div v-if="!reservations.bookedTable && !reservations.waitingForTable"
            class="mt-8 text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não tem nenhuma reserva ou fila de espera ativa.</p>
        </div>

        <div v-else class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
            <div>
                <h2 class="text-2xl font-bold mb-4 text-gray-800">Sua Próxima Reserva</h2>
                <div v-if="reservations.bookedTable">
                    <ReservationCard :reservation="reservations.bookedTable" type="booked"
                        @cancel="type => $emit('cancelReservation', type)"
                        @confirm="reservation => $emit('confirmReservation', reservation)"
                        @open-chat="context => chatStore.openChat(context)" />
                </div>
                <div v-else class="bg-white p-6 rounded-lg shadow-md text-center text-gray-400">
                    <p>Nenhuma mesa reservada.</p>
                </div>
            </div>

            <div>
                <h2 class="text-2xl font-bold mb-4 text-gray-800">Mesa em Fila de Espera</h2>
                <div v-if="reservations.waitingForTable">
                    <ReservationCard :reservation="reservations.waitingForTable" type="waiting"
                        @cancel="type => $emit('cancelReservation', type)" />
                </div>
                <div v-else class="bg-white p-6 rounded-lg shadow-md text-center text-gray-400">
                    <p>Você não está em nenhuma fila.</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import ReservationCard from './ReservationCard.vue';
import { useChatStore } from '@/stores/chatStore';

const chatStore = useChatStore();

defineProps({
    reservations: { type: Object, required: true }
});

// AQUI ESTÁ A CORREÇÃO: Adicionado 'confirmReservation'
defineEmits(['cancelReservation', 'backToMain', 'confirmReservation']);
</script>