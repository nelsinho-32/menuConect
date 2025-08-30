<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Criar Nova Promoção</h3>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4 max-h-[70vh] overflow-y-auto">
                <div v-if="authStore.currentUser?.role === 'admin'">
                    <label for="restaurant" class="block text-sm font-medium text-gray-700">Restaurante</label>
                    <select id="restaurant" v-model="form.restaurantId" required class="mt-1 block w-full rounded-md border-gray-300">
                        <option disabled value="">Selecione um restaurante</option>
                        <option v-for="restaurant in restaurantStore.restaurants" :key="restaurant.id" :value="restaurant.id">
                            {{ restaurant.name }}
                        </option>
                    </select>
                </div>
                <div>
                    <label for="title" class="block text-sm font-medium text-gray-700">Título da Promoção</label>
                    <input type="text" id="title" v-model="form.title" required placeholder="Ex: Happy Hour de Verão" class="mt-1 block w-full rounded-md border-gray-300">
                </div>
                <div>
                    <label for="description" class="block text-sm font-medium text-gray-700">Descrição</label>
                    <textarea id="description" v-model="form.description" rows="3" placeholder="Ex: 50% de desconto em todas as cervejas das 18h às 20h" class="mt-1 block w-full rounded-md border-gray-300"></textarea>
                </div>
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label for="discount_type" class="block text-sm font-medium text-gray-700">Tipo de Desconto</label>
                        <select id="discount_type" v-model="form.discount_type" class="mt-1 block w-full rounded-md border-gray-300">
                            <option value="percentage">Percentagem (%)</option>
                            <option value="fixed_amount">Valor Fixo (R$)</option>
                        </select>
                    </div>
                    <div>
                        <label for="discount_value" class="block text-sm font-medium text-gray-700">Valor do Desconto</label>
                        <input type="number" step="0.01" id="discount_value" v-model="form.discount_value" required placeholder="Ex: 20 (para 20%)" class="mt-1 block w-full rounded-md border-gray-300">
                    </div>
                </div>
                 <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label for="start_date" class="block text-sm font-medium text-gray-700">Data de Início (Opcional)</label>
                        <input type="date" id="start_date" v-model="form.start_date" class="mt-1 block w-full rounded-md border-gray-300">
                    </div>
                    <div>
                        <label for="end_date" class="block text-sm font-medium text-gray-700">Data de Fim (Opcional)</label>
                        <input type="date" id="end_date" v-model="form.end_date" class="mt-1 block w-full rounded-md border-gray-300">
                    </div>
                </div>
                 <div>
                    <label class="flex items-center">
                        <input type="checkbox" v-model="form.active" class="h-4 w-4 rounded border-gray-300 text-indigo-600">
                        <span class="ml-2 text-sm text-gray-700">Promoção Ativa</span>
                    </label>
                </div>

                <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3 -m-6 mt-6 pt-6">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Salvar Promoção</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useManagementStore } from '@/stores/managementStore';
import { useRestaurantStore } from '@/stores/restaurantStore'; // Importar a store de restaurantes

const emit = defineEmits(['close', 'createPromotion']);
const authStore = useAuthStore();
const managementStore = useManagementStore();
const restaurantStore = useRestaurantStore(); // Inicializar a store

const form = reactive({
    title: '',
    description: '',
    discount_type: 'percentage',
    discount_value: null,
    start_date: null,
    end_date: null,
    active: true,
    restaurantId: null // Começa como nulo para o admin
});

// Garante que o ID do restaurante selecionado no painel seja o padrão
onMounted(() => {
    if (authStore.currentUser?.role === 'admin') {
        form.restaurantId = managementStore.managedRestaurantId;
    }
});

const handleSubmit = () => {
    // Para 'empresa', o ID já está no token. Para 'admin', usamos o ID selecionado no formulário.
    emit('createPromotion', { ...form });
};
</script>