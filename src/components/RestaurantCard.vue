<template>
    <div 
        class="restaurant-card w-80 md:w-96 h-96 rounded-2xl overflow-hidden relative text-white flex flex-col justify-end p-6 bg-cover bg-center" 
        :style="{ backgroundImage: `url(${restaurant.imageUrl})` }"
    >
        <!-- Gradiente Overlay para legibilidade -->
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>

        <!-- Conteúdo do Card -->
        <div class="relative z-10">
            <span class="inline-block bg-white/20 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1 rounded-full mb-2">{{ restaurant.cuisine }}</span>
            <h3 class="text-3xl font-bold leading-tight">{{ restaurant.name }}</h3>
            
            <div class="text-sm text-gray-200 mt-2 min-h-[40px] transition-opacity duration-300" :class="reason ? 'opacity-100' : 'opacity-0'">
                <p v-if="!isLoading">{{ reason }}</p>
            </div>

            <button 
                @click="getReason" 
                class="mt-4 text-white font-semibold flex items-center gap-2 group" 
                :disabled="isLoading"
            >
                <span v-if="!isLoading">Por que visitar?</span>
                <span v-if="isLoading">Analisando...</span>
                <div v-if="isLoading" class="w-4 h-4 border-2 border-white/50 border-t-white rounded-full animate-spin"></div>
                <span v-else class="transition-transform duration-300 group-hover:translate-x-1">✨</span>
            </button>
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
    // Transforma o botão em um 'toggle' para mostrar/esconder a razão
    if (reason.value) {
        reason.value = '';
        return;
    }
    isLoading.value = true;
    const schema = { type: "OBJECT", properties: { reason: { type: "STRING" } } };
    const prompt = `Crie uma frase curta e convidativa (máximo 15 palavras) dizendo por que uma pessoa deveria visitar o restaurante '${props.restaurant.name}', que é do tipo '${props.restaurant.cuisine}'. Foque na atmosfera ou na experiência.`;
    const result = await callGemini(prompt, schema);
    reason.value = (result && result.reason) ? result.reason : `Um lugar perfeito para apreciar a culinária ${props.restaurant.cuisine}!`;
    isLoading.value = false;
}
</script>

<style scoped>
/* Efeito de hover aprimorado para dar profundidade */
.restaurant-card {
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.restaurant-card:hover {
    transform: translateY(-8px) scale(1.03);
    box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.2), 0 8px 10px -6px rgb(0 0 0 / 0.1);
}
</style>