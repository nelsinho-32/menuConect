<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-5xl w-full shadow-2xl relative max-h-[90vh] flex flex-col">
            <div class="p-6 border-b text-center">
                <h3 class="text-2xl font-bold text-gray-800">Adicionar Pedido à Mesa {{ session.table_id }}</h3>
                <p class="text-gray-500">Restaurante: {{ restaurant.name }}</p>
            </div>

            <div class="flex-grow grid grid-cols-1 md:grid-cols-2 overflow-hidden">
                <div class="p-6 border-r overflow-y-auto">
                    <div v-for="category in Object.keys(categorizedMenu)" :key="category" class="mb-4">
                        <h4 class="font-bold text-indigo-600 border-b pb-1 mb-2">{{ category }}</h4>
                        <div class="space-y-2">
                            <div v-for="item in categorizedMenu[category]" :key="item.id" @click="addItemToOrder(item)" class="p-2 rounded-lg hover:bg-gray-100 cursor-pointer flex justify-between items-center">
                                <span>{{ item.dishName }}</span>
                                <span class="font-semibold text-sm text-gray-600">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</span>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="p-6 bg-gray-50 flex flex-col">
                    <h3 class="text-xl font-bold mb-4">Comanda da Mesa</h3>
                    <div class="flex border-b mb-4">
                        <button v-for="(guest, index) in guests" :key="guest.id || index" @click="activeGuestId = guest.id || index"
                                :class="['py-2 px-4 font-semibold', activeGuestId === (guest.id || index) ? 'border-b-2 border-indigo-600 text-indigo-600' : 'text-gray-500 hover:text-gray-700']">
                            {{ guest.name }}
                        </button>
                    </div>

                    <div class="flex-grow space-y-3 overflow-y-auto pr-2">
                        <p v-if="activeGuestOrder.length === 0" class="text-center text-gray-400 mt-10">Selecione um item do cardápio para {{ activeGuestName }}.</p>
                        <div v-for="item in activeGuestOrder" :key="item.uniqueId" class="bg-white p-2 rounded-md shadow-sm">
                            <div class="flex items-center justify-between">
                                <div>
                                    <p class="font-semibold">{{ item.dishName }}</p>
                                    <p class="text-sm text-gray-500">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
                                </div>
                                <div class="flex items-center gap-2">
                                    <button @click="$emit('customizeItem', item)" title="Personalizar" class="p-1 rounded-full hover:bg-gray-200">
                                        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311a1.464 1.464 0 0 1-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705-1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c-1.4-.413-1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/></svg>
                                    </button>
                                    <button @click="removeItem(item.uniqueId)" class="w-6 h-6 rounded-full bg-red-100 text-red-600 hover:bg-red-200 font-bold">-</button>
                                </div>
                            </div>
                            <div v-if="item.customization" class="text-xs mt-1 pl-1 border-l-2 border-indigo-200">
                                <p v-if="item.customization.removedIngredients?.length" class="text-red-500">Sem: {{ item.customization.removedIngredients.join(', ') }}</p>
                                <p v-if="item.customization.notes" class="text-gray-500">Nota: {{ item.customization.notes }}</p>
                            </div>
                        </div>
                    </div>
                    <div class="border-t pt-4 mt-4">
                        <div class="flex justify-between font-bold text-xl">
                            <span>Total da Comanda:</span>
                            <span>R$ {{ totalOrder.toFixed(2).replace('.', ',') }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="p-4 bg-gray-100 border-t flex justify-end gap-3">
                <button @click="$emit('close')" class="bg-white border border-gray-300 text-gray-700 font-bold py-2 px-6 rounded-lg hover:bg-gray-50">Cancelar</button>
                <button @click="handleSubmit" :disabled="totalOrder === 0" class="bg-green-500 text-white font-bold py-2 px-6 rounded-lg hover:bg-green-600 disabled:bg-gray-300">Confirmar Pedido</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const props = defineProps({
    restaurant: { type: Object, required: true },
    session: { type: Object, required: true }
});
const emit = defineEmits(['close', 'confirmOrder', 'customizeItem']);

const guests = ref([]);
const activeGuestId = ref(null);
const fullOrder = ref([]); // Guarda todos os itens de todos os convidados

onMounted(() => {
    // Se a sessão tem nomes, usa-os. Senão, cria "Pessoa 1", "Pessoa 2", etc.
    if (props.session.customer_names?.length > 0) {
        guests.value = props.session.customer_names.map((name, index) => ({ id: index, name }));
    } else {
        guests.value = Array.from({ length: props.session.guests }, (_, i) => ({ id: i, name: `Pessoa ${i + 1}` }));
    }
    if (guests.value.length > 0) {
        activeGuestId.value = guests.value[0].id;
    }
});

// A LÓGICA QUE FALTAVA PARA PROCESSAR O CARDÁPIO
const categorizedMenu = computed(() => {
    if (!props.restaurant.menu) return {};
    return props.restaurant.menu.reduce((acc, item) => {
        const category = item.category || 'Outros';
        if (!acc[category]) {
            acc[category] = [];
        }
        acc[category].push(item);
        return acc;
    }, {});
});

const activeGuestName = computed(() => guests.value.find(g => g.id === activeGuestId.value)?.name || '');
const activeGuestOrder = computed(() => fullOrder.value.filter(item => item.guestId === activeGuestId.value));
const totalOrder = computed(() => fullOrder.value.reduce((sum, item) => sum + parseFloat(item.price), 0));

const addItemToOrder = (dish) => {
    // Para simplificar, cada clique adiciona um item, mesmo que repetido.
    // A gestão de quantidade foi removida para alinhar com o design de "comanda".
    const newItem = {
        ...dish,
        guestId: activeGuestId.value,
        uniqueId: Date.now() + Math.random() // ID único para cada item na comanda
    };
    fullOrder.value.push(newItem);
};

const removeItem = (uniqueId) => {
    fullOrder.value = fullOrder.value.filter(item => item.uniqueId !== uniqueId);
};

const handleSubmit = () => {
    // Agrupa os itens para enviar para a API (ex: 2x Hamburguer)
    const finalOrder = fullOrder.value.reduce((acc, item) => {
        const existing = acc.find(i => i.id === item.id && JSON.stringify(i.customization) === JSON.stringify(item.customization));
        if (existing) {
            existing.quantity++;
        } else {
            acc.push({ ...item, quantity: 1 });
        }
        return acc;
    }, []);
    emit('confirmOrder', finalOrder);
};

// Esta função é chamada pelo App.vue para atualizar um item
const updateOrderItem = (updatedItem) => {
    const index = fullOrder.value.findIndex(item => item.uniqueId === updatedItem.uniqueId);
    if (index !== -1) {
        fullOrder.value[index] = updatedItem;
    }
};
// Expõe a função para ser chamada pelo componente pai
defineExpose({ updateOrderItem });
</script>