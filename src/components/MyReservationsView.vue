<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        <h1 class="text-3xl font-bold">Minhas Reservas e Filas</h1>

        <div v-if="reservations.booked.length === 0 && reservations.waiting.length === 0"
            class="mt-8 text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você não tem nenhuma reserva ou fila de espera ativa.</p>
        </div>

        <div v-else class="mt-8 grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
            <div>
                <h2 class="text-2xl font-bold mb-4 text-gray-800">Suas Próximas Reservas</h2>
                <div v-if="reservations.booked.length > 0" class="space-y-6">
                    <ReservationCard v-for="res in reservations.booked" :key="res.id" :reservation="res" type="booked"
                        @cancel="() => $emit('cancelReservation', res)"
                        @confirm="() => $emit('confirmReservation', res)"
                        @open-chat="context => chatStore.openChat(context)" />
                </div>
                <div v-else class="bg-white p-6 rounded-lg shadow-md text-center text-gray-400">
                    <p>Nenhuma mesa reservada.</p>
                </div>
            </div>

            <div>
                <h2 class="text-2xl font-bold mb-4 text-gray-800">Filas de Espera</h2>
                 <div v-if="reservations.waiting.length > 0" class="space-y-6">
                    <ReservationCard v-for="wait in reservations.waiting" :key="wait.id" :reservation="wait" type="waiting"
                        @cancel="() => $emit('cancelWaitlist', wait)" />
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
    // A prop 'reservations' continua a ser um Objecto, o que está correto
    reservations: { type: Object, required: true }
});

defineEmits(['cancelReservation', 'backToMain', 'confirmReservation', 'cancelWaitlist']);
</script>