<template>
    <div @click.self="$emit('close')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl p-4">
            <div class="aspect-video bg-gray-200 rounded-lg flex items-center justify-center relative">
                <div v-if="isLoading" class="text-center">
                    <div class="loader-dark mx-auto"></div>
                    <p class="mt-2 text-sm text-gray-600">Gerando a vista da sua mesa...</p>
                </div>
                <img v-if="imageUrl" :src="imageUrl" class="w-full h-full object-cover rounded-lg" alt="Vista da mesa gerada por IA">
                <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
            </div>
            <div class="p-4 text-center">
                <h3 class="text-xl font-bold text-gray-800">Vista da Mesa {{ table.id }}</h3>
                <p class="text-gray-500 text-sm">Esta é uma representação artística gerada por IA.</p>
                <button @click="$emit('close')" class="mt-4 bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-indigo-700 transition-colors">Fechar</button>
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted } from 'vue';
const props = defineProps({
  table: { type: Object, required: true },
  restaurant: { type: Object, required: true }
});
defineEmits(['close']);

const isLoading = ref(true);
const imageUrl = ref(null);
const error = ref(null);

async function generateImageView() {
    // Esta é uma simulação da chamada à API de imagem
    // Em um projeto real, você faria a chamada aqui.
    const prompt = `A beautiful, photorealistic view from a table at a high-end ${props.restaurant.cuisine} restaurant. Table ${props.table.id} is near a window.`;
    console.log("Gerando imagem com o prompt:", prompt);
    
    // Simula o tempo de espera da API
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Usa um placeholder dinâmico para simular a imagem gerada
    imageUrl.value = `https://placehold.co/800x600/6366f1/ffffff?text=Vista+da+Mesa+${props.table.id}`;
    isLoading.value = false;
}

onMounted(generateImageView);
</script>