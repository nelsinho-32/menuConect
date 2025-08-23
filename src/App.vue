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
// import TableManagementView from './components/views/TableManagementView.vue';
import ReservationSharedView from './components/views/ReservationSharedView.vue';
import RouteView from './components/views/RouteView.vue';
// import DashboardView from './components/views/DashboardView.vue';
import LoginView from './components/views/LoginView.vue';
import RegisterView from './components/views/RegisterView.vue';
import ManagementView from './components/views/ManagementView.vue';

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
import TableDetailModal from './components/TableDetailModal.vue';
import ChatModal from './components/ChatModal.vue';
import MenuModal from './components/MenuModal.vue';
import StartSessionModal from './components/StartSessionModal.vue';
import SessionControlModal from './components/SessionControlModal.vue';
import AddOrderToSessionModal from './components/AddOrderToSessionModal.vue';
import FinishSessionModal from './components/FinishSessionModal.vue';
import DeleteConfirmationModal from './components/DeleteConfirmationModal.vue';
import ReservationDetailModal from './components/ReservationDetailModal.vue';

// 1. IMPORTAÇÃO DAS STORES DO PINIA
import { useRestaurantStore } from './stores/restaurantStore';
import { useEncontroStore } from './stores/encontroStore';
import { useUserStore } from './stores/userStore';
import { useChatStore } from './stores/chatStore';
import { useAuthStore } from './stores/authStore';
import { useUserDataStore } from './stores/userDataStore';
import { useReservationStore } from './stores/reservationStore';
import { useOrderStore } from './stores/orderStore'
import { useManagementStore } from './stores/managementStore';
import { useSessionStore } from './stores/sessionStore';

// 2. Ativação das stores para usar no componente
const restaurantStore = useRestaurantStore();
const encontroStore = useEncontroStore();
const chatStore = useChatStore();
const userStore = useUserStore();
const authStore = useAuthStore();
const userDataStore = useUserDataStore();
const reservationStore = useReservationStore();
const orderStore = useOrderStore();
const managementStore = useManagementStore();
const sessionStore = useSessionStore();

// --- ESTADO REATIVO (EXISTENTE) ---
const cart = reactive([]);
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
const isTableDetailModalOpen = ref(false);
const currentTableForDetail = ref(null);
const isNotificationsOpen = ref(false);
const isFriendsChatOpen = ref(false);
const isMenuModalOpen = ref(false);
const currentRestaurantForMenu = ref(null);
const isConfirmationModalOpen = ref(false);
const confirmationModalMessage = ref('');
const isStartSessionModalOpen = ref(false);
const isSessionControlModalOpen = ref(false);
const tableToManage = ref(null);
const restaurantForModal = ref(null);
const sessionToUpdateId = ref(null);
const isAddOrderToSessionModalOpen = ref(false);
const sessionForModal = ref(null);
const itemToCustomize = ref(null);
const addOrderModalRef = ref(null);
const isFinishSessionModalOpen = ref(false);
const consumptionForModal = ref([]);
const isDeleteModalOpen = ref(false);
const dishToDelete = ref(null);
const isReservationDetailModalOpen = ref(false);
const reservationForDetailModal = ref(null);
// Dados mockados que serão substituídos por dados reais da API
const allUsers = reactive([]);
const notifications = reactive([]);
const friends = reactive([]);


// O estado inicial da vista agora é 'login' se o usuário não estiver autenticado
const viewState = reactive({
    name: authStore.isAuthenticated ? 'home' : 'login',
    data: null
});

const previousViewState = ref('home');


// --- DADOS DO USUÁRIO ---
// O perfil do usuário agora vem da authStore
const userProfile = computed(() => authStore.currentUser || {
    name: 'Visitante',
    email: '',
    avatarUrl: 'https://placehold.co/256x256/cccccc/ffffff?text=?'
});

// --- DADOS COMPUTADOS ---
// Estes computados agora usam os dados diretamente do armazém de restaurantes
const cartItemCount = computed(() => cart.reduce((sum, item) => sum + item.quantity, 0));
const trendingDishes = computed(() => restaurantStore.allDishes.slice(0, 4));
const frequentDishes = computed(() => restaurantStore.allDishes.slice(1, 5));
const favoritedRestaurantsList = computed(() => {
    return restaurantStore.restaurants.filter(r => userDataStore.favoriteRestaurantIds.has(r.id));
});
const favoritedDishesList = computed(() => {
    return restaurantStore.allDishes.filter(d => userDataStore.favoriteDishIds.has(d.id));
});
const newlyAddedRestaurants = computed(() => {
    return restaurantStore.restaurants.filter(r => r.isNew).slice(0, 6);
});



// --- PERSISTÊNCIA ---

const saveOrderHistoryToLocalStorage = () => {
    localStorage.setItem('menuConnectOrderHistory', JSON.stringify(orderHistory));
};

const loadOrderHistoryFromLocalStorage = () => {
    const savedHistory = localStorage.getItem('menuConnectOrderHistory');
    if (savedHistory) {
        orderHistory.push(...JSON.parse(savedHistory));
    }
};

