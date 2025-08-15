<template>
    <div class="flex items-center justify-center min-h-screen bg-gray-50">
        <div class="max-w-md w-full bg-white p-8 rounded-2xl shadow-lg">
            <h2 class="text-3xl font-bold text-center text-gray-800 mb-6">Criar Conta</h2>
            <form @submit.prevent="handleSubmit">
                <div class="space-y-4">
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700">Nome Completo</label>
                        <input type="text" v-model="form.name" id="name" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                    <div>
                        <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
                        <input type="email" v-model="form.email" id="email" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                    <div>
                        <label for="password" class="block text-sm font-medium text-gray-700">Senha</label>
                        <input type="password" v-model="form.password" id="password" required class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                     <div>
                        <label for="phone" class="block text-sm font-medium text-gray-700">Telefone</label>
                        <input type="tel" v-model="form.phone" id="phone" placeholder="(XX) XXXXX-XXXX" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                    </div>
                    <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
                        <div class="sm:col-span-2">
                            <label for="city" class="block text-sm font-medium text-gray-700">Cidade</label>
                            <input type="text" v-model="form.city" id="city" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        </div>
                        <div>
                            <label for="uf" class="block text-sm font-medium text-gray-700">UF</label>
                            <input type="text" v-model="form.uf" id="uf" maxlength="2" class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500">
                        </div>
                    </div>
                     <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Tipo de Conta</label>
                        <div class="flex gap-4">
                            <label class="flex items-center">
                                <input type="radio" v-model="form.role" value="cliente" class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300">
                                <span class="ml-2 text-sm text-gray-700">Cliente</span>
                            </label>
                            <label class="flex items-center">
                                <input type="radio" v-model="form.role" value="empresa" class="focus:ring-indigo-500 h-4 w-4 text-indigo-600 border-gray-300">
                                <span class="ml-2 text-sm text-gray-700">Empresa</span>
                            </label>
                        </div>
                    </div>
                </div>
                <div class="mt-6">
                    <button type="submit" class="w-full flex justify-center py-3 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                        Registar
                    </button>
                </div>
                <p class="mt-4 text-center text-sm">
                    Já tem uma conta? 
                    <button type="button" @click="$emit('navigateTo', 'login')" class="font-medium text-indigo-600 hover:text-indigo-500">
                        Faça login
                    </button>
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';

const emit = defineEmits(['register', 'navigateTo']);

const form = reactive({
    name: '',
    email: '',
    password: '',
    role: 'cliente',
    phone: '', // NOVO
    city: '',  // NOVO
    uf: ''     // NOVO
});

const handleSubmit = () => {
    emit('register', { ...form });
};
</script>