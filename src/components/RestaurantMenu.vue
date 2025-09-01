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

                <div v-for="item in filteredMenu" :key="item.id" class="bg-white p-4 rounded-lg shadow-sm flex gap-4" :class="{'opacity-60': !item.is_available}">
                    <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.dishName" class="w-32 h-32 object-cover rounded-md flex-shrink-0">
                    <div class="flex-grow flex flex-col">
                        <div>
                            <div class="flex justify-between items-start">
                                <h4 class="font-bold text-lg">{{ item.dishName }}</h4>
                                <button v-if="canManageMenu" @click.stop="$emit('deleteDish', item)" title="Excluir Prato" class="text-gray-400 hover:text-red-500 p-1 -mr-1">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" fill="currentColor" viewBox="0 0 16 16">
                                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                                    </svg>
                                </button>
                            </div>
                            <p class="text-sm text-gray-500 mt-1">{{ item.description }}</p>
                             <div v-if="canManageMenu" class="mt-2">
                                <label class="flex items-center cursor-pointer">
                                    <div class="relative">
                                        <input type="checkbox" :checked="item.is_available" @change="$emit('toggleAvailability', item)" class="sr-only">
                                        <div class="block bg-gray-600 w-10 h-6 rounded-full"></div>
                                        <div :class="{'translate-x-4': item.is_available, 'translate-x-0': !item.is_available}" class="dot absolute left-1 top-1 bg-white w-4 h-4 rounded-full transition-transform"></div>
                                    </div>
                                    <div class="ml-3 text-gray-700 text-sm font-medium">
                                        {{ item.is_available ? 'Disponível' : 'Esgotado' }}
                                    </div>
                                </label>
                            </div>
                             </div>
                        <div class="mt-auto flex justify-between items-end">
                             <p class="font-bold text-indigo-600 text-lg">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
                             <button @click="$emit('openActionModal', item)" class="bg-indigo-100 text-indigo-600 p-2 rounded-full hover:bg-indigo-200 flex-shrink-0" :disabled="!item.is_available">
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
import { useAuthStore } from '@/stores/authStore';

const authStore = useAuthStore();

const props = defineProps({
    menu: { type: Array, required: true },
    restaurantId: { type: Number, required: true }
});

// ADICIONE 'toggleAvailability' AOS EVENTOS EMITIDOS
defineEmits(['openActionModal', 'openAddMenuItemModal', 'deleteDish', 'toggleAvailability']);

const canManageMenu = computed(() => {
    if (!authStore.currentUser) return false;
    if (authStore.currentUser.role === 'admin') return true;
    if (authStore.currentUser.role === 'empresa') {
        return authStore.currentUser.restaurant_id === props.restaurantId;
    }
    return false;
});

const categories = ref(['Entradas', 'Prato Principal', 'Sobremesas', 'Bebidas']);
const selectedCategory = ref(categories.value[0]);

const filteredMenu = computed(() => {
    if (!props.menu) return [];
    return props.menu.filter(item => item.category === selectedCategory.value);
});
</script>

<style scoped>
.dot {
    transition: transform 0.2s ease-in-out;
}
</style>