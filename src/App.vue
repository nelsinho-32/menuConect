<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import AppHeader from './components/AppHeader.vue';
import CartSidebar from './components/CartSidebar.vue';
import ActionModal from './components/ActionModal.vue';
import PaymentModal from './components/PaymentModal.vue';
import Footer from './components/Footer.vue';

// Importando os novos componentes de seção
import TrendingSection from './components/sections/TrendingSection.vue';
import DiscoverSection from './components/sections/DiscoverSection.vue';
import FrequentOrdersSection from './components/sections/FrequentOrdersSection.vue';
import AIFavoriteSection from './components/sections/AIFavoriteSection.vue';
import AICreateDish from './components/sections/AICreateDish.vue';


// --- DADOS REATIVOS ---
const cart = reactive([]);
const favoriteDishes = reactive(new Set()); // Usando um Set para IDs únicos de favoritos
const isCartOpen = ref(false);
const isActionModalOpen = ref(false);
const isPaymentModalOpen = ref(false);
const currentDishForAction = ref(null);
const currentDishForPayment = ref(null);
const isToastVisible = ref(false);
const toastMessage = ref('');

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

const toggleFavorite = (dish) => {
  if (favoriteDishes.has(dish.id)) {
    favoriteDishes.delete(dish.id);
    showToast(`'${dish.dishName}' removido dos favoritos.`);
  } else {
    favoriteDishes.add(dish.id);
    showToast(`'${dish.dishName}' adicionado aos favoritos!`);
  }
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
</script>

<template>
  <div>
    <app-header :cart-item-count="cartItemCount" @toggle-cart="toggleCart" />

    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">

      <FrequentOrdersSection :favorite-dishes="favoriteDishes" @open-action-modal="openActionModal"
        @toggle-favorite="toggleFavorite" />

      <TrendingSection :favorite-dishes="favoriteDishes" @open-action-modal="openActionModal"
        @toggle-favorite="toggleFavorite" />

      <DiscoverSection />

      <AIFavoriteSection @open-payment-modal="openPaymentModal" />

      <AICreateDish />

    </main>

    <Footer />

    <CartSidebar :cart="cart" :is-open="isCartOpen" @toggle-cart="toggleCart" />
    <ActionModal v-if="isActionModalOpen" :dish="currentDishForAction" @close-modal="closeActionModal"
      @add-to-cart="addToCart" @order-now="orderNowFromAction" />
    <PaymentModal v-if="isPaymentModalOpen" :dish="currentDishForPayment" @close-modal="closePaymentModal" />

    <div
      :class="['toast-notification fixed bottom-5 right-5 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg', { 'show': isToastVisible }]">
      {{ toastMessage }}
    </div>
  </div>
</template>