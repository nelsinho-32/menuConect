<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt;
            Voltar</button>
        <div class="flex justify-between items-center mb-8">
            <h1 class="text-3xl font-bold">Minhas Listas</h1>
            <button @click="$emit('openCreateListModal')"
                class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                Criar Nova Lista
            </button>
        </div>

        <div v-if="listStore.state.isLoading">A carregar...</div>
        <div v-else-if="listStore.state.myLists.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Você ainda não criou nenhuma lista.</p>
        </div>
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="list in listStore.state.myLists" :key="list.id" @click="$emit('viewList', list.id)"
                class="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow cursor-pointer">
                <h3 class="font-bold text-xl text-gray-800">{{ list.name }}</h3>
                <p class="text-sm text-gray-500 mt-1">{{ list.description }}</p>
                <p class="text-sm text-indigo-600 font-semibold mt-4">{{ list.itemCount }} itens</p>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useListStore } from '@/stores/listStore';

const listStore = useListStore();

// ALTERAÇÃO: Adicionado 'openCreateListModal' aos emits
defineEmits(['backToMain', 'openCreateListModal', 'viewList']);

onMounted(() => {
    listStore.fetchMyLists();
});
</script>