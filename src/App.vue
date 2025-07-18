<script setup>
import { ref, reactive, computed } from 'vue';
import AppHeader from './components/AppHeader.vue';
import Footer from './components/Footer.vue';

// Importando as novas telas
import HomeView from './components/views/HomeView.vue';
import RestaurantsView from './components/views/RestaurantsView.vue';
import DishesView from './components/views/DishesView.vue';
import RestaurantDetailView from './components/RestaurantDetailView.vue';
import ReservationView from './components/ReservationView.vue';
import MyReservationsView from './components/MyReservationsView.vue';
import UserProfileView from './components/UserProfileView.vue';
import CartView from './components/CartView.vue';

// Importando componentes de modais
import ActionModal from './components/ActionModal.vue';
import PaymentModal from './components/PaymentModal.vue';
import ConfirmationModal from './components/ConfirmationModal.vue';
import DineOptionsModal from './components/DineOptionsModal.vue';

// Importando imagens para os restaurantes E PRATOS
import TerracoLisboa from '@/assets/images/TerracoLisboa.webp';
import LogoLisboa from '@/assets/images/LogoLisboa.png';
import VistaPrincipalLisboa from '@/assets/images/VistaPrincipalLisboa.jpg';
import TerracoLisboaNoite from '@/assets/images/TerracoLisboaNoite.jpg';
import AcaiteriaImg from '@/assets/images/Acaiteria.jpg';
import BruttaoBurguerBeco from '@/assets/images/BruttaoBurguerBeco.jpg';
import BruttaoLogo from '@/assets/images/BruttaoLogo.png'; 
import BruttaoLocal from '@/assets/images/BruttaoLocal.jpg';
import PratoPrincipalLisboa from '@/assets/images/PratoPrincipalLisboa.webp';
import BurguerBruttao from '@/assets/images/BurguerBruttao.jpg';
import AcaiComMorango from '@/assets/images/AcaiComMorango.webp';
import PaoComRequeijao from '@/assets/images/PaoComRequeijao.jpeg';


// --- DADOS REATIVOS ---
const cart = reactive([]);
const favoriteDishes = reactive(new Set());
const favoriteRestaurants = reactive(new Set()); 
const isActionModalOpen = ref(false);
const isPaymentModalOpen = ref(false);
const isDineOptionsModalOpen = ref(false);
const currentDishForAction = ref(null);
const isToastVisible = ref(false);
const toastMessage = ref('');
const paymentShortcut = ref(null);

const viewState = reactive({
  name: 'home', 
  data: null 
});

const previousViewState = ref('home');

const userReservations = reactive({
  bookedTable: null,
  waitingForTable: null,
});

const userProfile = reactive({
    name: 'Nelsinho',
    email: 'nelsinho@email.com',
    phone: '+351 912 345 678',
    avatarUrl: 'https://placehold.co/256x256/6366f1/ffffff?text=N',
    preferences: ['Italiana', 'Hamburgueria', 'Japonesa']
});

const isConfirmationModalOpen = ref(false);
const confirmationModalMessage = ref('');

