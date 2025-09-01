<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl text-center">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Status do Pedido #{{ orderId }}</h3>
            </div>
            <div class="p-6">
                <div v-if="isLoading" class="py-8">A carregar status...</div>
                <div v-else class="space-y-4">
                    <div v-for="(step, index) in steps" :key="step.name" class="flex items-center">
                        <div class="w-8 h-8 rounded-full flex items-center justify-center text-white" :class="getStepClass(index)">
                            <span v-if="index < currentStepIndex">✓</span>
                            <span v-else>{{ index + 1 }}</span>
                        </div>
                        <p class="ml-4 font-semibold" :class="{'text-gray-800': index <= currentStepIndex, 'text-gray-400': index > currentStepIndex}">
                            {{ step.label }}
                        </p>
                    </div>
                </div>
            </div>
            <div class="p-4 bg-gray-100 border-t">
                <button @click="$emit('close')" class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Fechar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useOrderStore } from '@/stores/orderStore';

const props = defineProps({
    orderId: { type: Number, required: true }
});
defineEmits(['close']);

const orderStore = useOrderStore();
const isLoading = ref(true);
const orderStatus = ref('');

const steps = [
    { name: 'confirmed', label: 'Pedido Confirmado' },
    { name: 'preparing', label: 'Em Preparação' },
    { name: 'out_for_delivery', label: 'Saiu para Entrega' },
    { name: 'completed', label: 'Entregue' }
];

const currentStepIndex = computed(() => {
    const index = steps.findIndex(step => step.name === orderStatus.value);
    return index === -1 ? 0 : index;
});

const getStepClass = (index) => {
    if (index < currentStepIndex.value) return 'bg-green-500'; // Concluído
    if (index === currentStepIndex.value) return 'bg-indigo-600 animate-pulse'; // Atual
    return 'bg-gray-300'; // Pendente
};

onMounted(async () => {
    try {
        const statusData = await orderStore.fetchOrderStatus(props.orderId);
        orderStatus.value = statusData.status;
    } catch (error) {
        console.error("Erro ao buscar status do pedido:", error);
    } finally {
        isLoading.value = false;
    }
});
</script>