const saveUserProfileToLocalStorage = () => {
    localStorage.setItem('menuConnectUserProfile', JSON.stringify(userProfile));
};

const loadUserProfileFromLocalStorage = () => {
    const savedProfile = localStorage.getItem('menuConnectUserProfile');
    if (savedProfile) {
        Object.assign(userProfile, JSON.parse(savedProfile));
    }
};

// --- FUNÇÃO "MAESTRO" ---
/**
 * Carrega todos os dados iniciais necessários para um usuário autenticado.
 * Esta função só deve ser chamada DEPOIS que o login for confirmado.
 */
const loadInitialUserData = async () => {
    try {
        await restaurantStore.fetchRestaurantsFromAPI();

        await Promise.all([
            userDataStore.fetchAllUserData(),
            reservationStore.fetchAllUserReservations(),
            orderStore.fetchHistory() // <-- ADICIONE ESTA LINHA
        ]);
    } catch (error) {
        console.error("Ocorreu um erro ao carregar os dados iniciais:", error);
        showToast("Não foi possível carregar os seus dados.", "error");
    }
};

// Hook onMounted é executado quando a aplicação arranca
onMounted(() => {
    // 1. Tenta fazer o auto-login a partir do localStorage.
    authStore.tryAutoLogin();

    // 2. Se o auto-login funcionou (o token existe), carrega os dados do usuário.
    if (authStore.isAuthenticated) {
        loadInitialUserData();
    }
});

// Quando a aplicação é montada, carrega tudo a partir das fontes corretas.
onMounted(() => {
    if (authStore.isAuthenticated) {
        restaurantStore.fetchRestaurantsFromAPI();
        userDataStore.fetchAllUserData();
        reservationStore.fetchAllUserReservations();
    }
    restaurantStore.fetchRestaurantsFromAPI();
    loadOrderHistoryFromLocalStorage();
    loadUserProfileFromLocalStorage();
    userDataStore.fetchAllUserData();
});

onMounted(async () => {
    // 1. Primeiro, tenta fazer o auto-login a partir do localStorage.
    authStore.tryAutoLogin();

    // 2. SÓ SE o usuário estiver autenticado, busca todos os outros dados.
    if (authStore.isAuthenticated) {
        // O 'await' garante que a lista de restaurantes carrega primeiro.
        await restaurantStore.fetchRestaurantsFromAPI();

        // Agora que temos os restaurantes, podemos buscar os dados do usuário em paralelo.
        await Promise.all([
            userDataStore.fetchAllUserData(),
            reservationStore.fetchAllUserReservations()
        ]);
    }
});


// --- MÉTODOS ---
const showToast = (message, type = 'success') => {
    toastMessage.value = message;
    isToastVisible.value = true;
    // Adicionar classe de cor baseada no tipo (opcional, requer CSS)
    setTimeout(() => isToastVisible.value = false, 3000);
};

const goToView = (name, data = null) => {
    if (['home', 'restaurants', 'dishes', 'login', 'register'].includes(viewState.name)) {
        previousViewState.value = viewState.name;
    }
    viewState.name = name;
    viewState.data = data;
    window.scrollTo(0, 0);
};

