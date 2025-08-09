<template>
    <div class="flex items-start gap-4 border-t py-4" :class="{'bg-indigo-50 p-4 -m-4 rounded-lg': item.isPlanned}">
        <img :src="item.imageUrl" :alt="item.dishName" class="w-16 h-16 object-cover rounded-lg">
        <div class="flex-grow">
            <div class="flex items-center gap-2">
                <span v-if="item.isPlanned" title="Parte de um Encontro Planeado">🎁</span>
                <h3 class="font-semibold text-gray-800">{{ item.dishName }}</h3>
            </div>
            
            <div v-if="hasCustomization" class="text-xs text-gray-500 mt-1 bg-white p-2 rounded-md">
                <p v-if="removedIngredients" class=" text-red-600">
                    <span class="font-semibold">Sem:</span> {{ removedIngredients }}
                </p>
                <p v-if="item.customization.notes">
                    <span class="font-semibold">Notas:</span> {{ item.customization.notes }}
                </p>
            </div>

            <p class="font-semibold text-indigo-600 mt-2 text-sm">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
        </div>

        <div class="flex flex-col items-end justify-between h-16">
            <div class="flex items-center border border-gray-300 rounded-full bg-white">
                <button @click="decreaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-l-full">-</button>
                <span class="px-3 font-semibold text-sm">{{ item.quantity }}</span>
                <button @click="increaseQuantity" class="px-3 py-1 text-gray-600 hover:bg-gray-100 rounded-r-full">+</button>
            </div>
            <div class="flex gap-4 mt-1">
                <button @click="$emit('editItem', item)" class="text-xs font-semibold text-indigo-600 hover:underline">
                    Personalizar
                </button>
                <button @click="$emit('removeFromCart', item.cartItemId)" title="Remover item do carrinho" class="text-gray-400 hover:text-red-500">
                     <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                        <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                        <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                    </svg>
                </button>
            </div>
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

const initialIngredients = computed(() => new Set((props.item.description || '').split(',').map(i => i.trim()).filter(Boolean)));
const customizedIngredients = computed(() => new Set((props.item.customization?.ingredients || '').split(',').map(i => i.trim()).filter(Boolean)));
const removedIngredients = computed(() => Array.from(initialIngredients.value).filter(i => !customizedIngredients.value.has(i)).join(', '));
const hasCustomization = computed(() => props.item.customization && (props.item.customization.notes || removedIngredients.value));
</script>