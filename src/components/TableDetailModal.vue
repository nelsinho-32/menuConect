<template>
    <div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
        <div>
            <h4 class="font-bold text-gray-700 mb-2 mt-4">Consumo / Itens Pré-selecionados</h4>
            <ul v-if="details.consumption && details.consumption.length > 0" class="list-disc list-inside space-y-1 text-sm text-gray-600">
                <li v-for="(item, index) in details.consumption" :key="index">{{ item }}</li>
            </ul>
            <p v-else class="text-sm text-gray-400 text-center py-4">
                Nenhum consumo registado.
            </p>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
    table: { type: Object, required: true },
    details: { type: Object, required: true }
});
defineEmits(['close']);
const consumptionTotal = computed(() => {
    if (!props.details.consumption) return 0;
    return props.details.consumption.reduce((sum, item) => sum + (item.price_at_time * item.quantity), 0);
});
</script>