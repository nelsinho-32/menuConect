<template>
    <section class="my-12">
        <div class="flex justify-between items-center mb-6">
            <h2 class="section-title">Cardápio</h2>
        </div>
        
        <div class="border-b border-gray-200">
            <nav class="-mb-px flex space-x-6" aria-label="Tabs">
                <button v-for="category in categories" :key="category" 
                    @click="selectedCategory = category"
                    :class="[
                        category === selectedCategory 
                            ? 'border-indigo-500 text-indigo-600' 
                            : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
                        'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
                    ]">
                    {{ category }}
                </button>
            </nav>
        </div>

        <div class="mt-6">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div v-if="canManageMenu" @click="$emit('openAddMenuItemModal', selectedCategory)"
                    class="bg-gray-50 border-2 border-dashed border-gray-300 rounded-lg flex items-center justify-center text-gray-500 hover:border-indigo-500 hover:text-indigo-600 cursor-pointer min-h-[140px]">
                    <div class="text-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" fill="currentColor" class="mx-auto" viewBox="0 0 16 16">
                            <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
                            <path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"/>
                        </svg>
                        <p class="font-semibold mt-2">Adicionar Item</p>
                    </div>
                </div>

                <div v-for="item in filteredMenu" :key="item.id" class="bg-white p-4 rounded-lg shadow-sm flex gap-4">
                    <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.name" class="w-32 h-32 object-cover rounded-md flex-shrink-0">
                    <div class="flex-grow flex flex-col">
                        <div>
                            <h4 class="font-bold text-lg">{{ item.name }}</h4>
                            <p class="text-sm text-gray-500 mt-1">{{ item.description }}</p>
                        </div>
                        <div class="mt-auto flex justify-between items-end">
                             <p class="font-bold text-indigo-600 text-lg">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
                             <button @click="$emit('openActionModal', item)" class="bg-indigo-100 text-indigo-600 p-2 rounded-full hover:bg-indigo-200 flex-shrink-0">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useUserStore } from '@/stores/userStore';
import { useRestaurantStore } from '@/stores/restaurantStore';
import { useAuthStore } from '@/stores/authStore';

const userStore = useUserStore();
const authStore = useAuthStore();
const restaurantStore = useRestaurantStore();

const props = defineProps({
    menu: { type: Array, required: true },
    restaurantId: { type: Number, required: true }
});

defineEmits(['openActionModal', 'openAddMenuItemModal']);

const canManageMenu = computed(() => {
    if (!authStore.currentUser) return false;
    // Admin pode sempre
    if (authStore.currentUser.role === 'admin') return true;
    // Empresa só pode se o ID do restaurante corresponder
    if (authStore.currentUser.role === 'empresa') {
        return authStore.currentUser.restaurant_id === props.restaurantId;
    }
    return false;
});

// Define as categorias fixas para garantir a ordem
const categories = ref(['Entradas', 'Prato Principal', 'Sobremesas', 'Bebidas']);
const selectedCategory = ref(categories.value[0]);

const filteredMenu = computed(() => {
    // Adiciona uma verificação para garantir que o menu não é nulo/indefinido
    if (!props.menu) return [];
    return props.menu.filter(item => item.category === selectedCategory.value);
});
</script>