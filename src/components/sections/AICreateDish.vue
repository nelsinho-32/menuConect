<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">🧑‍🍳 Encontre seu Prato com IA</h2>
        <div class="bg-white rounded-2xl p-6 shadow-lg">
            <div class="flex flex-col md:flex-row items-center gap-4">
                <input type="text" v-model="ingredients" placeholder="Digite ingredientes (ex: carne, salada, calabresa)" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500">
                <button @click="findDishes" class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex-shrink-0 w-full md:w-auto" :disabled="isLoading">
                    <span v-if="!isLoading">🔍 Encontrar Pratos</span>
                    <span v-else class="flex items-center justify-center"><div class="loader-dark w-5 h-5 border-t-white border-indigo-200"></div></span>
                </button>
            </div>
            <div v-if="isLoading || results.length > 0 || error" class="mt-6 border-t pt-4">
                <div v-if="isLoading" class="flex items-center justify-center p-6"><div class="loader-dark"></div><p class="ml-4 text-gray-600">Procurando as melhores combinações...</p></div>
                <div v-else-if="error" class="p-4 bg-red-50 text-red-700 rounded-lg text-center">
                    <p>{{ error }}</p>
                </div>
                <div v-else-if="results.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <SuggestionCard v-for="(result, index) in results" :key="index" :suggestion="result" />
                </div>
            </div>
        </div>
    </section>
</template>
<script setup>
import { ref } from 'vue';
import { callGemini } from '../../services/geminiService';
import SuggestionCard from '../SuggestionCard.vue';

const props = defineProps({
    allDishes: { type: Array, required: true }
});

const ingredients = ref('');
const results = ref([]);
const isLoading = ref(false);
const error = ref(null);

async function findDishes() {
    if (!ingredients.value.trim()) {
        alert('Por favor, digite alguns ingredientes.');
        return;
    }
    
    isLoading.value = true;
    results.value = [];
    error.value = null;

    const schema = {
        type: "ARRAY",
        items: {
            type: "OBJECT",
            properties: {
                dishName: { type: "STRING" },
                restaurantName: { type: "STRING" },
                reason: { type: "STRING" }
            }
        }
    };
    const prompt = `Aja como um assistente de comida. Um usuário quer pratos que contenham os seguintes ingredientes: '${ingredients.value}'. Analise a lista de pratos disponíveis: ${JSON.stringify(props.allDishes)}. Retorne uma lista de até 3 pratos que melhor correspondem aos ingredientes. Para cada prato, forneça o nome do prato, o nome do restaurante e uma razão curta e convincente pela qual ele corresponde à busca. Se nenhum prato corresponder, retorne um array vazio.`;
    
    const result = await callGemini(prompt, schema);
    
    if (result) {
        if (result.length > 0) {
            results.value = result;
        } else {
            error.value = "Nenhum prato encontrado com esses ingredientes. Tente uma busca diferente!";
        }
    } else {
        error.value = "Não foi possível buscar sugestões no momento. Tente novamente mais tarde.";
    }

    isLoading.value = false;
}
</script>