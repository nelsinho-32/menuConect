<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <h1 class="text-3xl font-bold mb-8">Encontrar Pessoas</h1>

        <div v-if="usersStore.state.isLoading" class="text-center">A carregar...</div>
        <div v-else-if="usersStore.state.error" class="text-center text-red-500">{{ usersStore.state.error }}</div>
        
        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            <div v-for="user in usersStore.state.usersList" :key="user.id" 
                 @click="$emit('viewProfile', user.id)"
                 class="bg-white p-4 rounded-lg shadow-md flex items-center gap-4 cursor-pointer hover:shadow-xl transition-shadow">
                <img :src="user.avatarUrl || 'https://placehold.co/256x256/cccccc/ffffff?text=?'" 
                     alt="Avatar do usuário" 
                     class="w-16 h-16 rounded-full object-cover">
                <div>
                    <h3 class="font-bold text-gray-800">{{ user.name }}</h3>
                    <p class="text-sm text-gray-500">{{ user.city }}, {{ user.uf }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useUsersStore } from '@/stores/usersStore';

const usersStore = useUsersStore();

defineEmits(['viewProfile']);

onMounted(() => {
    usersStore.fetchAllUsers();
});
</script>