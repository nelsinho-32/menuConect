<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-2xl w-full shadow-2xl relative">
            <button @click="$emit('close')" class="absolute -top-4 -right-4 bg-white rounded-full p-1 text-gray-700 hover:text-red-500 z-10">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <div v-if="images && images.length" class="aspect-video relative overflow-hidden rounded-t-2xl">
                <transition name="fade" mode="out-in">
                    <img :key="currentImage" :src="currentImage" :alt="`Vista da mesa ${tableId}`" class="w-full h-full object-cover">
                </transition>

                <template v-if="images.length > 1">
                    <div class="absolute inset-0 flex justify-between items-center px-4">
                        <button @click.stop="prevImage" class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
                        </button>
                        <button @click.stop="nextImage" class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
                        </button>
                    </div>
                </template>
            </div>
             <div v-else class="aspect-video flex items-center justify-center bg-gray-100 rounded-t-2xl">
                <p class="text-gray-500">Nenhuma imagem disponível para esta mesa.</p>
            </div>

            <div class="p-6 text-center">
                <h3 class="text-2xl font-bold text-gray-800">Vista da Mesa {{ tableId }}</h3>
                <p class="text-gray-500 text-sm">Esta é a vista real a partir da mesa selecionada.</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  tableId: { type: [String, Number], required: true },
  images: { type: Array, default: () => [] }
});

defineEmits(['close']);

const currentImageIndex = ref(0);
const currentImage = computed(() => props.images[currentImageIndex.value]);

const nextImage = () => {
    currentImageIndex.value = (currentImageIndex.value + 1) % props.images.length;
};
const prevImage = () => {
    currentImageIndex.value = (currentImageIndex.value - 1 + props.images.length) % props.images.length;
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>