// --- DADOS GLOBAIS ---
const restaurants = reactive([
    { 
        id: 1, 
        name: "Terraço Lisboa Bistrô e Café", 
        cuisine: "Bistrô & Café", 
        imageUrl: TerracoLisboa,
        logoUrl: LogoLisboa,
        galleryUrls: [VistaPrincipalLisboa, TerracoLisboaNoite, TerracoLisboa],
        menu: [
            { id: 101, category: 'Entradas', name: 'Bruschetta Clássica', description: 'Pão italiano, tomate fresco, alho e manjericão.', price: 25.00, imageUrl: PratoPrincipalLisboa },
            { id: 201, category: 'Prato Principal', name: 'Spaghetti Carbonara', description: 'Massa italiana com pancetta, ovos e queijo pecorino.', price: 55.00, imageUrl: PratoPrincipalLisboa },
            { id: 301, category: 'Sobremesas', name: 'Tiramisù', description: 'Clássica sobremesa italiana com café e mascarpone.', price: 28.00, imageUrl: PratoPrincipalLisboa },
            { id: 401, category: 'Bebidas', name: 'Vinho Tinto (Taça)', description: 'Seleção do sommelier.', price: 22.00, imageUrl: PratoPrincipalLisboa },
        ]
    },
    { 
        id: 2, 
        name: "Bruttão Burger Bananeiras", 
        cuisine: "Hamburgueria", 
        imageUrl: BruttaoBurguerBeco,
        logoUrl: BruttaoLogo,
        galleryUrls: [BruttaoLocal, BruttaoBurguerBeco],
        menu: [
            { id: 103, category: 'Entradas', name: 'Batata Frita com Cheddar e Bacon', description: 'Porção generosa de batatas crocantes com muito cheddar e bacon.', price: 22.00, imageUrl: BurguerBruttao },
            { id: 204, category: 'Hambúrgueres', name: 'Bruttão Clássico', description: 'Pão brioche, 180g de carne, queijo prato, alface, tomate e molho da casa.', price: 32.00, imageUrl: BurguerBruttao },
            { id: 205, category: 'Hambúrgueres', name: 'Bruttão Duplo Bacon', description: 'Pão brioche, 2x 180g de carne, dobro de queijo e muito bacon.', price: 45.00, imageUrl: BurguerBruttao },
            { id: 303, category: 'Sobremesas', name: 'Milk-shake de Ovomaltine', description: 'Cremoso e irresistível, com 500ml.', price: 20.00, imageUrl: BurguerBruttao },
            { id: 403, category: 'Bebidas', name: 'Refrigerante Lata', description: '350ml.', price: 8.00, imageUrl: BurguerBruttao },
        ]
    },
    { 
        id: 3, 
        name: "Açaiteria", 
        cuisine: "Açaí & Lanches", 
        imageUrl: AcaiteriaImg,
        logoUrl: AcaiteriaImg,
        galleryUrls: [AcaiteriaImg],
        menu: [
           { id: 206, category: 'Açaí', name: 'Copo de Açaí 500ml', description: 'Açaí puro com banana, granola e leite condensado.', price: 25.00, imageUrl: AcaiComMorango },
           { id: 404, category: 'Bebidas', name: 'Suco de Laranja Natural', description: 'Feito na hora, 400ml.', price: 10.00, imageUrl: AcaiComMorango },
        ]
    }
]);

const trendingDishes = computed(() => [
    { id: 204, restaurantName: "Bruttão Burger Bananeiras", dishName: "Bruttão Clássico", price: "32.00", imageUrl: BurguerBruttao },
    { id: 201, restaurantName: "Terraço Lisboa Bistrô e Café", dishName: "Spaghetti Carbonara", price: "55.00", imageUrl: PratoPrincipalLisboa },
    { id: 206, restaurantName: "Açaiteria", dishName: "Copo de Açaí 500ml", price: "25.00", imageUrl: AcaiComMorango }
]);

const frequentDishes = computed(() => [
    { id: 103, restaurantName: "Bruttão Burger Bananeiras", dishName: "Batata Frita com Cheddar e Bacon", price: "22.00", imageUrl: BurguerBruttao },
    { id: 8, restaurantName: "Padaria Pão Quente", dishName: "Pão na Chapa com Requeijão", price: "8.50", imageUrl: PaoComRequeijao },
    { id: 404, restaurantName: "Açaiteria", dishName: "Suco de Laranja Natural", price: "10.00", imageUrl: AcaiComMorango },
]);

// --- DADOS COMPUTADOS ---
const cartItemCount = computed(() => cart.reduce((sum, item) => sum + item.quantity, 0));

const allDishes = computed(() => {
    return restaurants.flatMap(r => r.menu.map(item => ({...item, restaurantName: r.name, restaurantId: r.id})));
});

const searchableItems = computed(() => {
    const items = [];
    restaurants.forEach(r => {
        items.push({ type: 'restaurant', ...r });
        r.menu.forEach(item => {
            items.push({ type: 'dish', ...item, restaurantName: r.name, restaurantId: r.id });
        });
    });
    return items;
});

// --- MÉTODOS ---
const showToast = (message) => {
    toastMessage.value = message;
    isToastVisible.value = true;
    setTimeout(() => isToastVisible.value = false, 2500);
};

const addToCart = ({ dish, quantity }) => {
    const existingItem = cart.find(item => item.id === dish.id);
    if (existingItem) { 
        existingItem.quantity += quantity; 
    } else { 
        cart.push({ ...dish, quantity: quantity }); 
    }
    showToast(`${quantity}x '${dish.dishName}' adicionado!`);
};

