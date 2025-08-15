<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-50">
        <div class="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg">
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Entrar</h2>
            <form @submit.prevent="handleSubmit">
                <div class="space-y-4">
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" v-model="form.email" id="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
                        <input type="password" v-model="form.password" id="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                </div>
                <div class="mt-6">
                    <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Entrar
                    </button>
                </div>
                 <p class="mt-4 text-center text-sm">
                    Não tem uma conta? 
                    <button type="button" @click="$emit('navigateTo', 'register')" class="font-medium text-indigo-600 hover:text-indigo-500">
                        Registe-se
                    </button>
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';

const emit = defineEmits(['login', 'navigateTo']);

const form = reactive({
    email: '',
    password: ''
});

const handleSubmit = () => {
    emit('login', { ...form });
};
</script>