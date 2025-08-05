<template>
    <section class="mb-12">
        <h2 class="section-title mb-6">⚡ Peça seu Favorito com IA</h2>
        <div class="dish-card bg-white p-8 flex flex-col md:flex-row items-center justify-between gap-6">
            <div class="text-center md:text-left">
                <h3 class="text-3xl font-bold text-gray-800">Já sabe o que quer?</h3>
                <p class="text-gray-500 mt-1 min-h-[24px]" v-html="favoriteUpsellText"></p>
                </div>
            <button @click="$emit('openPaymentModal', favoriteDish)" :disabled="isLoading || hasError" class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed">
                Pedir agora!
            </button>
        </div>
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { callGemini } from '../../services/geminiService';

const favoriteDish = { id: 6, restaurantName: "Burger Queen", dishName: "Batata Frita com Cheddar", price: "22.00", imageUrl: "..." };
const favoriteUpsellText = ref('A nossa IA está a pensar numa oferta para você...');
const isLoading = ref(true);
const hasError = ref(false); // INÍCIO: Novo estado para controlar o erro
defineEmits(['openPaymentModal']);

async function initializeFavoriteUpsell() {
    isLoading.value = true;
    hasError.value = false;

    const schema = { type: "OBJECT", properties: { message: { type: "STRING" } } };
    const prompt = `Aja como um assistente de IA amigável. O prato favorito de um usuário é '${favoriteDish.dishName}'. Crie uma mensagem curta e convidativa (máximo 20 palavras) sugerindo que ele peça este prato novamente e adicione uma bebida que combine.`;

    // INÍCIO: Bloco try...catch para tratar o erro
    try {
        const result = await callGemini(prompt, schema);
        if (result && result.message) {
            favoriteUpsellText.value = result.message;
        } else {
            // Se a API não retornar uma mensagem (ou estiver desativada), usa um texto padrão.
            favoriteUpsellText.value = `Vimos que você adora <strong class="brand-text">${favoriteDish.dishName}</strong>. Que tal pedir de novo?`;
        }
    } catch (error) {
        console.warn('A funcionalidade de sugestão com IA está desativada:', error);
        favoriteUpsellText.value = 'A sugestão com IA está temporariamente indisponível.';
        hasError.value = true; // Marca que houve um erro
    } finally {
        isLoading.value = false;
    }
    // FIM: Bloco try...catch para tratar o erro
}

onMounted(initializeFavoriteUpsell);
</script>