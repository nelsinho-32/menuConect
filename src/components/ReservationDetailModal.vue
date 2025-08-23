<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl max-h-[90vh] flex flex-col">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Detalhes da Reserva</h3>
                <p class="text-gray-500">Mesa: <span class="font-bold text-indigo-600">{{ reservation.table_id }}</span></p>
            </div>

            <div class="p-6 space-y-6 overflow-y-auto">
                <div>
                    <h4 class="font-semibold text-gray-700">Informações Gerais</h4>
                    <div class="text-sm space-y-1 mt-2">
                        <p><strong>Cliente:</strong> {{ reservation.user_name }}</p>
                        <p><strong>Horário:</strong> {{ formattedBookingTime }}</p>
                        <p><strong>Pessoas:</strong> {{ reservation.guests }}</p>
                        <p><strong>Contato:</strong> {{ reservation.user_phone || 'Não informado' }}</p>
                    </div>
                </div>

                <div v-if="reservation.encontro_id">
                    <h4 class="font-semibold text-gray-700">Encontro Planejado</h4>
                    <div class="text-sm space-y-1 mt-2">
                         <p><strong>Pagamento:</strong> <span :class="paymentClass">{{ paymentStatus }}</span></p>
                    </div>
                    <div class="mt-4 space-y-3">
                        <div v-for="(guest, index) in reservation.encontro_details" :key="index" class="bg-gray-50 p-3 rounded-lg">
                            <p class="font-bold text-gray-800">{{ guest.guest_name }}</p>
                            <ul class="list-disc list-inside text-xs text-gray-600 pl-2 mt-1">
                                <li v-if="guest.menu_selection.starter?.dishName">Entrada: {{ guest.menu_selection.starter.dishName }}</li>
                                <li v-if="guest.menu_selection.main?.dishName">Principal: {{ guest.menu_selection.main.dishName }}</li>
                                <li v-if="guest.menu_selection.dessert?.dishName">Sobremesa: {{ guest.menu_selection.dessert.dishName }}</li>
                                <li v-if="guest.menu_selection.drink?.dishName">Bebida: {{ guest.menu_selection.drink.dishName }}</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
             <div class="p-4 bg-gray-50 border-t flex justify-end">
                <button @click="$emit('close')" class="bg-indigo-600 text-white font-bold py-2 px-6 rounded-lg hover:bg-indigo-700">Fechar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    reservation: { type: Object, required: true }
});

defineEmits(['close']);

const formattedBookingTime = computed(() => {
    if (!props.reservation.booking_time) return 'N/A';
    return new Date(props.reservation.booking_time).toLocaleString('pt-BR', {
        day: '2-digit', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit'
    });
});

const paymentStatus = computed(() => {
    if (props.reservation.payment_option === 'agora') return 'Pago (Online)';
    if (props.reservation.payment_option === 'local') return 'Pagar no Local';
    return 'Não especificado';
});

const paymentClass = computed(() => {
    return props.reservation.payment_option === 'agora' 
        ? 'font-semibold text-green-700' 
        : 'font-semibold text-orange-700';
});
</script>