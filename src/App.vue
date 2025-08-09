<script setup>
import { ref, reactive, computed, onMounted } from 'vue';
import AppHeader from './components/AppHeader.vue';
import Footer from './components/Footer.vue';

// Vistas
import HomeView from './components/views/HomeView.vue';
import RestaurantsView from './components/views/RestaurantsView.vue';
import DishesView from './components/views/DishesView.vue';
import RestaurantDetailView from './components/RestaurantDetailView.vue';
import ReservationView from './components/ReservationView.vue';
import MyReservationsView from './components/MyReservationsView.vue';
import UserProfileView from './components/UserProfileView.vue';
import CartView from './components/CartView.vue';
import FavoriteRestaurantsView from './components/views/FavoriteRestaurantsView.vue';
import FavoriteDishesView from './components/views/FavoriteDishesView.vue';
import OrderHistoryView from './components/views/OrderHistoryView.vue';

// Modais
import ActionModal from './components/ActionModal.vue';
import PaymentModal from './components/PaymentModal.vue';
import ConfirmationModal from './components/ConfirmationModal.vue';
import DineOptionsModal from './components/DineOptionsModal.vue';
import AddRestaurantModal from './components/AddRestaurantModal.vue';
import AddDishModal from './components/AddDishModal.vue';
import PixModal from './components/PixModal.vue';
import CustomizeDishModal from './components/CustomizeDishModal.vue';
import SelectMenuItemModal from './components/SelectMenuItemModal.vue';

// 1. IMPORTAÇÃO DAS STORES DO PINIA
import { useRestaurantStore } from './stores/restaurantStore';
import { useEncontroStore } from './stores/encontroStore';
import { useUserStore } from './stores/userStore';

// 2. Ativação das stores para usar no componente
const restaurantStore = useRestaurantStore();
const encontroStore = useEncontroStore();
const userStore = useUserStore();

// --- DADOS REATIVOS QUE PERMANECEM NO APP.VUE ---
const cart = reactive([]);
const favoriteDishes = reactive(new Set());
const favoriteRestaurants = reactive(new Set());
const isActionModalOpen = ref(false);
const isPaymentModalOpen = ref(false);
const isPixModalOpen = ref(false);
const isDineOptionsModalOpen = ref(false);
const currentDishForAction = ref(null);
const isToastVisible = ref(false);
const toastMessage = ref('');
const paymentShortcut = ref(null);
const isAddRestaurantModalOpen = ref(false);
const isAddDishModalOpen = ref(false);
const dishModalProps = ref({});
const orderHistory = reactive([]);
const isCustomizeModalOpen = ref(false);
const isSelectMenuItemModalOpen = ref(false);
const menuItemModalProps = ref({});


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
    phone: '+83 99692-1055',
    avatarUrl: 'https://placehold.co/256x256/6366f1/ffffff?text=N',
    preferences: ['Italiana', 'Hamburgueria', 'Japonesa']
});

const isConfirmationModalOpen = ref(false);
const confirmationModalMessage = ref('');

// --- DADOS COMPUTADOS ---
// Estes computados agora usam os dados diretamente do armazém de restaurantes
const cartItemCount = computed(() => cart.reduce((sum, item) => sum + item.quantity, 0));
const trendingDishes = computed(() => restaurantStore.allDishes.slice(0, 4));
const frequentDishes = computed(() => restaurantStore.allDishes.slice(1, 5));
const favoritedRestaurantsList = computed(() => restaurantStore.restaurants.filter(r => favoriteRestaurants.has(r.id)));
const favoritedDishesList = computed(() => restaurantStore.allDishes.filter(d => favoriteDishes.has(d.id)).slice(0, 10));


// --- PERSISTÊNCIA ---
const saveFavoritesToLocalStorage = () => {
    localStorage.setItem('menuConnectFavoriteDishes', JSON.stringify(Array.from(favoriteDishes)));
    localStorage.setItem('menuConnectFavoriteRestaurants', JSON.stringify(Array.from(favoriteRestaurants)));
};

const loadFavoritesFromLocalStorage = () => {
    const savedDishIds = localStorage.getItem('menuConnectFavoriteDishes');
    const savedRestaurantIds = localStorage.getItem('menuConnectFavoriteRestaurants');
    favoriteDishes.clear();
    favoriteRestaurants.clear();
    if (savedDishIds) JSON.parse(savedDishIds).forEach(id => favoriteDishes.add(id));
    if (savedRestaurantIds) JSON.parse(savedRestaurantIds).forEach(id => favoriteRestaurants.add(id));
};

