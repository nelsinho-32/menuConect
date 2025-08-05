// src/components/sections/AIEncontroSection.vue (CORRIGIDO)

<template>
    <section class="my-12">
        <h2 class="section-title mb-6">✨ Sugestões para seu Encontro</h2>
        <div v-if="isLoading" class="flex items-center justify-center p-10 bg-white rounded-lg shadow-lg">
            <div class="loader-dark"></div>
            <p class="ml-4 text-gray-600">A criar experiências únicas para você...</p>
        </div>
        <div v-else-if="error" class="p-10 bg-red-50 text-red-700 rounded-lg shadow-lg text-center">
            <p class="font-bold">Oops! Algo deu errado ao gerar as sugestões.</p>
            <p class="text-sm mt-2">{{ error }}</p>
            <button @click="generateSuggestions" class="mt-4 bg-red-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-600">
                Tentar Novamente
            </button>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <EncontroCard 
                v-for="(suggestion, index) in suggestions" 
                :key="index"
                :initial-suggestion="suggestion"
                :restaurant-menu="restaurant.menu"
                :restaurant-theme="restaurant.cuisine"
            />
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { callGemini } from '../../services/geminiService'; 
import EncontroCard from '../EncontroCard.vue';

const props = defineProps({
    restaurant: { type: Object, required: true }
});

const isLoading = ref(true);
const suggestions = ref([]);
const error = ref(null);

async function generateSuggestions() {
    isLoading.value = true;
    error.value = null;
    suggestions.value = [];

    const schema = {
      type: "ARRAY",
      items: {
        type: "OBJECT",
        properties: {
          title: { type: "STRING" },
          table: { type: "STRING" },
          menu: { 
            type: "OBJECT",
            properties: {
              starter: { type: "STRING" },
              main: { type: "STRING" },
              dessert: { type: "STRING" },
              drink: { type: "STRING" }
            }
          },
          tip: { type: "STRING" }
        }
      }
    };
    const prompt = `Aja como um concierge de encontros para o restaurante '${props.restaurant.name}', um local de '${props.restaurant.cuisine}'. Crie exatamente 3 sugestões de "encontros" temáticos. Para cada um, forneça um título criativo, uma sugestão de mesa (ex: "Mesa 5, perto da janela"), um menu completo (entrada, prato principal, sobremesa, bebida) e uma dica especial curta. Baseie as sugestões de pratos e bebidas no cardápio do restaurante: ${JSON.stringify(props.restaurant.menu)}.`;
    
    try {
        const result = await callGemini(prompt, schema);
        if (result && result.length) {
            suggestions.value = result;
        } else {
            throw new Error("A IA não retornou sugestões válidas.");
        }
    } catch (err) {
        // Agora, `err` conterá a mensagem de erro específica da API
        error.value = err.message || "Não foi possível gerar sugestões no momento.";
    } finally {
        isLoading.value = false;
    }
}

onMounted(generateSuggestions);
</script>