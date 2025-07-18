<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import AppHeader from './components/AppHeader.vue';
import DishCard from './components/DishCard.vue';
import RestaurantCard from './components/RestaurantCard.vue';
import CartSidebar from './components/CartSidebar.vue';
import ActionModal from './components/ActionModal.vue';
import PaymentModal from './components/PaymentModal.vue';
import { callGemini } from './services/geminiService.js';

// --- DADOS REATIVOS ---
const trendingDishes = reactive([
    { id: 1, restaurantName: "Cantina da Nona", dishName: "Lasanha à Bolonhesa", price: "45.50", imageUrl: "https://placehold.co/600x400/f87171/ffffff?text=Lasanha" },
    { id: 2, restaurantName: "Sushi House", dishName: "Combinado Salmão (20pç)", price: "79.90", imageUrl: "https://placehold.co/600x400/60a5fa/ffffff?text=Sushi" },
    { id: 3, restaurantName: "Burger Queen", dishName: "X-Tudo Monstro", price: "38.00", imageUrl: "https://placehold.co/600x400/fbbf24/ffffff?text=Hamb%C3%BArguer" }
]);
const frequentDishes = reactive([
    { id: 6, restaurantName: "Burger Queen", dishName: "Batata Frita com Cheddar", price: "22.00", imageUrl: "https://placehold.co/600x400/fca5a5/ffffff?text=Batata+Frita" },
    { id: 7, restaurantName: "Açaí Power", dishName: "Copo de Açaí 500ml", price: "25.00", imageUrl: "https://placehold.co/600x400/c084fc/ffffff?text=A%C3%A7a%C3%AD" },
    { id: 8, restaurantName: "Padaria Pão Quente", dishName: "Pão na Chapa com Requeijão", price: "8.50", imageUrl: "https://placehold.co/600x400/fdba74/ffffff?text=P%C3%A3o" }
]);
const restaurants = reactive([
    { id: 1, name: "La Trattoria", cuisine: "Italiana", imageUrl: "https://placehold.co/800x600/ef4444/ffffff?text=Restaurante+Italiano" },
    { id: 2, name: "Mar Aberto", cuisine: "Frutos do Mar", imageUrl: "https://placehold.co/800x600/3b82f6/ffffff?text=Frutos+do+Mar" },
    { id: 3, name: "Pampa Grill", cuisine: "Churrascaria", imageUrl: "https://placehold.co/800x600/f97316/ffffff?text=Churrascaria" }
]);
const cart = reactive([]);
const isCartOpen = ref(false);
const isActionModalOpen = ref(false);
const isPaymentModalOpen = ref(false);
const currentDishForAction = ref(null);
const currentDishForPayment = ref(null);
const isToastVisible = ref(false);
const toastMessage = ref('');
const favoriteUpsellText = ref('Nossa IA está pensando em uma oferta para você...');

// --- DADOS COMPUTADOS ---
const cartItemCount = computed(() => cart.reduce((sum, item) => sum + item.quantity, 0));

// --- MÉTODOS ---
const toggleCart = (state) => isCartOpen.value = state;

const showToast = (message) => {
    toastMessage.value = message;
    isToastVisible.value = true;
    setTimeout(() => isToastVisible.value = false, 2500);
};

const addToCart = (dish) => {
    const existingItem = cart.find(item => item.id === dish.id);
    if (existingItem) {
        existingItem.quantity++;
    } else {
        cart.push({ ...dish, quantity: 1 });
    }
    showToast(`'${dish.dishName}' adicionado!`);
};

const openActionModal = (dish) => {
    currentDishForAction.value = dish;
    isActionModalOpen.value = true;
};
const closeActionModal = () => isActionModalOpen.value = false;

const openPaymentModal = (dish) => {
    currentDishForPayment.value = dish;
    isPaymentModalOpen.value = true;
};
const closePaymentModal = () => isPaymentModalOpen.value = false;

const orderNowFromAction = (dish) => {
    closeActionModal();
    openPaymentModal(dish);
};

async function initializeFavoriteUpsell() {
    const dish = frequentDishes[0];
    if (!dish) return;
    const schema = { type: "OBJECT", properties: { message: { type: "STRING" } } };
    const prompt = `Aja como um assistente de IA amigável. O prato favorito de um usuário é '${dish.dishName}'. Crie uma mensagem curta e convidativa (máximo 20 palavras) sugerindo que ele peça este prato novamente e adicione uma bebida que combine.`;
    const result = await callGemini(prompt, schema);
    favoriteUpsellText.value = (result && result.message) ? result.message : `Vimos que você adora <strong class="brand-text">${dish.dishName}</strong>. Que tal pedir de novo?`;
}

onMounted(() => {
    initializeFavoriteUpsell();
});
</script>

<template>
  <div>
    <app-header :cart-item-count="cartItemCount" @toggle-cart="toggleCart" />

    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <section id="trending" class="mb-12">
            <h2 class="section-title mb-6">🔥 Em Alta</h2>
            <div class="horizontal-scroll-container">
                <dish-card v-for="dish in trendingDishes" :key="dish.id" :dish="dish" @open-action-modal="openActionModal" />
            </div>
        </section>
        
        <section id="discover-restaurants" class="mb-12">
            <h2 class="section-title mb-6">📍 Descubra Novos Lugares</h2>
            <div class="horizontal-scroll-container">
                <restaurant-card v-for="rest in restaurants" :key="rest.id" :restaurant="rest" />
            </div>
        </section>

        <section id="frequent-orders" class="mb-12">
            <h2 class="section-title mb-6">⭐ Meus Pedidos Frequentes</h2>
            <div class="horizontal-scroll-container">
                 <dish-card v-for="dish in frequentDishes" :key="dish.id" :dish="dish" @open-action-modal="openActionModal" />
            </div>
        </section>

         <section id="ai-favorite" class="mb-12">
            <h2 class="section-title mb-6">⚡ Peça seu Favorito com IA</h2>
            <div class="dish-card bg-white p-8 flex flex-col md:flex-row items-center justify-between gap-6">
                <div class="text-center md:text-left">
                    <h3 class="text-3xl font-bold text-gray-800">Já sabe o que quer?</h3>
                    <p class="text-gray-500 mt-1" v-html="favoriteUpsellText"></p>
                </div>
                <button @click="openPaymentModal(frequentDishes[0])" :disabled="!favoriteUpsellText.includes('Vimos')" class="bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors flex-shrink-0 disabled:opacity-50 disabled:cursor-not-allowed">Pedir agora!</button>
            </div>
        </section>
    </main>
    
    <footer class="text-center py-8 text-gray-500">
        <p>&copy; 2024 Menu Connect. Feito com ❤️ para você.</p>
    </footer>

    <cart-sidebar :cart="cart" :is-open="isCartOpen" @toggle-cart="toggleCart" />
    <action-modal v-if="isActionModalOpen" :dish="currentDishForAction" @close-modal="closeActionModal" @add-to-cart="addToCart" @order-now="orderNowFromAction" />
    <payment-modal v-if="isPaymentModalOpen" :dish="currentDishForPayment" @close-modal="closePaymentModal" />

    <div :class="['toast-notification fixed bottom-5 right-5 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg', { 'show': isToastVisible }]">
        {{ toastMessage }}
    </div>
    </div>
</template>