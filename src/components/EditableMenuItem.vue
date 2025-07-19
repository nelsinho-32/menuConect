<template>
    <div class="flex items-center justify-between">
        <div>
            <p class="font-semibold text-gray-500 uppercase text-xs">{{ label }}</p>
            <p class="text-gray-800">{{ item }}</p>
        </div>
        <button @click="regenerate" :disabled="isLoading" class="p-2 rounded-full hover:bg-gray-200 transition-colors">
            <div v-if="isLoading" class="w-4 h-4 border-2 border-gray-300 border-t-indigo-500 rounded-full animate-spin"></div>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-500"><path d="M21 12a9 9 0 0 0-9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"/><path d="M3 3v5h5"/><path d="M3 12a9 9 0 0 0 9 9 9.75 9.75 0 0 0 6.74-2.74L21 16"/><path d="M21 21v-5h-5"/></svg>
        </button>
    </div>
</template>

<script setup>
import { ref, getCurrentInstance } from 'vue';
import { callGemini } from '../services/geminiService';

const props = defineProps({
    label: String,
    item: String
});
const emit = defineEmits(['regenerate']);

const isLoading = ref(false);

const parentProps = getCurrentInstance().parent.props;

async function regenerate() {
    isLoading.value = true;
    const schema = { type: "OBJECT", properties: { itemName: { type: "STRING" } } };
    const prompt = `Sugira um item diferente para '${props.label}' que combine com um encontro '${parentProps.initialSuggestion.title}' em um restaurante '${parentProps.restaurantTheme}'. O item atual é '${props.item}'. Escolha uma opção do seguinte cardápio: ${JSON.stringify(parentProps.restaurantMenu)}. Responda apenas com o nome do novo item.`;
    
    const result = await callGemini(prompt, schema);
    emit('regenerate', result);
    isLoading.value = false;
}
</script>
