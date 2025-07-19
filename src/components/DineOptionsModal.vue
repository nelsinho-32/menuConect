<template>
    <div @click.self="$emit('closeModal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-xs w-full shadow-2xl p-6 text-center relative">
            <button @click="$emit('closeModal')" class="absolute top-4 right-4 text-gray-400 hover:text-gray-600">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>

            <h3 class="text-xl font-bold text-gray-800 mb-2">Como prefere?</h3>
            <p class="text-gray-500 mb-6 text-sm">Escolha uma opção para {{ dish.dishName }}</p>

            <div class="flex flex-col gap-3">
                <button @click="$emit('dineIn', dish)" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors">Comer no Local</button>
                <button @click="$emit('takeout', dish)" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors">Para Retirada</button>
                <button @click="$emit('reserve', dish)" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Reservar uma Mesa</button>
            </div>
        </div>
    </div>
</template>
<script setup>
defineProps({
  dish: {
    type: Object,
    required: true
  }
});
defineEmits(['closeModal', 'dineIn', 'takeout', 'reserve']);
</script>