<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar</button>

        <!-- Hero Section com Galeria -->
        <div class="mb-8">
            <div class="h-96 flex gap-2 rounded-2xl overflow-hidden">
                <div class="w-1/3 h-full bg-gray-100 flex items-center justify-center">
                    <img :src="restaurant.logoUrl" alt="Logo do Restaurante" class="max-h-full max-w-full object-contain p-4">
                </div>
                <div class="w-2/3 h-full relative">
                    <transition name="fade" mode="out-in">
                        <img :key="currentImage" :src="currentImage" alt="Vista do restaurante" class="w-full h-full object-cover absolute inset-0">
                    </transition>
                    <div v-if="carouselImages.length > 1">
                        <div class="absolute inset-0 flex justify-between items-center px-4">
                            <button @click="prevImage" class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"></polyline></svg>
                            </button>
                            <button @click="nextImage" class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"></polyline></svg>
                            </button>
                        </div>
                        <div class="absolute bottom-4 left-0 right-0 flex justify-center gap-2">
                            <button v-for="(image, index) in carouselImages" :key="index" @click="currentImageIndex = index"
                                    :class="['w-3 h-3 rounded-full', currentImageIndex === index ? 'bg-white' : 'bg-white/50']">
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold mt-6">{{ restaurant.name }}</h1>
        </div>

        <AIEncontroSection :restaurant="restaurant" />

        <RestaurantMenu :menu="restaurant.menu" @open-action-modal="dish => $emit('openActionModal', dish)" />

    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import AIEncontroSection from  './sections/AIEncontroSection.vue';
import RestaurantMenu from './RestaurantMenu.vue';

const props = defineProps({
    restaurant: { type: Object, required: true }
});
defineEmits(['backToMain', 'openActionModal']);

const carouselImages = ref([]);
const currentImageIndex = ref(0);
const currentImage = computed(() => carouselImages.value[currentImageIndex.value]);

const nextImage = () => {
    currentImageIndex.value = (currentImageIndex.value + 1) % carouselImages.value.length;
};
const prevImage = () => {
    currentImageIndex.value = (currentImageIndex.value - 1 + carouselImages.value.length) % carouselImages.value.length;
};

onMounted(() => {
    if (props.restaurant && props.restaurant.galleryUrls) {
        carouselImages.value = [props.restaurant.imageUrl, ...props.restaurant.galleryUrls];
    } else {
        carouselImages.value = [props.restaurant.imageUrl];
    }
});
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>