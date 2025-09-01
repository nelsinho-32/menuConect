<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Criar Nova Lista</h3>
            </div>
            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
                <div>
                    <label for="list-name" class="block text-sm font-medium text-gray-700">Nome da Lista</label>
                    <input type="text" id="list-name" v-model="form.name" required class="mt-1 block w-full rounded-md border-gray-300">
                </div>
                <div>
                    <label for="list-desc" class="block text-sm font-medium text-gray-700">Descrição (Opcional)</label>
                    <textarea id="list-desc" v-model="form.description" rows="3" class="mt-1 block w-full rounded-md border-gray-300"></textarea>
                </div>
                <div class="pt-4 flex gap-3">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Criar</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
const emit = defineEmits(['close', 'create']);
const form = reactive({ name: '', description: '' });
const handleSubmit = () => {
    emit('create', { ...form });
};
</script>