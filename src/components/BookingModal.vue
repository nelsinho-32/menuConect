<template>
    <div @click.self="$emit('close')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Confirmar Reserva</h3>
                <p class="text-gray-500">Mesa {{ table.id }} em {{ restaurant.name }}</p>
            </div>
            <div class="p-6 space-y-4">
                <div>
                    <label for="date" class="block text-sm font-medium text-gray-700">Data</label>
                    <input type="date" id="date" v-model="bookingDate" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                </div>
                <div>
                    <label for="time" class="block text-sm font-medium text-gray-700">Horário</label>
                    <input type="time" id="time" v-model="bookingTime" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                </div>
                 <div>
                    <label for="guests" class="block text-sm font-medium text-gray-700">Número de Pessoas</label>
                    <input type="number" id="guests" v-model="numberOfGuests" min="1" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                    </div>
            </div>
            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Cancelar</button>
                <button @click="onConfirm" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Confirmar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
  table: { type: Object, required: true },
  restaurant: { type: Object, required: true }
});
const emit = defineEmits(['close', 'confirmBooking']);

const today = new Date();
const bookingDate = ref(today.toISOString().split('T')[0]);
const bookingTime = ref(`${String(today.getHours()).padStart(2, '0')}:${String(today.getMinutes()).padStart(2, '0')}`);
const numberOfGuests = ref(2); // INÍCIO DA ALTERAÇÃO: Variável para guardar o número de pessoas

const onConfirm = () => {
    const [year, month, day] = bookingDate.value.split('-').map(Number);
    const [hours, minutes] = bookingTime.value.split(':').map(Number);
    const dateTime = new Date(year, month - 1, day, hours, minutes);
    
    if (dateTime < new Date()) {
        alert("Não é possível fazer uma reserva para uma data ou hora no passado.");
        return;
    }

    // INÍCIO DA ALTERAÇÃO: Envia também o número de pessoas
    emit('confirmBooking', { dateTime, guests: numberOfGuests.value });
};
</script>