<template>
    <div @click.self="closeModal" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-2xl w-full shadow-2xl relative max-h-[90vh] flex flex-col">
            <div class="p-6 border-b flex justify-between items-start">
                <div>
                    <h3 class="text-2xl font-bold text-gray-800">Atendimento da Mesa {{ table.id }}</h3>
                    <p v-if="session" class="text-sm text-gray-500">Iniciado em: {{ formattedStartTime }} ({{ elapsedTime }})</p>
                    <p v-else class="text-sm text-gray-500">Status: Ocupada (sem sessão iniciada)</p>
                </div>
                <button @click="closeModal" class="text-gray-400 hover:text-gray-600 text-2xl">&times;</button>
            </div>

            <div class="p-6 overflow-y-auto flex-grow">
                <div v-if="sessionStore.state.isLoading">Carregando dados do atendimento...</div>
                <div v-else-if="sessionStore.state.error && sessionStore.state.error !== 'Nenhuma sessão ativa encontrada para esta mesa.'" class="text-red-500">{{ sessionStore.state.error }}</div>
                <div v-else>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div>
                            <div class="bg-gray-50 p-4 rounded-lg">
                                <h4 class="font-bold text-gray-700 mb-2">Clientes na Mesa ({{ session?.guests || 'N/A' }})</h4>
                                <ul v-if="session?.customer_names?.length" class="list-disc list-inside text-gray-600 text-sm">
                                    <li v-for="name in session.customer_names" :key="name">{{ name }}</li>
                                </ul>
                                <p v-else class="text-sm text-gray-400">Nenhum nome registado.</p>
                            </div>
                            <div class="mt-4 border-t pt-4">
                                <h4 class="font-bold text-gray-700 mb-2">Ações Rápidas</h4>
                                <div class="flex flex-col gap-2">
                                     <button @click="$emit('changeStatus', 'cleaning')" class="w-full bg-yellow-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-yellow-600">Marcar como "A Limpar"</button>
                                     <button @click="$emit('changeStatus', 'available')" class="w-full bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">Liberar Mesa (Disponível)</button>
                                </div>
                            </div>
                        </div>
                        
                        <div>
                            <h4 class="font-bold text-gray-700 mb-2">Extrato de Consumo</h4>
                            <div class="bg-gray-50 p-4 rounded-lg space-y-3 max-h-64 overflow-y-auto">
                               <p v-if="consumption.length === 0" class="text-sm text-gray-400">Nenhum item consumido ainda.</p>
                               
                               <div v-for="(item, index) in consumption" :key="index" class="text-sm border-b pb-2 last:border-b-0">
                                   <div class="flex justify-between">
                                       <span class="font-semibold">{{ item.quantity }}x {{ item.dishName }}</span>
                                       <span class="font-semibold">R$ {{ (item.price_at_time * item.quantity).toFixed(2).replace('.', ',') }}</span>
                                   </div>
                                   <div v-if="item.customization" class="text-xs mt-1 pl-1 border-l-2 border-indigo-200">
                                        <p v-if="item.customization.removedIngredients?.length" class="text-red-500">Sem: {{ item.customization.removedIngredients.join(', ') }}</p>
                                        <p v-if="item.customization.notes" class="text-gray-500">Nota: {{ item.customization.notes }}</p>
                                    </div>
                               </div>
                            </div>
                             <div class="text-right font-bold text-lg mt-4 pt-2 border-t">
                                Total: R$ {{ totalConsumption.toFixed(2).replace('.', ',') }}
                            </div>
                            <div class="mt-4 flex flex-col gap-2">
                                 <button @click="addOrder" class="w-full bg-indigo-700 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Adicionar Pedido</button>
                                 <button @click="finishSession" class="w-full bg-cyan-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">Finalizar Atendimento</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue';
import { useSessionStore } from '@/stores/sessionStore';

const props = defineProps({
    table: { type: Object, required: true },
    restaurant: { type: Object, required: true }
});

const emit = defineEmits(['close', 'addOrder', 'finishSession', 'changeStatus']); // <-- ADICIONADO 'changeStatus'
const sessionStore = useSessionStore();

const elapsedTime = ref('00:00:00');
let timerInterval = null;

const session = computed(() => sessionStore.state.activeSession?.session);
const consumption = computed(() => sessionStore.state.activeSession?.consumption || []);

const formattedStartTime = computed(() => {
    if (!session.value?.start_time) return '';
    return new Date(session.value.start_time).toLocaleTimeString('pt-BR');
});

const totalConsumption = computed(() => {
    return consumption.value.reduce((sum, item) => sum + (item.price_at_time * item.quantity), 0);
});

const startTimer = () => {
    if (!session.value?.start_time) return;
    const startTime = new Date(session.value.start_time).getTime();
    timerInterval = setInterval(() => {
        const now = new Date().getTime();
        const distance = now - startTime;
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        elapsedTime.value = `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    }, 1000);
};

onMounted(() => {
    sessionStore.fetchActiveSessionForTable(props.restaurant.id, props.table.id)
        .then(() => {
            if (session.value) {
                startTimer();
            }
        });
});

onUnmounted(() => {
    clearInterval(timerInterval);
    sessionStore.clearActiveSession();
});
const addOrder = () => {
    // CORREÇÃO: Envia o objeto 'session' completo no payload do evento.
    emit('addOrder', {
        session: session.value,
        restaurant: props.restaurant
    });
};
const closeModal = () => emit('close');
const finishSession = () => {
    // CORREÇÃO: Emite o objeto 'session' completo, que já temos
    // na nossa propriedade computada 'session'.
    emit('finishSession', {
        session: session.value,
        consumption: consumption.value
    });
};
</script>