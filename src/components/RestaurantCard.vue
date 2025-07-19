<template>
    <div 
        @click="$emit('viewRestaurant', restaurant)"
        class="restaurant-card w-80 md:w-96 h-96 rounded-2xl overflow-hidden relative text-white flex flex-col justify-end p-6 bg-cover bg-center cursor-pointer" 
        :style="{ backgroundImage: `url(${restaurant.imageUrl})` }"
    >
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>
        <button 
            @click.stop="$emit('toggleFavorite', restaurant)" 
            title="Adicionar aos favoritos" 
            class="absolute top-4 right-4 bg-white/20 backdrop-blur-sm p-2 rounded-full transition-colors duration-200 hover:bg-white/40 z-20"
        >
            <svg xmlns="http://www.w3.org/2000/svg" width="22" height="22" viewBox="0 0 24 24" 
                 :fill="isFavorited ? '#facc15' : 'none'" 
                 stroke="#facc15" 
                 stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                 class="transition-all duration-200"
            >
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon>
            </svg>
        </button>
        <div class="relative z-10">
            <span class="inline-block bg-white/20 backdrop-blur-sm text-white text-xs font-semibold px-3 py-1 rounded-full mb-2">{{ restaurant.cuisine }}</span>
            <h3 class="text-3xl font-bold leading-tight">{{ restaurant.name }}</h3>
            
            <!-- ATUALIZADO: Div para exibir a razão -->
            <div class="text-sm text-gray-200 mt-2 min-h-[40px] transition-opacity duration-300" :class="reason ? 'opacity-100' : 'opacity-0'">
                <p v-if="!isLoading">{{ reason }}</p>
            </div>

            <div class="mt-4 flex gap-4">
                 <button @click.stop="$emit('requestReservation', restaurant)" class="bg-white text-gray-800 font-bold py-2 px-4 rounded-full text-sm">Reservar Mesa</button>
                 <button @click.stop="getReason" class="bg-transparent border border-white/50 text-white font-bold py-2 px-4 rounded-full text-sm hover:bg-white/10" :disabled="isLoading">
                    <span v-if="!isLoading && !reason">Por que visitar? ✨</span>
                    <span v-if="!isLoading && reason">Esconder dica</span>
                    <span v-if="isLoading">Analisando...</span>
                 </button>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import { callGemini } from '../services/geminiService.js';
const props = defineProps({
  restaurant: { type: Object, required: true },
  isFavorited: { type: Boolean, default: false }
});
defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant']);
const reason = ref('');
const isLoading = ref(false);

async function getReason() {
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