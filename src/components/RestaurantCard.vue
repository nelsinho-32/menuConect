<template>
    <div class="restaurant-card w-80 md:w-96">
        <img class="h-56 w-full object-cover" :src="restaurant.imageUrl" :alt="'Imagem de ' + restaurant.name">
        <div class="p-5">
            <h3 class="text-2xl font-bold text-gray-900">{{ restaurant.name }}</h3>
            <p class="text-gray-500 text-md">{{ restaurant.cuisine }}</p>
            <div class="text-sm text-gray-700 mt-2 min-h-[40px]">
                <div v-if="isLoading" class="flex items-center"><div class="loader-dark w-4 h-4"></div><p class="ml-2 text-sm text-gray-500">Buscando um bom motivo...</p></div>
                <p v-else>{{ reason }}</p>
            </div>
            <button @click="getReason" class="mt-4 text-indigo-600 font-semibold hover:text-indigo-800">Por que visitar? ✨</button>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { callGemini } from '../services/geminiService.js';
const props = defineProps({
  restaurant: {
    type: Object,
    required: true
  }
});
const reason = ref('');
const isLoading = ref(false);
async function getReason() {
    isLoading.value = true;
    const schema = { type: "OBJECT", properties: { reason: { type: "STRING" } } };
    const prompt = `Crie uma frase curta e convidativa (máximo 15 palavras) dizendo por que uma pessoa deveria visitar o restaurante '${props.restaurant.name}', que é do tipo '${props.restaurant.cuisine}'. Foque na atmosfera ou na experiência.`;
    const result = await callGemini(prompt, schema);
    reason.value = (result && result.reason) ? result.reason : `Um lugar perfeito para apreciar a culinária ${props.restaurant.cuisine}!`;
    isLoading.value = false;
}
</script>