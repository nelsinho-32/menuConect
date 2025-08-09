<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Continuar a comprar</button>
        <h1 class="text-3xl font-bold mb-8">Meu Carrinho</h1>

        <div v-if="cartItems.length === 0" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">O seu carrinho está vazio.</p>
        </div>

        <div v-else class="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
            <div class="lg:col-span-2 bg-white rounded-lg shadow-md p-6 space-y-6">
                <div v-for="(group, groupName) in groupedCart" :key="groupName" class="border rounded-lg p-4">
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-bold">{{ group.restaurantName }}</h2>
                        <select v-model="group.dineOption" @change="e => $emit('updateDineOption', { restaurantId: group.restaurantId, newOption: e.target.value })" class="text-sm border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                            <option value="delivery">Delivery</option>
                            <option value="takeout">Retirada</option>
                            <option value="dine-in">Comer no Local</option>
                        </select>
                    </div>

                    <CartItem 
                        v-for="item in group.items" 
                        :key="item.cartItemId" 
                        :item="item"
                        @update-quantity="payload => $emit('updateQuantity', payload)"
                        @remove-from-cart="id => $emit('removeFromCart', id)"
                        @edit-item="item => $emit('editItem', item)"
                    />
                </div>
            </div>

            <div class="lg:col-span-1 bg-white rounded-lg shadow-md p-6 sticky top-24">
                <h2 class="text-2xl font-bold border-b pb-4">Resumo do Pedido</h2>
                <div class="space-y-2 mt-4 text-gray-600">
                    <div class="flex justify-between"><span>Subtotal</span><span>R$ {{ subtotal.toFixed(2).replace('.', ',') }}</span></div>
                    <div class="flex justify-between" :class="deliveryFee > 0 ? 'text-gray-600' : 'text-green-600'">
                        <span>Taxa de Entrega</span>
                        <span v-if="deliveryFee > 0">R$ {{ deliveryFee.toFixed(2).replace('.', ',') }}</span>
                        <span v-else>Grátis</span>
                    </div>
                    <div class="flex justify-between font-bold text-lg text-gray-800 border-t pt-2 mt-2"><span>Total</span><span>R$ {{ total.toFixed(2).replace('.', ',') }}</span></div>
                </div>
                
                <div class="mt-6 space-y-3">
                    <button @click="$emit('checkout', 'pix')" class="w-full bg-cyan-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-cyan-600 flex items-center justify-center gap-2">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M12 22h.01m-4.2-7.8-4.2 4.2m8.4-4.2 4.2 4.2M2 7.1 6.2 11m11.6-3.9 4.2-4.2M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm0 5.1V12"/></svg>
                        Pagar com Pix
                    </button>
                    <button @click="$emit('checkout')" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Finalizar Compra</button>
                </div>

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
const emit = defineEmits(['updateQuantity', 'removeFromCart', 'addToCart', 'backToMain', 'checkout', 'editItem', 'updateDineOption']);

const isAISuggesting = ref(false);
const aiSuggestion = ref(null);

const groupedCart = computed(() => {
    return props.cartItems.reduce((acc, item) => {
        const key = item.restaurantId;
        if (!acc[key]) {
            acc[key] = {
                restaurantId: item.restaurantId,
                restaurantName: item.restaurantName,
                dineOption: item.dineOption,
                items: []
            };
        }
        acc[key].items.push(item);
        return acc;
    }, {});
});

const subtotal = computed(() => {
    return props.cartItems.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

// AQUI ESTÁ A LÓGICA ATUALIZADA
const deliveryFee = computed(() => {
    const deliveryRestaurants = new Set();
    props.cartItems.forEach(item => {
        if (item.dineOption === 'delivery' || !item.dineOption) {
            deliveryRestaurants.add(item.restaurantId);
        }
    });
    return deliveryRestaurants.size * 5.00; // 5.00 por cada restaurante único com delivery
});

const total = computed(() => subtotal.value + deliveryFee.value);

async function getAISuggestion() {
    isAISuggesting.value = true;
    aiSuggestion.value = null;

    const cartContent = props.cartItems.map(item => item.dishName).join(', ');
    const availableItems = props.allDishes.filter(dish => !props.cartItems.some(cartItem => cartItem.id === dish.id));
    
    const schema = { type: "OBJECT", properties: { dishName: { type: "STRING" }, reason: { type: "STRING" } } };
    const prompt = `Com base nos itens do carrinho: '${cartContent}', sugira um acompanhamento (bebida ou sobremesa) da lista de itens disponíveis: ${JSON.stringify(availableItems)}. Forneça o nome exato do prato e uma razão curta e convincente para a sugestão.`;

    try {
        const result = await callGemini(prompt, schema);
        if (result) {
            aiSuggestion.value = result;
        }
    } catch(error) {
        console.error("Falha ao obter sugestão da IA:", error);
        // Opcional: mostrar um erro ao utilizador
    } finally {
        isAISuggesting.value = false;
    }
}

function addSuggestionToCart() {
    if (aiSuggestion.value) {
        const dishToAdd = props.allDishes.find(d => d.dishName === aiSuggestion.value.dishName);
        if (dishToAdd) {
            // Ao adicionar, assume o mesmo modo de consumo do primeiro item do carrinho
            const dineOption = props.cartItems[0]?.dineOption || 'delivery';
            emit('addToCart', { dish: dishToAdd, quantity: 1, dineOption });
            aiSuggestion.value = null;
        }
    }
}
</script>