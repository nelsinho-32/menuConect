<template>
    <section class="my-12">
        <h2 class="section-title mb-6">Cardápio</h2>
        <div class="border-b border-gray-200 mb-6">
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

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div v-for="item in filteredMenu" :key="item.id" class="bg-white p-4 rounded-lg shadow-sm flex justify-between items-start">
                <div>
                    <h4 class="font-bold text-lg">{{ item.name }}</h4>
                    <p class="text-sm text-gray-500 mt-1">{{ item.description }}</p>
                    <p class="font-bold text-indigo-600 mt-2">R$ {{ item.price.toFixed(2).replace('.', ',') }}</p>
                </div>
                <button @click="$emit('openActionModal', item)" class="ml-4 bg-indigo-100 text-indigo-600 p-2 rounded-full hover:bg-indigo-200 flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"></line><line x1="5" y1="12" x2="19" y2="12"></line></svg>
                </button>
            </div>
        </div>
    </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
    menu: {
        type: Array,
        required: true
    }
});
defineEmits(['openActionModal']);

const categories = computed(() => [...new Set(props.menu.map(item => item.category))]);
const selectedCategory = ref(categories.value[0] || '');

const filteredMenu = computed(() => {
    return props.menu.filter(item => item.category === selectedCategory.value);
});

// Garante que uma categoria válida seja selecionada se o menu mudar
watch(categories, (newCategories) => {
    if (newCategories.length && !newCategories.includes(selectedCategory.value)) {
        selectedCategory.value = newCategories[0];
    }
});
</script>