const removeFromCart = (dishId) => {
    const index = cart.findIndex(item => item.id === dishId);
    if (index !== -1) {
        showToast(`'${cart[index].dishName}' removido.`);
        cart.splice(index, 1);
    }
};

const updateQuantity = ({ dishId, quantity }) => {
    const item = cart.find(item => item.id === dishId);
    if (item) {
        item.quantity = quantity;
        if (item.quantity <= 0) {
            removeFromCart(dishId);
        }
    }
};

const toggleDishFavorite = (dish) => {
    if (favoriteDishes.has(dish.id)) {
        favoriteDishes.delete(dish.id);
        showToast(`'${dish.dishName}' removido dos favoritos.`);
    } else {
        favoriteDishes.add(dish.id);
        showToast(`'${dish.dishName}' adicionado aos favoritos!`);
    }
};

const toggleRestaurantFavorite = (restaurant) => {
    if (favoriteRestaurants.has(restaurant.id)) {
        favoriteRestaurants.delete(restaurant.id);
        showToast(`'${restaurant.name}' removido dos favoritos.`);
    } else {
        favoriteRestaurants.add(restaurant.id);
        showToast(`'${restaurant.name}' adicionado aos favoritos!`);
    }
};

const openActionModal = (dish) => {
    if (dish && dish.id) {
        currentDishForAction.value = dish;
        isActionModalOpen.value = true;
    } else {
        console.error("openActionModal called with an invalid dish object:", dish);
    }
};
const closeActionModal = () => isActionModalOpen.value = false;

const openDineOptionsModal = (dish) => {
    currentDishForAction.value = dish;
    isDineOptionsModalOpen.value = true;
};
const closeDineOptionsModal = () => isDineOptionsModalOpen.value = false;

const openCheckout = (shortcut = null) => {
    paymentShortcut.value = shortcut;
    isPaymentModalOpen.value = true;
};
const closePaymentModal = () => isPaymentModalOpen.value = false;

const orderNowFromAction = ({ dish, quantity }) => {
    addToCart({ dish, quantity });
    goToView('cart');
};

const goToView = (name, data = null) => {
    if (['home', 'restaurants', 'dishes'].includes(viewState.name)) {
        previousViewState.value = viewState.name;
    }
    viewState.name = name;
    viewState.data = data;
    window.scrollTo(0, 0);
};

const goBack = () => {
    goToView(previousViewState.value || 'home');
};

const handleDineInOrTakeout = (dish) => {
    addToCart({ dish, quantity: 1 });
    goToView('cart');
};

const handleGoToReservation = (dish) => {
    const restaurant = restaurants.find(r => r.name === dish.restaurantName);
    if (restaurant) {
        goToView('reservation', restaurant);
    }
};

const handleBooking = ({ restaurant, table, dateTime }) => {
    userReservations.bookedTable = { 
        restaurantId: restaurant.id, 
        tableId: table.id,
        restaurantName: restaurant.name,
        restaurantImage: restaurant.imageUrl,
        bookingTime: dateTime
    };
    
    showToast(`Mesa ${table.id} em ${restaurant.name} reservada com sucesso!`);
    
    const minutesToBooking = (dateTime.getTime() - new Date().getTime()) / (1000 * 60);
    if (minutesToBooking > 60) {
        confirmationModalMessage.value = "Você receberá uma mensagem no WhatsApp 1 hora antes para confirmar sua reserva. Você terá 20 minutos para responder.";
    } else if (minutesToBooking > 20) {
        confirmationModalMessage.value = "Sua reserva é para breve! Enviaremos uma mensagem de confirmação 15 minutos antes.";
    } else {
        confirmationModalMessage.value = "Sua reserva é para agora! Por favor, dirija-se ao restaurante.";
    }
    isConfirmationModalOpen.value = true;
};

const handleWaitingList = ({ restaurant, table }) => {
    userReservations.waitingForTable = {
        restaurantId: restaurant.id,
        tableId: table.id,
        restaurantName: restaurant.name,
        restaurantImage: restaurant.imageUrl,
        position: 2
    };
    showToast(`Você entrou na fila de espera para a mesa ${table.id} em ${restaurant.name}.`);
};

const handleCancellation = (type) => {
    if (type === 'booked' && userReservations.bookedTable) {
        showToast(`Reserva da mesa ${userReservations.bookedTable.tableId} cancelada.`);
        userReservations.bookedTable = null;
    }
    if (type === 'waiting' && userReservations.waitingForTable) {
        showToast(`Saída da fila de espera da mesa ${userReservations.waitingForTable.tableId}.`);
        userReservations.waitingForTable = null;
    }
};