const saveOrderHistoryToLocalStorage = () => {
    localStorage.setItem('menuConnectOrderHistory', JSON.stringify(orderHistory));
};

const loadOrderHistoryFromLocalStorage = () => {
    const savedHistory = localStorage.getItem('menuConnectOrderHistory');
    if (savedHistory) {
        orderHistory.push(...JSON.parse(savedHistory));
    }
};

// Quando a aplicação é montada, carrega tudo a partir das fontes corretas.
onMounted(() => {
    restaurantStore.loadRestaurantsFromLocalStorage();
    loadFavoritesFromLocalStorage();
    loadOrderHistoryFromLocalStorage();
});


// --- MÉTODOS ---
const showToast = (message) => {
    toastMessage.value = message;
    isToastVisible.value = true;
    setTimeout(() => isToastVisible.value = false, 2500);
};

const goToView = (name, data = null) => {
    if (['home', 'restaurants', 'dishes'].includes(viewState.name)) {
        previousViewState.value = viewState.name;
    }
    viewState.name = name;
    viewState.data = data;
    window.scrollTo(0, 0);
};

const goBack = () => goToView(previousViewState.value || 'home');

const handleAddRestaurant = (newRestaurantData) => {
    const added = restaurantStore.addRestaurant(newRestaurantData);
    showToast(`Restaurante '${added.name}' adicionado com sucesso!`);
    closeAddRestaurantModal();
};

const handleAddDish = (newDishData) => {
    const added = restaurantStore.addDish(newDishData);
    if (added) {
        showToast(`Prato '${added.dishName}' adicionado com sucesso!`);
    } else {
        showToast(`Erro: Restaurante não encontrado.`, 'error');
    }
    closeAddDishModal();
};

const handleUpdateMap = (updatedLayout) => {
    if (viewState.data && viewState.data.id) {
        restaurantStore.updateRestaurantMap(viewState.data.id, updatedLayout);
        showToast('Mapa salvo com sucesso!');
    }
};

const addToCart = ({ dish, quantity, customization = null, isPlanned = false }) => {
    const cartItemId = `${dish.id}-${Date.now()}`;
    cart.push({ ...dish, quantity, customization, isPlanned, cartItemId });
    closeCustomizeModal();
    closeActionModal();
    showToast(`${quantity}x '${dish.dishName}' adicionado!`);
};

const handleConfirmEncontro = (encontroData) => {
    if (encontroData.paymentOption === 'agora') {
        encontroData.guests.forEach(guest => {
            Object.values(guest.menu).forEach(itemName => {
                if (itemName) {
                    const dish = restaurantStore.allDishes.find(d => d.name === itemName || d.dishName === itemName);
                    if (dish) {
                        addToCart({ dish, quantity: 1, isPlanned: true });
                    }
                }
            });
        });
        goToView('cart');
    }
    const restaurant = restaurantStore.restaurants.find(r => r.id === encontroData.restaurantId);
    if (restaurant) {
        handleBooking({
            restaurant,
            table: encontroData.selectedTable,
            dateTime: encontroData.dateTime,
            guests: encontroData.guests.length
        });
    }
    encontroStore.cancelPlanning();
};

const openSelectMenuItemModal = (props) => {
    console.log('4. Evento CHEGOU ao App.vue! A abrir a modal com os seguintes dados:', props);
    menuItemModalProps.value = props;
    isSelectMenuItemModalOpen.value = true;
};

const handleMenuItemSelection = (item) => {
    const { guest, category } = menuItemModalProps.value;
    const categoryMap = { 'Entradas': 'starter', 'Prato Principal': 'main', 'Sobremesas': 'dessert', 'Bebidas': 'drink' };
    const menuKey = categoryMap[category];
    if (menuKey) {
        encontroStore.setGuestMenu(guest.id, menuKey, item.name);
    }
    isSelectMenuItemModalOpen.value = false;
};

// Nova função para atualizar a opção de consumo de um grupo de itens
const handleUpdateDineOption = ({ restaurantId, newOption }) => {
    cart.forEach(item => {
        if (item.restaurantId === restaurantId) {
            item.dineOption = newOption;
        }
    });
    const restaurantName = cart.find(item => item.restaurantId === restaurantId)?.restaurantName;
    if (restaurantName) {
        showToast(`Opção de consumo para ${restaurantName} atualizada!`);
    }
};

