<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-xs w-full shadow-2xl p-6 text-center relative">
            <button @click="$emit('openConfig')" title="Configurar Mesa" class="absolute top-4 right-4 text-gray-400 hover:text-indigo-600">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311a1.464 1.464 0 0 1-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705 1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/>
                </svg>
            </button>

            <h3 class="text-xl font-bold text-gray-800 mb-1">Mesa {{ table.id }}</h3>
            <p class="text-gray-500 mb-6">{{ getStatusText() }}</p>
            
            <div class="flex flex-col gap-3">
                <template v-if="table.status === 'available' && !isMyBooking">
                    <button @click="$emit('book')" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700">Reservar esta mesa</button>
                </template>

                <template v-if="table.status === 'occupied' && !isMyBooking">
                     <button @click="$emit('joinWaitlist')" class="w-full bg-orange-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-orange-600">Entrar na fila de espera</button>
                </template>

                <template v-if="isMyBooking">
                     <p class="text-sm bg-blue-100 text-blue-800 p-3 rounded-lg">Esta é a sua reserva atual.</p>
                     <button @click="$emit('cancel')" class="w-full bg-red-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-red-600">Cancelar reserva</button>
                </template>
                
                <button v-if="table.images && table.images.length" @click="$emit('viewTable')" class="w-full bg-gray-800 text-white px-6 py-3 rounded-lg font-bold hover:bg-black">
                    🖼️ Ver Mesa
                </button>

                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-bold hover:bg-gray-300 mt-2">Voltar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({ 
    table: { type: Object, required: true },
    userReservations: { type: Object, required: true }
});

defineEmits(['close', 'book', 'joinWaitlist', 'cancel', 'viewTable', 'openConfig']);

const isMyBooking = computed(() => props.userReservations?.bookedTable?.tableId === props.table.id);

const getStatusText = () => {
    if (isMyBooking.value) return "Você tem esta mesa reservada.";
    if (props.table.status === 'available') return "Esta mesa está disponível.";
    if (props.table.status === 'occupied') return "Esta mesa está ocupada no momento.";
    return "";
};
</script>