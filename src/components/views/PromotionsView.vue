<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex flex-col md:flex-row justify-between md:items-center mb-8 gap-4">
            <div>
                <h1 class="text-3xl font-bold">Gestão de Promoções</h1>
                <p v-if="managedRestaurant" class="text-gray-500">
                    Crie e gira as promoções para <span class="font-semibold text-indigo-600">{{ managedRestaurant.name }}</span>
                </p>
            </div>
            <button @click="$emit('openPromotionModal')" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700 flex items-center gap-2 self-start md:self-center">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16"><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/></svg>
                Criar Nova Promoção
            </button>
        </div>

        <div v-if="promotionStore.state.isLoading" class="text-center py-10">
            <p class="text-gray-500">A carregar promoções...</p>
        </div>
        <div v-else-if="promotionStore.state.error" class="text-center py-10 bg-red-50 text-red-700 rounded-lg">
            <p>{{ promotionStore.state.error }}</p>
        </div>
        <div v-else-if="promotionStore.state.promotions.length === 0" class="text-center py-20 bg-white rounded-lg shadow-md">
            <p class="text-gray-500">Ainda não há nenhuma promoção criada para este restaurante.</p>
            <p class="text-sm text-gray-400 mt-2">Clique em "Criar Nova Promoção" para começar.</p>
        </div>

        <div v-else class="space-y-4">
            <div v-for="promo in promotionStore.state.promotions" :key="promo.id" class="bg-white p-4 rounded-lg shadow-md flex justify-between items-center">
                <div>
                    <div class="flex items-center gap-3">
                        <span class="px-2 py-1 text-xs font-semibold rounded-full" :class="promo.active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'">
                            {{ promo.active ? 'Ativa' : 'Inativa' }}
                        </span>
                        <h3 class="font-bold text-lg text-gray-800">{{ promo.title }}</h3>
                    </div>
                    <p class="text-sm text-gray-600 mt-1">{{ promo.description }}</p>
                    <p class="text-xs text-gray-400 mt-2">Validade: {{ formatDate(promo.start_date) }} - {{ formatDate(promo.end_date) || 'Sem data final' }}</p>
                </div>
                <div class="text-right">
                    <p class="font-bold text-2xl text-indigo-600">{{ formatDiscount(promo) }}</p>
                    </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, computed, watch } from 'vue';
import { usePromotionStore } from '@/stores/promotionsStore';
import { useManagementStore } from '@/stores/managementStore';
import { useRestaurantStore } from '@/stores/restaurantStore';

const promotionStore = usePromotionStore();
const managementStore = useManagementStore();
const restaurantStore = useRestaurantStore();

defineEmits(['openPromotionModal']);

const managedRestaurant = computed(() => {
    return restaurantStore.restaurants.find(r => r.id === managementStore.managedRestaurantId);
});

// Busca as promoções quando o componente é montado
onMounted(() => {
    promotionStore.fetchPromotions();
});

// Observa se o admin muda de restaurante e busca as novas promoções
watch(() => managementStore.managedRestaurantId, () => {
    promotionStore.fetchPromotions();
});

const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', { timeZone: 'UTC' }); // UTC para evitar problemas de fuso horário
};

const formatDiscount = (promo) => {
    if (promo.discount_type === 'percentage') {
        return `${promo.discount_value}% OFF`;
    }
    return `R$ ${parseFloat(promo.discount_value).toFixed(2).replace('.', ',')} OFF`;
};
</script>