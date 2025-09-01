<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt;
            Voltar</button>

        <div class="mb-8">
            <div class="h-96 flex gap-2 rounded-2xl overflow-hidden">
                <div class="w-1/3 h-full bg-gray-100 flex items-center justify-center">
                    <img :src="restaurant.logoUrl" alt="Logo do Restaurante"
                        class="max-h-full max-w-full object-contain p-4">
                </div>
                <div class="w-2/3 h-full relative">
                    <transition name="fade" mode="out-in">
                        <img :key="currentImage" :src="currentImage" alt="Vista do restaurante"
                            class="w-full h-full object-cover absolute inset-0">
                    </transition>
                    <div v-if="carouselImages.length > 1">
                        <div class="absolute inset-0 flex justify-between items-center px-4">
                            <button @click="prevImage"
                                class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <polyline points="15 18 9 12 15 6"></polyline>
                                </svg>
                            </button>
                            <button @click="nextImage"
                                class="bg-black/40 text-white p-2 rounded-full hover:bg-black/60 transition-colors">
                                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"
                                    fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                                    stroke-linejoin="round">
                                    <polyline points="9 18 15 12 9 6"></polyline>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
            <h1 class="text-4xl md:text-5xl font-extrabold mt-6">{{ restaurant.name }}</h1>
            <button @click="$emit('viewRoute', restaurant)"
                class="mt-6 bg-blue-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-600">
                Ver Rota
            </button>
            <section v-if="restaurant.promotions && restaurant.promotions.length > 0" class="my-12">
    <h2 class="section-title mb-6">🎉 Ofertas Especiais Ativas</h2>
    <div class="space-y-4">
        <div v-for="promo in restaurant.promotions" :key="promo.id" class="bg-indigo-50 border-l-4 border-indigo-500 p-4 rounded-r-lg shadow-sm">
            <div class="flex justify-between items-start">
                <div>
                    <h3 class="font-bold text-indigo-800 text-lg">{{ promo.title }}</h3>
                    <p class="text-indigo-700 text-sm mt-1">{{ promo.description }}</p>
                </div>
                <p class="text-xl font-extrabold text-green-600 flex-shrink-0 ml-4">{{ formatDiscount(promo) }}</p>
            </div>
        </div>
    </div>
</section>
        </div>

        <AIEncontroSection :restaurant="restaurant" :user-profile="userProfile" :all-users="allUsers"
            @confirm-encontro="payload => $emit('confirmEncontro', payload)"
            @open-menu-item-select-modal="payload => $emit('openMenuItemSelectModal', payload)"
            @open-customize-modal="payload => $emit('openCustomizeModal', payload)"
            @open-table-select-modal="payload => $emit('openTableSelectModal', payload)" />

        <RestaurantMenu :menu="restaurant.menu" :restaurant-id="restaurant.id"
            @open-action-modal="dish => $emit('openActionModal', dish)"
            @open-add-menu-item-modal="category => $emit('openAddDishModal', { restaurant, category })"
            @delete-dish="dish => $emit('deleteDish', dish)"
            @toggle-availability="item => $emit('toggleAvailability', item)" 
        />
        <section class="my-12">
    <div class="flex justify-between items-center mb-6">
        <h2 class="section-title">Avaliações ({{ restaurant.review_count || 0 }})</h2>
        <button @click="$emit('openAddReviewModal', restaurant)" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
            Deixar uma Avaliação
        </button>
    </div>
    <div class="bg-white p-6 rounded-lg shadow-lg">
        
        <div v-if="restaurant.review_count > 0" class="flex items-center gap-2 mb-4 border-b pb-4">
            <span class="text-4xl font-extrabold text-gray-800">{{ restaurant.average_rating.toFixed(1).replace('.', ',') }}</span>
            <div class="flex items-center text-2xl" :title="`${restaurant.average_rating.toFixed(2)} de 5 estrelas`">
                 <span v-for="n in 5" :key="n" :class="n <= Math.round(restaurant.average_rating) ? 'text-yellow-400' : 'text-gray-300'">★</span>
            </div>
            <span class="text-gray-500 ml-2">de {{ restaurant.review_count }} avaliações</span>
        </div>
        
        <div v-if="restaurantStore.reviews.length > 0">
            <ReviewCard v-for="review in restaurantStore.reviews" :key="review.id" :review="review" />
        </div>
        <div v-else class="text-center text-gray-500 py-8">
            <p>{{ restaurant.review_count > 0 ? 'A carregar avaliações...' : 'Este restaurante ainda não tem avaliações. Seja o primeiro!' }}</p>
        </div>
    </div>
</section>

    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import AIEncontroSection from './sections/AIEncontroSection.vue';
import RestaurantMenu from './RestaurantMenu.vue';
import ReviewCard from  './ReviewCard.vue';
import { useRestaurantStore } from '@/stores/restaurantStore';

const restaurantStore = useRestaurantStore();

const props = defineProps({
    restaurant: { type: Object, required: true },
    userProfile: { type: Object, required: true },
    allUsers: { type: Array, required: true },
});

// ADICIONE 'toggleAvailability' À LISTA DE EVENTOS
defineEmits([
    'backToMain', 
    'openActionModal', 
    'openAddDishModal', 
    'confirmEncontro', 
    'openMenuItemSelectModal', 
    'openCustomizeModal', 
    'openTableSelectModal', 
    'viewRoute', 
    'deleteDish',
    'openAddReviewModal',
    'toggleAvailability'
]);

const formatDiscount = (promo) => {
    if (promo.discount_type === 'percentage') {
        return `${Math.round(promo.discount_value)}% OFF`;
    }
    return `R$ ${parseFloat(promo.discount_value).toFixed(2).replace('.', ',')} OFF`;
};

const carouselImages = ref([]);
const currentImageIndex = ref(0);
const currentImage = computed(() => carouselImages.value[currentImageIndex.value]);


const setupCarousel = () => {
    if (props.restaurant) {
        // Garante que a imagem principal está sempre primeiro e evita duplicados
        const images = new Set([props.restaurant.imageUrl, ...(props.restaurant.galleryUrls || [])]);
        carouselImages.value = Array.from(images);
        currentImageIndex.value = 0;
    }
};

const nextImage = () => {
    currentImageIndex.value = (currentImageIndex.value + 1) % carouselImages.value.length;
};
const prevImage = () => {
    currentImageIndex.value = (currentImageIndex.value - 1 + carouselImages.value.length) % carouselImages.value.length;
};

onMounted(() => {
    setupCarousel();
    if(props.restaurant?.id) {
        restaurantStore.fetchReviewsForRestaurant(props.restaurant.id);
    }
});

watch(() => props.restaurant, (newRestaurant) => {
    if (newRestaurant?.id) {
        restaurantStore.fetchReviewsForRestaurant(newRestaurant.id);
    }
});

onMounted(setupCarousel);
// Garante que o carrossel é atualizado se o restaurante mudar
watch(() => props.restaurant, setupCarousel);

</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}
</style>