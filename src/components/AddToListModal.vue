<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Adicionar a uma Lista</h3>
                <p class="text-gray-500 text-sm">A adicionar: <span class="font-semibold">{{ itemToAdd.name || itemToAdd.dishName }}</span></p>
            </div>
            <div class="p-4 max-h-60 overflow-y-auto">
                <div v-if="listStore.state.isLoading">A carregar listas...</div>
                <div v-else-if="listStore.state.myLists.length === 0" class="text-center text-gray-400 py-4">
                    <p>Nenhuma lista encontrada.</p>
                    <button @click="$emit('createList')" class="text-indigo-600 font-semibold mt-2">Criar uma agora</button>
                </div>
                <ul v-else class="space-y-2">
                    <li v-for="list in listStore.state.myLists" :key="list.id" 
                        @click="$emit('selectList', list.id)"
                        class="p-3 rounded-lg hover:bg-indigo-50 cursor-pointer transition-colors">
                        {{ list.name }}
                    </li>
                </ul>
            </div>
             <div class="p-4 bg-gray-100 border-t flex justify-end">
                <button @click="$emit('close')" class="bg-gray-200 text-gray-700 font-bold py-2 px-6 rounded-lg hover:bg-gray-300">Cancelar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { useListStore } from '@/stores/listStore';
const listStore = useListStore();
defineProps({
    itemToAdd: { type: Object, required: true }
});
defineEmits(['close', 'selectList', 'createList']);
</script>