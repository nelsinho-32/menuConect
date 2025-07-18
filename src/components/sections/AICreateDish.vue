<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">🧑‍🍳 Crie seu Prato com IA</h2>
        <div class="bg-white rounded-2xl p-6 shadow-sm">
            <div class="flex flex-col md:flex-row items-center gap-4">
                <input type="text" v-model="ingredients" placeholder="Digite alguns ingredientes (ex: frango, creme, milho)" class="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-indigo-500 focus:border-indigo-500">
                <button @click="createDish" class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex-shrink-0 w-full md:w-auto" :disabled="isLoading">
                    <span v-if="!isLoading">✨ Criar Prato</span>
                    <span v-else class="flex items-center justify-center"><div class="loader-dark w-5 h-5"></div></span>
                </button>
            </div>
            <div v-if="createdDish || isLoading" class="mt-6">
                <div v-if="isLoading" class="flex items-center justify-center p-6"><div class="loader-dark"></div><p class="ml-4 text-gray-600">Criando sua obra-prima...</p></div>
                <div v-else-if="createdDish" class="border-t pt-4">
                    <h4 class="font-bold text-2xl text-indigo-600">{{ createdDish.dishName }}</h4>
                    <p class="font-semibold text-gray-500 mt-1">por {{ createdDish.restaurantConcept }}</p>
                    <p class="text-gray-700 mt-4">{{ createdDish.description }}</p>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref } from 'vue';
import { callGemini } from '../../services/geminiService';

const ingredients = ref('');
const createdDish = ref(null);
const isLoading = ref(false);

async function createDish() {
    if (!ingredients.value.trim()) {
        alert('Por favor, digite alguns ingredientes.');
        return;
    }
    
    isLoading.value = true;
    createdDish.value = null;

    const schema = { type: "OBJECT", properties: { dishName: { type: "STRING" }, description: { type: "STRING" }, restaurantConcept: { type: "STRING" } } };
    const prompt = `Com base nos ingredientes: '${ingredients.value}', crie um prato. Invente um nome criativo para o prato, uma descrição apetitosa e um nome/conceito de restaurante fictício que o serviria.`;
    const result = await callGemini(prompt, schema);
    
    if (result) {
        createdDish.value = result;
    } else {
        alert("Não foi possível criar um prato. Tente ingredientes diferentes.");
    }

    isLoading.value = false;
}
</script>