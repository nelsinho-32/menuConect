<template>
    <div class="flex items-start gap-4 border-b pb-4">
        <img :src="item.imageUrl" :alt="item.dishName" class="w-24 h-24 object-cover rounded-lg">
        <div class="flex-grow">
            <h3 class="font-bold text-lg">{{ item.dishName }}</h3>
            
            <div v-if="hasCustomization" class="text-xs text-gray-500 mt-1 bg-gray-50 p-2 rounded-md">
                <p v-if="removedIngredients" class=" text-red-600">
                    <span class="font-semibold">Sem:</span> {{ removedIngredients }}
                </p>
                <p v-if="item.customization.notes">
                    <span class="font-semibold">Notas:</span> {{ item.customization.notes }}
                </p>
            </div>

            <p class="font-semibold text-indigo-600 mt-2">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
            
            <div class="mt-2">
                <button @click="$emit('editItem', item)" class="text-xs font-semibold text-indigo-600 hover:underline">
                    Personalizar
                </button>
            </div>
        </div>

        <div class="flex flex-col items-end justify-between h-24">
            <div class="flex items-center border border-gray-300 rounded-full">
                <button @click="decreaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-l-full">-</button>
                <span class="px-3 font-semibold">{{ item.quantity }}</span>
                <button @click="increaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-r-full">+</button>
            </div>
            <button @click="$emit('removeFromCart', item.cartItemId)" title="Remover item do carrinho" class="text-gray-400 hover:text-red-500">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                    <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    item: { type: Object, required: true }
});
const emit = defineEmits(['updateQuantity', 'removeFromCart', 'editItem']);

const increaseQuantity = () => {
    emit('updateQuantity', { cartItemId: props.item.cartItemId, quantity: props.item.quantity + 1 });
};

const decreaseQuantity = () => {
    emit('updateQuantity', { cartItemId: props.item.cartItemId, quantity: props.item.quantity - 1 });
};

const initialIngredients = computed(() => {
    // A descrição original do prato, que contém todos os ingredientes
    return new Set((props.item.description || '').split(',').map(i => i.trim()).filter(Boolean));
});

const customizedIngredients = computed(() => {
    // Os ingredientes que o utilizador deixou (após desmarcar alguns)
    return new Set((props.item.customization?.ingredients || '').split(',').map(i => i.trim()).filter(Boolean));
});

const removedIngredients = computed(() => {
    if (!props.item.customization) return '';
    // Filtra para encontrar quais ingredientes do original não estão na lista customizada
    return Array.from(initialIngredients.value).filter(i => !customizedIngredients.value.has(i)).join(', ');
});

const hasCustomization = computed(() => {
    return props.item.customization && (props.item.customization.notes || removedIngredients.value);
});
</script>