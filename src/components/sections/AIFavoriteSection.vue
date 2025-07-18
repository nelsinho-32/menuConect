<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">⚡ Peça seu Favorito com IA</h2>
        <div class="dish-card bg-white p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="text-center md:text-left">
                <h3 class="text-3xl font-bold text-gray-800">Já sabe o que quer?</h3>
                <p class="text-gray-500 mt-1" v-html="favoriteUpsellText"></p>
            </div>
            <button @click="$emit('openPaymentModal', favoriteDish)" :disabled="isLoading" class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed">
                Pedir agora!
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { callGemini } from '../../services/geminiService';

const favoriteDish = { id: 6, restaurantName: "Burger Queen", dishName: "Batata Frita com Cheddar", price: "22.00", imageUrl: "..." };
const favoriteUpsellText = ref('Nossa IA está pensando em uma oferta para você...');
const isLoading = ref(true);
defineEmits(['openPaymentModal']);

async function initializeFavoriteUpsell() {
    const schema = { type: "OBJECT", properties: { message: { type: "STRING" } } };
    const prompt = `Aja como um assistente de IA amigável. O prato favorito de um usuário é '${favoriteDish.dishName}'. Crie uma mensagem curta e convidativa (máximo 20 palavras) sugerindo que ele peça este prato novamente e adicione uma bebida que combine.`;
    const result = await callGemini(prompt, schema);
    favoriteUpsellText.value = (result && result.message) ? result.message : `Vimos que você adora <strong class="brand-text">${favoriteDish.dishName}</strong>. Que tal pedir de novo?`;
    isLoading.value = false;
}

onMounted(initializeFavoriteUpsell);
</script>