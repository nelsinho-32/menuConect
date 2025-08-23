<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl p-6 text-center">
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-red-100 mb-4">
                <svg class="h-6 w-6 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">Confirmar Exclusão</h3>
            <p class="text-gray-500 mb-6 text-sm">
                Tem certeza que deseja excluir o item "<strong>{{ itemName }}</strong>"? Esta ação não pode ser desfeita.
            </p>
            <div class="flex gap-3">
                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                <button @click="$emit('confirm')" class="w-full bg-red-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-red-700">Excluir</button>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    itemName: { type: String, required: true }
});
defineEmits(['close', 'confirm']);
</script>