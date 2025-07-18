<template>
    <div @click.self="$emit('close-modal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-xs w-full shadow-2xl p-6 text-center">
            <h3 class="text-xl font-bold text-gray-800 mb-4">{{ dish.dishName }}</h3>
            <div class="flex flex-col gap-3">
                <button @click="$emit('order-now', dish)" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 transition-colors">Pedir Agora</button>
                <button @click="$emit('add-to-cart', dish)" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Adicionar ao Carrinho</button>
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
defineEmits(['close-modal', 'add-to-cart', 'order-now']);
</script>