const handleUpdateUser = (updatedUser) => {
    Object.assign(userProfile, updatedUser);
    showToast('Perfil atualizado com sucesso!');
};

const handleSearchNavigation = (item) => {
    if (item.type === 'restaurant') {
        goToView('restaurantDetail', item);
    } else if (item.type === 'dish') {
        const restaurant = restaurants.find(r => r.id === item.restaurantId);
        if (restaurant) {
            goToView('restaurantDetail', restaurant);
        }
    }
};
</script>

<template>
    <div>
        <app-header
            :cart-item-count="cartItemCount"
            :user="userProfile"
            :searchable-items="searchableItems"
            :active-view="viewState.name"
            @navigate="goToView"
            @search-navigate="handleSearchNavigation"
        />
        <HomeView
            v-if="viewState.name === 'home'"
            :restaurants="restaurants"
            :trending-dishes="trendingDishes"
            :frequent-dishes="frequentDishes"
            :favorite-dishes="favoriteDishes"
            :favorite-restaurants="favoriteRestaurants"
            :all-dishes="allDishes"
            @open-action-modal="openActionModal"
            @open-dine-options="openDineOptionsModal"
            @toggle-dish-favorite="toggleDishFavorite"
            @toggle-restaurant-favorite="toggleRestaurantFavorite"
            @request-reservation="restaurant => goToView('reservation', restaurant)"
            @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
            @open-payment-modal="openCheckout"
        />
        <RestaurantsView
            v-if="viewState.name === 'restaurants'"
            :restaurants="restaurants"
            :favorite-restaurants="favoriteRestaurants"
            @toggle-favorite="toggleRestaurantFavorite"
            @request-reservation="restaurant => goToView('reservation', restaurant)"
            @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
        />
        <DishesView
            v-if="viewState.name === 'dishes'"
            :dishes="allDishes"
            :favorite-dishes="favoriteDishes"
            @open-action-modal="openActionModal"
            @open-dine-options="openDineOptionsModal"
            @toggle-favorite="toggleDishFavorite"
        />
        <ReservationView
            v-if="viewState.name === 'reservation'"
            :restaurant="viewState.data"
            :user-reservations="userReservations"
            @back="goBack"
            @book-table="handleBooking"
            @join-waitlist="handleWaitingList"
            @cancel-reservation="handleCancellation('booked')"
        />
        <RestaurantDetailView
            v-if="viewState.name === 'restaurantDetail'"
            :restaurant="viewState.data"
            @back="goBack"
            @open-action-modal="openActionModal"
        />
        <MyReservationsView
            v-if="viewState.name === 'myReservations'"
            :reservations="userReservations"
            @cancel-reservation="handleCancellation"
            @back="goBack"
        />
        <UserProfileView
            v-if="viewState.name === 'userProfile'"
            :user="userProfile"
            @update-user="handleUpdateUser"
            @back="goBack"
        />
        <CartView
            v-if="viewState.name === 'cart'"
            :cart-items="cart"
            :all-dishes="allDishes"
            @update-quantity="updateQuantity"
            @remove-from-cart="removeFromCart"
            @add-to-cart="addToCart"
            @back="goBack"
            @checkout="openCheckout"
        />
        
        <Footer />
        <ActionModal v-if="isActionModalOpen" :dish="currentDishForAction" @close-modal="closeActionModal" @add-to-cart="addToCart" @order-now="orderNowFromAction" />
        <DineOptionsModal v-if="isDineOptionsModalOpen" :dish="currentDishForAction" @close-modal="closeDineOptionsModal" @dine-in="handleDineInOrTakeout" @takeout="handleDineInOrTakeout" @reserve="handleGoToReservation" />
        <PaymentModal v-if="isPaymentModalOpen" :cart="cart" :shortcut="paymentShortcut" @close-modal="closePaymentModal" />
        <ConfirmationModal v-if="isConfirmationModalOpen" :message="confirmationModalMessage" @close="isConfirmationModalOpen = false" />
        <div :class="['toast-notification fixed bottom-5 right-5 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg', { 'show': isToastVisible }]">
            {{ toastMessage }}
        </div>
    </div>
</template>