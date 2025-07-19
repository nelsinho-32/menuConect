<template>
    <div class="flex items-center gap-4 border-b pb-4">
        <img :src="item.imageUrl" :alt="item.dishName" class="w-24 h-24 object-cover rounded-lg">
        <div class="flex-grow">
            <h3 class="font-bold text-lg">{{ item.dishName }}</h3>
            <p class="text-sm text-gray-500">{{ item.restaurantName }}</p>
            <p class="font-semibold text-indigo-600 mt-1">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
        </div>
        <div class="flex flex-col items-end gap-2">
            <!-- Controlo de Quantidade -->
            <div class="flex items-center border border-gray-300 rounded-full">
                <button @click="decreaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-l-full">-</button>
                <span class="px-3 font-semibold">{{ item.quantity }}</span>
                <button @click="increaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-r-full">+</button>
            </div>
            <!-- Botão de Remover -->
            <button @click="$emit('removeFromCart', item.id)" class="text-xs text-red-500 hover:underline">Remover</button>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    item: { type: Object, required: true }
});
const emit = defineEmits(['updateQuantity', 'removeFromCart']);

const increaseQuantity = () => {
    emit('updateQuantity', { dishId: props.item.id, quantity: props.item.quantity + 1 });
};

const decreaseQuantity = () => {
    emit('updateQuantity', { dishId: props.item.id, quantity: props.item.quantity - 1 });
};
</script>