const removeFromCart = (cartItemId) => {
    const index = cart.findIndex(item => item.cartItemId === cartItemId);
    if (index !== -1) {
        showToast(`'${cart[index].dishName}' removido.`);
        cart.splice(index, 1);
    }
};

const updateQuantity = ({ cartItemId, quantity }) => {
    const item = cart.find(item => item.cartItemId === cartItemId);
    if (item) {
        item.quantity = quantity;
        if (item.quantity <= 0) {
            removeFromCart(cartItemId);
        }
    }
};

const handleUpdateCartItem = ({ dish, quantity, customization }) => {
    const itemIndex = cart.findIndex(item => item.cartItemId === dish.cartItemId);
    if (itemIndex !== -1) {
        const originalDineOption = cart[itemIndex].dineOption;
        cart[itemIndex] = { ...dish, quantity, customization, dineOption: originalDineOption, cartItemId: dish.cartItemId };
        showToast(`Item '${dish.dishName}' atualizado.`);
    }
    closeCustomizeModal();
};


const toggleDishFavorite = (dish) => {
    if (favoriteDishes.has(dish.id)) {
        favoriteDishes.delete(dish.id);
        showToast(`'${dish.dishName}' removido dos favoritos.`);
    } else {
        favoriteDishes.add(dish.id);
        showToast(`'${dish.dishName}' adicionado aos favoritos!`);
    }
    saveFavoritesToLocalStorage();
};

const toggleRestaurantFavorite = (restaurant) => {
    if (favoriteRestaurants.has(restaurant.id)) {
        favoriteRestaurants.delete(restaurant.id);
        showToast(`'${restaurant.name}' removido dos favoritos.`);
    } else {
        favoriteRestaurants.add(restaurant.id);
        showToast(`'${restaurant.name}' adicionado aos favoritos!`);
    }
    saveFavoritesToLocalStorage();
};

const openActionModal = (dish) => {
    if (dish && dish.id) {
        currentDishForAction.value = dish;
        isActionModalOpen.value = true;
    }
};
const closeActionModal = () => isActionModalOpen.value = false;

const openDineOptionsModal = (dish) => {
    currentDishForAction.value = dish;
    isDineOptionsModalOpen.value = true;
};
const closeDineOptionsModal = () => isDineOptionsModalOpen.value = false;

const openCheckout = (shortcut = null) => {
    if (shortcut === 'pix') {
        isPixModalOpen.value = true;
    } else {
        paymentShortcut.value = shortcut;
        isPaymentModalOpen.value = true;
    }
};

const closePixModal = () => isPixModalOpen.value = false;
const closePaymentModal = () => isPaymentModalOpen.value = false;

// função para lidar com o sucesso do pagamento
const handlePaymentSuccess = () => {
    if (cart.length === 0) return;

    // AQUI ESTÁ A CORREÇÃO: Voltamos a guardar uma cópia profunda do carrinho.
    const itemsForHistory = JSON.parse(JSON.stringify(cart));

    const deliveryRestaurants = new Set();
    cart.forEach(item => {
        if (item.dineOption === 'delivery' || !item.dineOption) {
            deliveryRestaurants.add(item.restaurantId);
        }
    });
    const finalDeliveryFee = deliveryRestaurants.size * 5.00;
    const finalSubtotal = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);

    const newOrder = {
        id: Date.now(),
        date: new Date().toISOString(),
        items: itemsForHistory, // Guarda a versão completa dos itens
        total: finalSubtotal + finalDeliveryFee
    };

    orderHistory.push(newOrder);
    saveOrderHistoryToLocalStorage();

    cart.length = 0;
    closePaymentModal();
    closePixModal();
    goToView('home');
    showToast("Pedido realizado com sucesso! Obrigado!");
};


const orderNowFromAction = ({ dish, quantity }) => {
    addToCart({ dish, quantity, dineOption: 'delivery' });
    goToView('cart');
};

const handleDineInOrTakeout = (payload) => {
    addToCart({
        dish: payload.dish,
        quantity: 1,
        dineOption: payload.dineOption
    });
    goToView('cart');
};

const handleGoToReservation = (dish) => {
    const restaurant = restaurantStore.restaurants.find(r => r.name === dish.restaurantName);
    if (restaurant) {
        goToView('reservation', restaurant);
    }
};