const handleRegister = async (credentials) => {
    try {
        await authStore.register(credentials);
        showToast('Registo bem-sucedido! Por favor, faça login.');
        goToView('login');
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const onCustomizeSessionItem = (item) => {
    itemToCustomize.value = item;
    isCustomizeModalOpen.value = true;
};

const handleLogin = async (credentials) => {
    try {
        await authStore.login(credentials);
        userStore.setUserRole(authStore.currentUser.role);
        showToast(`Bem-vindo de volta, ${authStore.currentUser.name}!`);
        await restaurantStore.fetchRestaurantsFromAPI();
        await loadInitialUserData();
        // Agora podemos buscar os dados específicos do usuário com segurança
        userDataStore.fetchAllUserData();
        reservationStore.fetchAllUserReservations();
        goToView('home');
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const handleChangeTableStatus = async (newStatus) => {
    if (!tableToManage.value || !restaurantForModal.value) return;

    try {
        const validStatuses = ["available", "occupied", "reserved", "cleaning"]; // Adicione "cleaning" se for válido
        if (!validStatuses.includes(newStatus)) {
            console.error("Status inválido:", newStatus);
            return;
        }

        await managementStore.updateTableStatus(tableToManage.value.id, newStatus);
        await restaurantStore.fetchRestaurantsFromAPI();
        isSessionControlModalOpen.value = false;
    } catch (errorMsg) {
        console.error("Erro ao mudar o status da mesa:", errorMsg);
    }
};

const onAddOrderToSession = (payload) => {
    sessionForModal.value = payload.session;
    sessionToUpdateId.value = payload.session.id;
    restaurantForModal.value = payload.restaurant;
    isAddOrderToSessionModalOpen.value = true;
    isSessionControlModalOpen.value = false; // Fecha o modal de controlo
};

const handleConfirmOrderForSession = async (items) => {
    if (!sessionToUpdateId.value) {
        showToast("Erro: Sessão da mesa não identificada.", "error");
        return;
    }
    try {
        await sessionStore.addOrderToSession(sessionToUpdateId.value, items);
        showToast('Pedido adicionado à mesa com sucesso!');

        // Recarrega os detalhes da sessão para atualizar o extrato
        await sessionStore.fetchActiveSessionForTable(restaurantForModal.value.id, tableToManage.value.id);

        // Fecha o modal de adicionar pedido e reabre o de controlo
        isAddOrderToSessionModalOpen.value = false;
        isSessionControlModalOpen.value = true;
    } catch (error) {
        showToast(`Erro ao adicionar pedido: ${error}`, "error");
    }
};

const handleLogout = () => {
    authStore.logout();
    showToast('Sessão terminada.');
    goToView('login');
};

const handleViewRoute = (restaurant) => {
    goToView('route', restaurant);
};

const goBack = () => goToView(previousViewState.value || 'home');

const onOpenStartSessionModal = (payload) => {
    tableToManage.value = payload.table;
    restaurantForModal.value = payload.restaurant; // <-- Guarda o restaurante
    isStartSessionModalOpen.value = true;
};

const onOpenSessionControlModal = (payload) => {
    tableToManage.value = payload.table;
    restaurantForModal.value = payload.restaurant; // <-- Guarda o restaurante
    isSessionControlModalOpen.value = true;
};

const handleStartSession = async (sessionData) => {
    // Pega no ID do restaurante que está a ser gerido na managementStore
    const restaurantId = managementStore.managedRestaurantId;

    if (!restaurantId) {
        showToast("Não foi possível identificar o restaurante.", "error");
        return;
    }
    try {
        await sessionStore.startSession({
            ...sessionData,
            restaurantId: restaurantId // Usa o ID correto
        });

        await restaurantStore.fetchRestaurantsFromAPI();
        isStartSessionModalOpen.value = false;

        // Abre o modal de controlo da sessão que acabámos de iniciar
        onOpenSessionControlModal({ table: tableToManage.value, restaurant: restaurantForModal.value });

        showToast(`Atendimento iniciado na mesa ${sessionData.tableId}!`);
    } catch (errorMsg) {
        showToast(`Erro ao iniciar atendimento: ${errorMsg}`, 'error');
    }
};

const onOpenReservationDetailModal = (reservation) => {
    reservationForDetailModal.value = reservation;
    isReservationDetailModalOpen.value = true;
};

const closeReservationDetailModal = () => {
    isReservationDetailModalOpen.value = false;
};

// Abre o modal de finalização
const onOpenFinishSessionModal = (payload) => {
    // CORREÇÃO: A função agora desempacota o 'payload' completo.
    sessionForModal.value = payload.session;
    consumptionForModal.value = payload.consumption; // <-- Guarda a lista de consumo

    isSessionControlModalOpen.value = false;
    isFinishSessionModalOpen.value = true;
};

const handleAddRestaurant = async (newRestaurantData) => {
    const added = await restaurantStore.addRestaurant(newRestaurantData);
    if (added) { // Verifica se o restaurante foi adicionado com sucesso
        showToast(`Restaurante '${added.name}' adicionado com sucesso!`);
        closeAddRestaurantModal();
    } else {
        showToast('Erro ao adicionar restaurante. Tente novamente.', 'error');
    }
};

const handleOrderForSession = async (dish, quantity = 1) => {
    if (!sessionToUpdateId.value) {
        showToast("Erro: Sessão da mesa não identificada.", "error");
        return;
    }

    // O 'dish' já tem restaurantId e restaurantName da nossa store
    const item = {
        ...dish,
        id: dish.id,
        price: dish.price,
        quantity: quantity
    };

    try {
        await sessionStore.addOrderToSession(sessionToUpdateId.value, [item]);
        showToast(`'${dish.dishName}' adicionado à mesa!`);

        // Recarrega os detalhes da sessão para atualizar o extrato
        await sessionStore.fetchActiveSessionForTable(restaurantForModal.value.id, tableToManage.value.id);

        // Fecha o modal do menu e reabre o de controlo da sessão
        closeMenuModal();
        isSessionControlModalOpen.value = true;
    } catch (error) {
        showToast(`Erro ao adicionar pedido: ${error}`, "error");
    }
};

const handleCancelWaitlist = async (waitlistEntry) => {
    try {
        await reservationStore.leaveWaitlist(waitlistEntry.restaurantId);
        showToast(`Você saiu da fila de espera de ${waitlistEntry.restaurantName}.`);
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const handleAddDish = async (newDishData) => {
    const added = await restaurantStore.addDish(newDishData);
    if (added) {
        showToast(`Prato '${added.dishName}' adicionado com sucesso!`);
    } else {
        showToast(`Erro ao adicionar prato. Verifique os dados e tente novamente.`, 'error');
    }
    closeAddDishModal();
};

const openDeleteDishModal = (dish) => {
    dishToDelete.value = dish;
    isDeleteModalOpen.value = true;
};

const closeDeleteDishModal = () => {
    isDeleteModalOpen.value = false;
    dishToDelete.value = null;
};

const handleDeleteDish = async () => {
    if (!dishToDelete.value) return;
    try {
        const success = await restaurantStore.deleteDish(dishToDelete.value.id);
        if (success) {
            showToast(`Prato '${dishToDelete.value.dishName}' excluído com sucesso!`);
        }
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    } finally {
        closeDeleteDishModal();
    }
};

const toggleNotifications = () => {
    isNotificationsOpen.value = !isNotificationsOpen.value;
    if (isNotificationsOpen.value) isFriendsChatOpen.value = false; // Fecha o outro painel
};

const toggleFriendsChat = () => {
    isFriendsChatOpen.value = !isFriendsChatOpen.value;
    if (isFriendsChatOpen.value) isNotificationsOpen.value = false; // Fecha o outro painel
};

const handleUpdateMap = async (updatedLayout) => {
    if (viewState.data && viewState.data.id) {
        try {
            await restaurantStore.updateRestaurantMap(viewState.data.id, updatedLayout);
            showToast('Mapa salvo com sucesso!');
        } catch (errorMsg) {
            showToast(errorMsg, 'error');
        }
    }
};

const handleBooking = async ({ restaurant, table, date, time, guests }) => {
    try {
        // CORREÇÃO: A função agora recebe 'date' e 'time' diretamente,
        // e não dentro de um objeto 'dateTime'.
        const bookingTimeForAPI = `${date} ${time}:00`;

        const reservationData = {
            restaurantId: restaurant.id,
            tableId: table.id,
            bookingTime: bookingTimeForAPI,
            guests: guests,
            status: 'pending'
        };

        const success = await reservationStore.createReservation(reservationData);

        if (success) {
            restaurantStore.updateTableStatus({
                restaurantId: restaurant.id,
                tableId: table.id,
                newStatus: 'occupied'
            });

            await restaurantStore.fetchRestaurantsFromAPI(); // Garante que o mapa é atualizado

            confirmationModalMessage.value = "A sua reserva foi confirmada com sucesso!";
            isConfirmationModalOpen.value = true;

            // A lógica do WhatsApp
            const [year, month, day] = date.split('-').map(Number);
            const [hours, minutes] = time.split(':').map(Number);
            const localDateTime = new Date(year, month - 1, day, hours, minutes);

            setTimeout(() => {
                sendWhatsAppConfirmation({ restaurant, table, dateTime: localDateTime, guests });
            }, 500);

            goToView('myReservations');
        }
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const addToCart = ({ dish, quantity, isPlanned = false, dineOption = 'delivery', customization = null, encontroPayload = null }) => {
    if (sessionToUpdateId.value) {
        handleOrderForSession(dish, quantity);
        sessionToUpdateId.value = null;
        closeActionModal();
    } else {
        const cartItemId = `${dish.id}-${Date.now()}`;
        cart.push({ ...dish, quantity, customization, isPlanned, dineOption, cartItemId, encontroPayload });
        closeCustomizeModal();
        closeActionModal();
        showToast(`${quantity}x '${dish.dishName}' adicionado!`);
    }
};

const handleConfirmEncontro = async (encontroData) => {
    try {
        const savedEncontro = await encontroStore.saveEncontroToAPI();

        if (encontroData.paymentOption === 'agora') {
            encontroData.guests.forEach(guest => {
                Object.values(guest.menu).forEach(dishObject => {
                    if (dishObject && dishObject.id) {
                        const { customization, ...restOfDish } = dishObject;

                        addToCart({
                            dish: { ...restOfDish, restaurantId: encontroData.restaurantId, restaurantName: encontroData.restaurantName },
                            quantity: 1,
                            isPlanned: true,
                            dineOption: 'dine-in',
                            customization: customization || null,
                            encontroPayload: {
                                restaurantId: encontroData.restaurantId,
                                tableId: encontroData.selectedTable.id,
                                dateTime: encontroData.dateTime,
                                guests: encontroData.guests.length,
                                encontroId: savedEncontro.encontroId,
                                menu: encontroData.guests.map(g => g.menu)
                            }
                        });
                        // --- FIM DA CORREÇÃO ---
                    }
                });
            });
            goToView('cart');
            showToast(`Encontro planeado! Por favor, finalize o pagamento.`);
        } else { // 'Pagar no Local'
            await reservationStore.createReservation({
                restaurantId: encontroData.restaurantId,
                tableId: encontroData.selectedTable.id,
                bookingTime: encontroData.dateTime,
                guests: encontroData.guests.length,
                status: 'confirmed',
                encontroId: savedEncontro.encontroId
            });
            await restaurantStore.fetchRestaurantsFromAPI();
            showToast(`Encontro planeado com sucesso e mesa reservada!`);
        }
    } catch (errorMsg) {
        showToast(`Erro: ${errorMsg}`, 'error');
    }
};

// Lida com a confirmação do pagamento
const handleFinishSession = async (paymentMethod) => {
    const sessionId = sessionForModal.value?.id;
    if (!sessionId) {
        showToast("Não foi possível identificar a sessão para finalizar.", "error");
        return;
    }

    try {
        await sessionStore.finishSession(sessionId, paymentMethod);
        isFinishSessionModalOpen.value = false;
        await restaurantStore.fetchRestaurantsFromAPI();
        await managementStore.fetchManagementData();
        showToast(`Atendimento da mesa ${tableToManage.value.id} finalizado com sucesso!`);
    } catch (errorMsg) {
        showToast(`Erro ao finalizar atendimento: ${errorMsg}`, 'error');
    }
};

const showSharedReservation = (encontroData, invitedUser) => {
    const restaurant = restaurantStore.restaurants.find(r => r.id === encontroData.restaurantId);
    if (restaurant) {
        goToView('sharedReservation', {
            encounter: encontroData,
            currentUser: invitedUser,
            restaurant: restaurant
        });
    }
};

const openMenuModal = (restaurant) => {
    currentRestaurantForMenu.value = restaurant;
    isMenuModalOpen.value = true;
};

const closeMenuModal = () => {
    isMenuModalOpen.value = false;
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
        encontroStore.setGuestMenu(guest.id, menuKey, item);
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

const handleUpdateCartItem = (customizedData) => {
    // Cenário 1: Atualização vinda do painel de gestão.
    if (isAddOrderToSessionModalOpen.value) {
        const updatedItem = {
            ...itemToCustomize.value,
            customization: customizedData.customization
        };
        addOrderModalRef.value?.updateOrderItem(updatedItem);
        showToast("Item atualizado na comanda!");
    }
    // Cenário 2: Atualização vinda do Planeador de Encontros.
    else if (dishModalProps.value.plannerData) {
        const { guest, categoryKey } = dishModalProps.value.plannerData;
        const customizedItemForPlanner = { ...itemToCustomize.value, customization: customizedData.customization };
        encontroStore.setGuestMenu(guest.id, categoryKey, customizedItemForPlanner);
        showToast("Seleção do convidado atualizada!");
    }
    // Cenário 3: Atualização/Adição ao carrinho normal do cliente.
    else {
        const itemIndex = cart.findIndex(item => item.cartItemId === customizedData.dish.cartItemId);
        if (itemIndex !== -1) {
            // Se o item já existe no carrinho, atualiza a sua personalização.
            cart[itemIndex].customization = customizedData.customization;
            showToast(`Item '${customizedData.dish.dishName}' atualizado no carrinho.`);
        } else {
            // Se o item não existe no carrinho (vindo de um card), adiciona-o com a personalização.
            // CORREÇÃO: Passa os dados corretamente para a função addToCart.
            addToCart({
                dish: customizedData.dish,
                quantity: 1, // A quantidade é sempre 1 ao adicionar pela primeira vez
                customization: customizedData.customization,
                dineOption: 'delivery'
            });
        }
    }
    closeCustomizeModal();
};


const toggleDishFavorite = async (dish) => {
    const actionResult = await userDataStore.toggleFavoriteDish(dish.id);
    if (actionResult === 'added') {
        showToast(`'${dish.dishName}' adicionado aos favoritos!`);
    } else if (actionResult === 'removed') {
        showToast(`'${dish.dishName}' removido dos favoritos.`);
    }
};

const toggleRestaurantFavorite = async (restaurant) => {
    // 1. Captura o resultado da ação (ex: 'added' ou 'removed')
    const actionResult = await userDataStore.toggleFavoriteRestaurant(restaurant.id);

    // 2. Mostra a mensagem correta com base no resultado
    if (actionResult === 'added') {
        showToast(`'${restaurant.name}' adicionado aos favoritos!`);
    } else if (actionResult === 'removed') {
        showToast(`'${restaurant.name}' removido dos favoritos.`);
    }
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

const handlePaymentSuccess = async () => {
    if (cart.length === 0) return;
    const finalTotal = cart.reduce((sum, item) => sum + (parseFloat(item.price) * item.quantity), 0);
    const encontroItem = cart.find(item => item.isPlanned && item.encontroPayload);

    try {
        let reservationIdParaPedido = null;
        if (encontroItem) {
            // --- INÍCIO DA CORREÇÃO 1: Mapeamento de 'dateTime' para 'bookingTime' ---
            const payload = encontroItem.encontroPayload;
            const reservationData = {
                restaurantId: payload.restaurantId,
                tableId: payload.tableId,
                bookingTime: payload.dateTime, // Remapeia o nome do campo
                guests: payload.guests,
                encontroId: payload.encontroId,
                status: 'confirmed'
            };

            const reservationResult = await reservationStore.createReservation(reservationData);
            reservationIdParaPedido = reservationResult.reservationId;
            // --- FIM DA CORREÇÃO 1 ---

            const restaurant = restaurantStore.restaurants.find(r => r.id === payload.restaurantId);
            const table = restaurant?.tables.find(t => t.id.toString() === payload.tableId.toString());

            if (restaurant && table) {
                // Passa o menu para a função de notificação
                sendWhatsAppConfirmation({
                    restaurant,
                    table,
                    dateTime: new Date(payload.dateTime),
                    guests: payload.guests,
                    menu: payload.menu
                });
            }
        }

        await orderStore.createOrder(cart, finalTotal, reservationIdParaPedido);

        cart.length = 0;
        closePaymentModal();
        closePixModal();
        await restaurantStore.fetchRestaurantsFromAPI();
        goToView('home');
        showToast("Pedido realizado e pago com sucesso! Obrigado!");
    } catch (errorMsg) {
        showToast(`Erro no pagamento: ${errorMsg}`, 'error');
    }
};

const openTableDetailModal = (table) => {
    managementStore.fetchTableDetails(managedRestaurant.value.id, table.id);
    currentTableForDetail.value = table;
    isTableDetailModalOpen.value = true;
}

const handleUpdateTableStatus = ({ tableId, status }) => {
    // A gestão é feita pelo clique na modal, mas o evento vem da TableDetailModal
    const restaurant = restaurantStore.restaurants.find(r => r.tables.some(t => t.id === tableId));
    if (restaurant) {
        restaurantStore.updateTableStatus({ restaurantId: restaurant.id, tableId, newStatus: status });
    }
};

const orderNowFromAction = ({ dish, quantity }) => {
    // Pedidos "agora" são assumidos como entrega, a não ser que o fluxo mude
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
    const { restaurant, table, dateTime, guests, menu } = reservationDetails;

    if (!userProfile.value || !userProfile.value.phone) {
        showToast("Não foi possível enviar a confirmação: número de telefone não encontrado no perfil.", "error");
        return;
    }
    let phone = userProfile.value.phone.replace(/\D/g, '');
    if (phone.length <= 11) phone = '55' + phone;

    const formattedDate = dateTime.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' });
    const formattedTime = dateTime.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    let message = `Olá! 👋\n\nSua reserva no *${restaurant.name}* para um Encontro Planejado está confirmada!\n\n*Detalhes:*\n- *Mesa:* ${table.id}\n- *Data:* ${formattedDate}\n- *Hora:* ${formattedTime}\n- *Pessoas:* ${guests}`;

    if (menu && menu.length > 0) {
        message += `\n\n*Itens pré-selecionados:*\n`;
        const allItems = menu.flatMap(guestMenu => Object.values(guestMenu)).filter(item => item && item.dishName);

        const itemCounts = allItems.reduce((acc, item) => {
            acc[item.dishName] = (acc[item.dishName] || 0) + 1;
            return acc;
        }, {});

        for (const [dishName, count] of Object.entries(itemCounts)) {
            message += `- ${count}x ${dishName}\n`;
        }
    }

    message += `\nObrigado por usar o Menu Connect!`;

    const whatsappUrl = `https://wa.me/${phone}?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
    showToast("Confirmação enviada para o WhatsApp!");
};

const handleWaitingList = async ({ restaurant }) => {
    try {
        await reservationStore.joinWaitlist(restaurant.id);
        showToast(`Você entrou na fila de espera de ${restaurant.name}.`);
        goToView('myReservations');
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const handleCancellation = async (reservation) => {
    try {
        await reservationStore.cancelReservation(reservation.id);
        showToast(`Reserva da mesa ${reservation.tableId} cancelada.`);
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const handleConfirmReservation = async (reservation) => {
    try {
        await reservationStore.confirmReservation(reservation.id);
        showToast(`Reserva para a mesa ${reservation.tableId} confirmada!`);
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
};

const handleUpdateUser = async (updatedData) => {
    try {
        await authStore.updateProfile(updatedData);
        showToast('Perfil atualizado com sucesso!');
    } catch (errorMsg) {
        showToast(errorMsg, 'error');
    }
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

const openCustomizeModal = (payload) => {
    // Se vier do carrinho, 'payload' é o item. Se vier do planeador, é um objeto com 'guest' e 'item'.
    itemToCustomize.value = payload.item || payload;
    // Guarda os dados extras do planeador para podermos salvar no sítio certo
    dishModalProps.value.plannerData = payload.guest ? payload : null;
    isActionModalOpen.value = false;
    isCustomizeModalOpen.value = true;
};

const closeCustomizeModal = () => {
    isCustomizeModalOpen.value = false;
};



</script>

<template>
    <div>
        <template v-if="!authStore.isAuthenticated">
            <LoginView v-if="viewState.name === 'login'" @login="handleLogin" @navigate-to="goToView" />
            <RegisterView v-if="viewState.name === 'register'" @register="handleRegister" @navigate-to="goToView" />
        </template>

        <template v-else>
            <app-header :cart-item-count="cartItemCount" :user="userProfile"
                :searchable-items="restaurantStore.searchableItems" :active-view="viewState.name"
                :is-notifications-open="isNotificationsOpen" :is-friends-chat-open="isFriendsChatOpen"
                :notifications="notifications" :friends="friends" @navigate="goToView" @logout="handleLogout"
                @search-navigate="handleSearchNavigation"
                @toggle-notifications="isNotificationsOpen = !isNotificationsOpen"
                @toggle-friends-chat="isFriendsChatOpen = !isFriendsChatOpen" />

            <main>
                <HomeView v-if="viewState.name === 'home'" :restaurants="restaurantStore.featuredRestaurants"
                    :new-restaurants="newlyAddedRestaurants" :trending-dishes="trendingDishes"
                    :frequent-dishes="frequentDishes" :favorite-dishes="userDataStore.favoriteDishIds"
                    :favorite-restaurants="userDataStore.favoriteRestaurantIds" :all-dishes="restaurantStore.allDishes"
                    @open-action-modal="openActionModal" @open-dine-options="openDineOptionsModal"
                    @toggle-dish-favorite="toggleDishFavorite" @toggle-restaurant-favorite="toggleRestaurantFavorite"
                    @request-reservation="restaurant => goToView('reservation', restaurant)"
                    @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
                    @open-payment-modal="openCheckout" @open-menu-modal="openMenuModal" />
                <RestaurantsView v-if="viewState.name === 'restaurants'" :restaurants="restaurantStore.restaurants"
                    :favorite-restaurants="userDataStore.favoriteRestaurantIds"
                    @toggle-favorite="toggleRestaurantFavorite"
                    @request-reservation="restaurant => goToView('reservation', restaurant)"
                    @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
                    @open-add-restaurant-modal="openAddRestaurantModal" @open-menu-modal="openMenuModal" />
                <DishesView v-if="viewState.name === 'dishes'" :dishes="restaurantStore.allDishes"
                    :favorite-dishes="userDataStore.favoriteDishIds" @open-action-modal="openActionModal"
                    @open-dine-options="openDineOptionsModal" @toggle-favorite="toggleDishFavorite"
                    @open-add-dish-modal="openAddDishModal" />
                <RestaurantDetailView v-if="viewState.name === 'restaurantDetail'" :restaurant="viewState.data"
                    :user-profile="userProfile" :all-users="allUsers" @back-to-main="goBack"
                    @open-action-modal="openActionModal" @open-add-dish-modal="openAddDishModal"
                    @confirm-encontro="handleConfirmEncontro" @open-menu-item-select-modal="openSelectMenuItemModal"
                    @open-customize-modal="openCustomizeModal" @view-route="handleViewRoute"
                    @delete-dish="openDeleteDishModal" />
                <RouteView v-if="viewState.name === 'route'" :restaurant="viewState.data" @back="goBack" />
                <ReservationView v-if="viewState.name === 'reservation'" :restaurant="viewState.data"
                    :user-reservations="reservationStore.userReservations.booked" @back-to-main="goBack"
                    @update-map="handleUpdateMap" @book-table="handleBooking" @join-waitlist="handleWaitingList"
                    @cancel-reservation="handleCancellation('booked')" />
                <MyReservationsView v-if="viewState.name === 'myReservations'"
                    :reservations="reservationStore.userReservations" @cancel-reservation="handleCancellation"
                    @confirm-reservation="handleConfirmReservation" @back-to-main="goBack"
                    @cancel-waitlist="handleCancelWaitlist" />
                <UserProfileView v-if="viewState.name === 'userProfile'" :user="userProfile"
                    @update-user="handleUpdateUser" @back-to-main="goBack" />
                <CartView v-if="viewState.name === 'cart'" :cart-items="cart" :all-dishes="restaurantStore.allDishes"
                    @update-quantity="updateQuantity" @remove-from-cart="removeFromCart" @add-to-cart="addToCart"
                    @back-to-main="goBack" @checkout="openCheckout" @edit-item="openCustomizeModal"
                    @update-dine-option="handleUpdateDineOption" />
                <FavoriteRestaurantsView v-if="viewState.name === 'favoriteRestaurants'"
                    :favorite-restaurants="favoritedRestaurantsList" @toggle-favorite="toggleRestaurantFavorite"
                    @request-reservation="restaurant => goToView('reservation', restaurant)"
                    @view-restaurant="restaurant => goToView('restaurantDetail', restaurant)"
                    @back-to-main="goToView('home')" @open-menu-modal="openMenuModal" />
                <FavoriteDishesView v-if="viewState.name === 'favoriteDishes'" :favorite-dishes="favoritedDishesList"
                    @toggle-favorite="toggleDishFavorite" @open-action-modal="openActionModal"
                    @open-dine-options="openDineOptionsModal" @back-to-main="goToView('home')" />
                <OrderHistoryView v-if="viewState.name === 'orderHistory'" :order-history="orderHistory"
                    @back-to-main="goToView('home')" />
                <!-- <TableManagementView v-if="viewState.name === 'tableManagement'" :order-history="orderHistory"
                    @open-table-detail-modal="openTableDetailModal" /> -->
                <ManagementView v-if="viewState.name === 'dashboard'"
                    @open-start-session-modal="onOpenStartSessionModal"
                    @open-session-control-modal="onOpenSessionControlModal"
                    @open-reservation-detail-modal="onOpenReservationDetailModal" />
                <!-- <DashboardView v-if="viewState.name === 'dashboard'" :reservations="userReservations"
                    :order-history="orderHistory" @navigate-to="goToView" /> -->
                <ReservationSharedView v-if="viewState.name === 'sharedReservation'"
                    :encounter="viewState.data.encounter" :current-user="viewState.data.currentUser"
                    :restaurant="viewState.data.restaurant" @back-to-main="goToView('home')"
                    @open-menu-item-select-modal="openSelectMenuItemModal" />
            </main>

            <Footer />

            <AddRestaurantModal v-if="isAddRestaurantModalOpen" @close="closeAddRestaurantModal"
                @add-restaurant="handleAddRestaurant" />
            <AddDishModal v-if="isAddDishModalOpen" :allRestaurants="restaurantStore.restaurants"
                :restaurant="dishModalProps.restaurant" :category="dishModalProps.category" @close="closeAddDishModal"
                @add-dish="handleAddDish" />
            <ActionModal v-if="isActionModalOpen" :dish="currentDishForAction" @close-modal="closeActionModal"
                @add-to-cart="addToCart" @order-now="orderNowFromAction" @open-customize-modal="openCustomizeModal" />
            <CustomizeDishModal v-if="isCustomizeModalOpen" :dish="itemToCustomize" @close="closeCustomizeModal"
                @add-to-cart="handleUpdateCartItem" />
            <DineOptionsModal v-if="isDineOptionsModalOpen" :dish="currentDishForAction"
                @close-modal="closeDineOptionsModal" @dine-in="handleDineInOrTakeout" @takeout="handleDineInOrTakeout"
                @reserve="handleGoToReservation" />
            <PaymentModal v-if="isPaymentModalOpen" :cart="cart" :shortcut="paymentShortcut"
                @close-modal="closePaymentModal" @payment-success="handlePaymentSuccess" />
            <PixModal v-if="isPixModalOpen" :cart="cart" @close="closePixModal"
                @payment-success="handlePaymentSuccess" />
            <ConfirmationModal v-if="isConfirmationModalOpen" :message="confirmationModalMessage"
                @close="isConfirmationModalOpen = false" />
            <SelectMenuItemModal v-if="isSelectMenuItemModalOpen" :menu-items="menuItemModalProps.menuItems"
                :category="menuItemModalProps.category" @close="isSelectMenuItemModalOpen = false"
                @item-selected="handleMenuItemSelection" />
            <TableDetailModal v-if="isTableDetailModalOpen" :table="currentTableForDetail"
                :details="managementStore.state.selectedTableDetails" @close="isTableDetailModalOpen = false" />
            <ChatModal />
            <MenuModal v-if="isMenuModalOpen" :restaurant="currentRestaurantForMenu" @close="closeMenuModal"
                @open-action-modal="openActionModal" />
            <StartSessionModal v-if="isStartSessionModalOpen" :table="tableToManage"
                @close="isStartSessionModalOpen = false" @start-session="handleStartSession" />
            <SessionControlModal v-if="isSessionControlModalOpen" :table="tableToManage"
                :restaurant="restaurantForModal" @close="isSessionControlModalOpen = false"
                @change-status="handleChangeTableStatus" @add-order="onAddOrderToSession"
                @finish-session="onOpenFinishSessionModal" />
            <AddOrderToSessionModal v-if="isAddOrderToSessionModalOpen" ref="addOrderModalRef"
                :session="sessionForModal" :restaurant="restaurantForModal"
                @close="isAddOrderToSessionModalOpen = false" @confirm-order="handleConfirmOrderForSession"
                @customize-item="onCustomizeSessionItem" />
            <FinishSessionModal v-if="isFinishSessionModalOpen" :session="sessionForModal"
                :consumption="consumptionForModal" @close="isFinishSessionModalOpen = false"
                @confirm="handleFinishSession" />
            <DeleteConfirmationModal v-if="isDeleteModalOpen" :item-name="dishToDelete ? dishToDelete.dishName : ''"
                @close="closeDeleteDishModal" @confirm="handleDeleteDish" />
            <ReservationDetailModal v-if="isReservationDetailModalOpen" :reservation="reservationForDetailModal"
                @close="closeReservationDetailModal" />
            <div
                :class="['toast-notification fixed bottom-5 right-5 bg-gray-800 text-white px-6 py-3 rounded-lg shadow-lg', { 'show': isToastVisible }]">
                {{ toastMessage }}
            </div>
        </template>
    </div>
</template>