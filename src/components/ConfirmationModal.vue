<template>
    <div @click.self="$emit('close')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl p-6 text-center">
            <div class="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-green-100 mb-4">
                <svg class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                </svg>
            </div>
            <h3 class="text-xl font-bold text-gray-800 mb-2">Reserva Confirmada!</h3>
            <p class="text-gray-500 mb-6 text-sm">{{ message }}</p>
            <button @click="$emit('close')" class="w-full bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-indigo-700 transition-colors">OK</button>
        </div>
    </div>
</template>

<script setup>
defineProps({
    message: { type: String, required: true }
});
defineEmits(['close']);
</script>