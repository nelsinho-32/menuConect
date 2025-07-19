<template>
    <div @click.self="$emit('close')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-xs w-full shadow-2xl p-6 text-center">
            <h3 class="text-xl font-bold text-gray-800 mb-1">Mesa {{ table.id }}</h3>
            <p class="text-gray-500 mb-6">{{ getStatusText() }}</p>
            
            <div class="flex flex-col gap-3">
                <!-- Ações para mesa disponível -->
                <template v-if="table.status === 'available' && !isMyBooking">
                    <button @click="$emit('book')" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700">Reservar esta mesa</button>
                </template>

                <!-- Ações para mesa ocupada -->
                <template v-if="table.status === 'occupied' && !isMyBooking">
                     <button @click="$emit('joinWaitlist')" class="w-full bg-orange-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-orange-600">Entrar na fila de espera</button>
                </template>

                <!-- Ações para a sua reserva -->
                <template v-if="isMyBooking">
                     <p class="text-sm bg-blue-100 text-blue-800 p-3 rounded-lg">Esta é a sua reserva atual.</p>
                     <button @click="$emit('cancel')" class="w-full bg-red-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-red-600">Cancelar reserva</button>
                </template>

                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Voltar</button>
            </div>
        </div>
    </div>
</template>
<script setup>
import { computed } from 'vue';
const props = defineProps({ 
    table: { type: Object, required: true },
    userReservations: { type: Object, required: true },
    restaurant: { type: Object, required: true }
});
defineEmits(['close', 'book', 'joinWaitlist', 'cancel']);

const isMyBooking = computed(() => props.userReservations.bookedTable?.tableId === props.table.id);

const getStatusText = () => {
    if (isMyBooking.value) return "Você tem esta mesa reservada.";
    if (props.table.status === 'available') return "Esta mesa está disponível.";
    if (props.table.status === 'occupied') return "Esta mesa está ocupada no momento.";
    return "";
};
</script>