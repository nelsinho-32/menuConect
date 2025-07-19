<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Continuar a comprar</button>
        <h1 class="text-3xl font-bold mb-8">Meu Carrinho</h1>

        <div v-if="cartItems.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">O seu carrinho está vazio.</p>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            <!-- Coluna de Itens -->
            <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-6 space-y-4">
                <CartItem 
                    v-for="item in cartItems" 
                    :key="item.id" 
                    :item="item"
                    @update-quantity="payload => $emit('updateQuantity', payload)"
                    @remove-from-cart="id => $emit('removeFromCart', id)"
                />
            </div>

            <!-- Coluna de Resumo -->
            <div class="lg:col-span-1 bg-white rounded-lg shadow-md p-6 sticky top-24">
                <h2 class="text-2xl font-bold border-b pb-4">Resumo do Pedido</h2>
                <div class="space-y-2 mt-4 text-gray-600">
                    <div class="flex justify-between"><span>Subtotal</span><span>R$ {{ subtotal.toFixed(2).replace('.', ',') }}</span></div>
                    <div class="flex justify-between"><span>Taxa de Entrega</span><span>R$ 5,00</span></div>
                    <div class="flex justify-between font-bold text-lg text-gray-800 border-t pt-2 mt-2"><span>Total</span><span>R$ {{ (subtotal + 5).toFixed(2).replace('.', ',') }}</span></div>
                </div>
                
                <div class="mt-6 space-y-3">
                    <button @click="$emit('checkout', 'pix')" class="w-full bg-cyan-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-cyan-600 transition-colors flex items-center justify-center gap-2">
                        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22h.01"/><path d="m7.1 12.2-4.2 4.2"/><path d="m16.9 12.2 4.2 4.2"/><path d="M2 7.1 6.2 11"/><path d="m17.8 11 4.2-4.2"/><path d="M12 2a10 10 0 1 0 10 10"/><path d="M12 7.1V12"/></svg>
                        Pagar com Pix
                    </button>
                    <button @click="$emit('checkout')" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Finalizar Compra</button>
                </div>

                <!-- IA: Sugestão de Acompanhamento -->
                <div class="mt-6 border-t pt-4">
                    <p class="font-semibold text-gray-700 mb-2">Que tal adicionar um acompanhamento?</p>
                    <button @click="getAISuggestion" class="w-full bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg font-bold hover:bg-indigo-100 text-sm" :disabled="isAISuggesting">
                        <span v-if="!isAISuggesting">✨ Sugerir com IA</span>
                        <span v-else>A pensar...</span>
                    </button>
                    <div v-if="aiSuggestion" class="mt-4 bg-indigo-100 p-3 rounded-lg">
                        <p class="text-sm font-semibold text-indigo-800">{{ aiSuggestion.dishName }}</p>
                        <p class="text-xs text-indigo-700 mt-1">{{ aiSuggestion.reason }}</p>
                        <button @click="addSuggestionToCart" class="text-xs font-bold text-indigo-600 hover:underline mt-2">Adicionar</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import CartItem from './CartItem.vue';
import { callGemini } from '../services/geminiService';

const props = defineProps({
    cartItems: { type: Array, required: true },
    allDishes: { type: Array, required: true }
});
const emit = defineEmits(['updateQuantity', 'removeFromCart', 'addToCart', 'backToMain', 'checkout']);

const isAISuggesting = ref(false);
const aiSuggestion = ref(null);

const subtotal = computed(() => {
    return props.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

async function getAISuggestion() {
    isAISuggesting.value = true;
    aiSuggestion.value = null;

    const cartContent = props.cartItems.map(item => item.dishName).join(', ');
    const availableItems = props.allDishes.filter(dish => !props.cartItems.some(cartItem => cartItem.id === dish.id));
    
    const schema = { type: "OBJECT", properties: { dishName: { type: "STRING" }, reason: { type: "STRING" } } };
    const prompt = `Com base nos itens do carrinho: '${cartContent}', sugira um acompanhamento (bebida ou sobremesa) da lista de itens disponíveis: ${JSON.stringify(availableItems)}. Forneça o nome exato do prato e uma razão curta e convincente para a sugestão.`;

    const result = await callGemini(prompt, schema);
    if (result) {
        aiSuggestion.value = result;
    }
    isAISuggesting.value = false;
}

function addSuggestionToCart() {
    if (aiSuggestion.value) {
        const dishToAdd = props.allDishes.find(d => d.dishName === aiSuggestion.value.dishName);
        if (dishToAdd) {
            emit('addToCart', dishToAdd);
            aiSuggestion.value = null;
        }
    }
}
</script>