const sendWhatsAppConfirmation = (reservationDetails) => {
    const { restaurant, table, dateTime, guests } = reservationDetails;
    let phone = userProfile.phone.replace(/\D/g, '');
    if (phone.length <= 11) phone = '55' + phone;
    const formattedDate = dateTime.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    const formattedTime = dateTime.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });
    const message = `Olá! 👋\n\nSua reserva no *${restaurant.name}* está confirmada!\n\n*Detalhes:*\n- *Mesa:* ${table.id}\n- *Data:* ${formattedDate}\n- *Hora:* ${formattedTime}\n- *Pessoas:* ${guests}\n\nObrigado por usar o Menu Connect!`;
    const whatsappUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
    showToast("Confirmação enviada para o WhatsApp!");
};

const handleBooking = ({ restaurant, table, dateTime, guests }) => {
    userReservations.bookedTable = {
        restaurantId: restaurant.id,
        tableId: table.id,
        restaurantName: restaurant.name,
        restaurantImage: restaurant.imageUrl,
        bookingTime: dateTime,
        guests: guests,
        status: 'confirmed'
    };
    const minutesToBooking = (dateTime.getTime() - new Date().getTime()) / (1000 * 60);
    if (minutesToBooking > 60) {
        confirmationModalMessage.value = "Você receberá uma mensagem no WhatsApp 1 hora antes para confirmar sua reserva. Você terá 20 minutos para responder.";
    } else if (minutesToBooking > 20) {
        confirmationModalMessage.value = "Sua reserva é para breve! Enviaremos uma mensagem de confirmação 15 minutos antes.";
    } else {
        confirmationModalMessage.value = "Sua reserva é para agora! Por favor, dirija-se ao restaurante.";
    }
    isConfirmationModalOpen.value = true;
    setTimeout(() => {
        sendWhatsAppConfirmation({ restaurant, table, dateTime, guests });
    }, 500);
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

const handleConfirmReservation = (reservation) => {
    if (userReservations.bookedTable && userReservations.bookedTable.tableId === reservation.tableId) {
        userReservations.bookedTable.status = 'confirmed';
        showToast(`Reserva para a mesa ${reservation.tableId} confirmada!`);
    }
};
const handleUpdateUser = (updatedData) => {
    Object.assign(userProfile, updatedData);
    showToast('Perfil atualizado com sucesso!');
};
const handleSearchNavigation = (item) => {
    if (item.type === 'restaurant') {
        goToView('restaurantDetail', item);
    } else if (item.type === 'dish') {
        const restaurant = restaurantStore.restaurants.find(r => r.id === item.restaurantId);
        if (restaurant) {
            goToView('restaurantDetail', restaurant);
        }
    }
};
const openAddRestaurantModal = () => isAddRestaurantModalOpen.value = true;
const closeAddRestaurantModal = () => isAddRestaurantModalOpen.value = false;
const openAddDishModal = (props = {}) => {
    dishModalProps.value = props;
    isAddDishModalOpen.value = true;
};
const closeAddDishModal = () => isAddDishModalOpen.value = false;

const openCustomizeModal = (dish) => {
    currentDishForAction.value = dish;
    isActionModalOpen.value = false; // Fecha a modal de ação
    isCustomizeModalOpen.value = true;
};

const closeCustomizeModal = () => {
    isCustomizeModalOpen.value = false;
};



</script>

<template>
    <div>
        <app-header :cart-item-count="cartItemCount" :user="userProfile"
            :searchable-items="restaurantStore.searchableItems" :active-view="viewState.name" @navigate="goToView"
            @search-navigate="handleSearchNavigation" />
        <HomeView v-if="viewState.name === 'home'" :restaurants="restaurantStore.featuredRestaurants"
            :trending-dishes="trendingDishes" :frequent-dishes="frequentDishes" :favorite-dishes="favoriteDishes"
            :favorite-restaurants="favoriteRestaurants" :all-dishes="restaurantStore.allDishes"
            @open-action-modal="openActionModal" @open-dine-options="openDineOptionsModal"
            @toggle-dish-favorite="toggleDishFavorite" @toggle-restaurant-favorite="toggleRestaurantFavorite"
            @request-reservation="restaurant => goToView('reservation', restaurant)"
            @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
            @open-payment-modal="openCheckout" />
        <RestaurantsView v-if="viewState.name === 'restaurants'" :restaurants="restaurantStore.restaurants"
            :favorite-restaurants="favoriteRestaurants" @toggle-favorite="toggleRestaurantFavorite"
            @request-reservation="restaurant => goToView('reservation', restaurant)"
            @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
            @open-add-restaurant-modal="openAddRestaurantModal" />
        <DishesView v-if="viewState.name === 'dishes'" :dishes="restaurantStore.allDishes"
            :favorite-dishes="favoriteDishes" @open-action-modal="openActionModal"
            @open-dine-options="openDineOptionsModal" @toggle-favorite="toggleDishFavorite"
            @open-add-dish-modal="openAddDishModal" />
        <RestaurantDetailView v-if="viewState.name === 'restaurantDetail'" :restaurant="viewState.data"
            @back-to-main="goBack" @open-action-modal="openActionModal" @open-add-dish-modal="openAddDishModal"
            @confirm-encontro="handleConfirmEncontro" @open-menu-item-select-modal="openSelectMenuItemModal" />
        <ReservationView v-if="viewState.name === 'reservation'" :restaurant="viewState.data"
            :user-reservations="userReservations" @back-to-main="goBack" @update-map="handleUpdateMap"
            @book-table="handleBooking" @join-waitlist="handleWaitingList"
            @cancel-reservation="handleCancellation('booked')" />
        <MyReservationsView v-if="viewState.name === 'myReservations'" :reservations="userReservations"
            @cancel-reservation="handleCancellation" @confirm-reservation="handleConfirmReservation"
            @back-to-main="goBack" />
        <UserProfileView v-if="viewState.name === 'userProfile'" :user="userProfile" @update-user="handleUpdateUser"
            @back-to-main="goBack" />
        <CartView v-if="viewState.name === 'cart'" :cart-items="cart" :all-dishes="restaurantStore.allDishes"
            @update-quantity="updateQuantity" @remove-from-cart="removeFromCart" @add-to-cart="addToCart"
            @back-to-main="goBack" @checkout="openCheckout" @edit-item="openCustomizeModal"
            @update-dine-option="handleUpdateDineOption" />
        <FavoriteRestaurantsView v-if="viewState.name === 'favoriteRestaurants'"
            :favorite-restaurants="favoritedRestaurantsList" @toggle-favorite="toggleRestaurantFavorite"
            @request-reservation="restaurant => goToView('reservation', restaurant)"
            @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
            @back-to-main="goToView('home')" />
        <FavoriteDishesView v-if="viewState.name === 'favoriteDishes'" :favorite-dishes="favoritedDishesList"
            @toggle-favorite="toggleDishFavorite" @open-action-modal="openActionModal"
            @open-dine-options="openDineOptionsModal" @back-to-main="goToView('home')" />
        <OrderHistoryView v-if="viewState.name === 'orderHistory'"
            :order-history="orderHistory"
            @back-to-main="goToView('home')" />

        <Footer />

        <AddRestaurantModal v-if="isAddRestaurantModalOpen" @close="closeAddRestaurantModal"
            @add-restaurant="handleAddRestaurant" />
        <AddDishModal v-if="isAddDishModalOpen" :allRestaurants="restaurantStore.restaurants"
            :restaurant="dishModalProps.restaurant" :category="dishModalProps.category" @close="closeAddDishModal"
            @add-dish="handleAddDish" />
        <ActionModal v-if="isActionModalOpen" :dish="currentDishForAction" @close-modal="closeActionModal"
            @add-to-cart="addToCart" @order-now="orderNowFromAction" @open-customize-modal="openCustomizeModal" />
        <CustomizeDishModal v-if="isCustomizeModalOpen" :dish="currentDishForAction" @close="closeCustomizeModal"
            @add-to-cart="addToCart" />
        <DineOptionsModal v-if="isDineOptionsModalOpen" :dish="currentDishForAction"
            @close-modal="closeDineOptionsModal" @dine-in="handleDineInOrTakeout" @takeout="handleDineInOrTakeout"
            @reserve="handleGoToReservation" />
        <PaymentModal v-if="isPaymentModalOpen" :cart="cart" :shortcut="paymentShortcut"
            @close-modal="closePaymentModal" @payment-success="handlePaymentSuccess" />
        <PixModal v-if="isPixModalOpen" :cart="cart" @close="closePixModal" @payment-success="handlePaymentSuccess" />
        <ConfirmationModal v-if="isConfirmationModalOpen" :message="confirmationModalMessage"
            @close="isConfirmationModalOpen = false" />
        <SelectMenuItemModal v-if="isSelectMenuItemModalOpen" :menu-items="menuItemModalProps.menuItems"
            :category="menuItemModalProps.category" @close="isSelectMenuItemModalOpen = false"
            @item-selected="handleMenuItemSelection" />
        <div
            :class="['toast-notification fixed bottom-5 right-5 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg', { 'show': isToastVisible }]">
            {{ toastMessage }}
        </div>
    </div>
</template>