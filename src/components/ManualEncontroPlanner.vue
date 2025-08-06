<template>
    <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div v-if="!encontroStore.isPlanning">
            <h3 class="font-bold text-xl text-gray-800">Planeja o Encontro Perfeito</h3>
            <p class="text-gray-500 mt-2">Escolha a mesa, os pratos para cada convidado e a forma de pagamento. Ideal para surpreender alguém!</p>
            <button @click="encontroStore.startPlanning(restaurant)" class="mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                Começar a Planejar
            </button>
        </div>

        <div v-else class="relative">
            <button @click="encontroStore.cancelPlanning()" class="absolute -top-2 -right-2 text-gray-400 hover:text-red-500 text-xs">Cancelar</button>
            
            <div v-if="encontroStore.plannedEncontro.step === 'table'">
                <h4 class="font-bold text-lg">Passo 1: Escolha a sua mesa</h4>
                <p class="text-sm text-gray-500 mb-4">Clique no botão abaixo para abrir o mapa do restaurante.</p>
                <button @click="$emit('openTableSelectModal')" class="w-full bg-blue-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-blue-600">
                    Ver Mapa e Escolher Mesa
                </button>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'guests'">
                <h4 class="font-bold text-lg">Passo 2: Para quantas pessoas?</h4>
                <p class="text-sm text-gray-500 mb-4">Mesa selecionada: <span class="font-bold text-indigo-600">{{ encontroStore.plannedEncontro.selectedTable.id }}</span></p>
                <div class="flex items-center gap-4">
                    <input type="number" v-model.number="guestCount" min="1" max="10" class="w-24 p-2 border rounded-md">
                    <button @click="encontroStore.setGuests(guestCount)" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Continuar</button>
                </div>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'menu'">
                <h4 class="font-bold text-lg">Passo 3: Monte o pedido para cada convidado</h4>
                 <div class="space-y-4 mt-4 max-h-96 overflow-y-auto pr-2">
                    <div v-for="guest in encontroStore.plannedEncontro.guests" :key="guest.id" class="bg-gray-50 p-4 rounded-lg">
                        <p class="font-semibold text-gray-800">{{ guest.name }}</p>
                        <div class="grid grid-cols-2 gap-4 mt-2 text-sm">
                            <select @change="e => encontroStore.setGuestMenu(guest.id, 'starter', e.target.value)" class="p-2 border rounded-md bg-white">
                                <option value="">-- Entrada (Opcional) --</option>
                                <option v-for="item in menuByCategory.Entradas" :key="item.id">{{ item.name }}</option>
                            </select>
                             <select @change="e => encontroStore.setGuestMenu(guest.id, 'main', e.target.value)" class="p-2 border rounded-md bg-white">
                                <option value="">-- Prato Principal --</option>
                                <option v-for="item in menuByCategory['Prato Principal']" :key="item.id">{{ item.name }}</option>
                            </select>
                             <select @change="e => encontroStore.setGuestMenu(guest.id, 'dessert', e.target.value)" class="p-2 border rounded-md bg-white">
                                <option value="">-- Sobremesa (Opcional) --</option>
                                <option v-for="item in menuByCategory.Sobremesas" :key="item.id">{{ item.name }}</option>
                            </select>
                             <select @change="e => encontroStore.setGuestMenu(guest.id, 'drink', e.target.value)" class="p-2 border rounded-md bg-white">
                                <option value="">-- Bebida --</option>
                                <option v-for="item in menuByCategory.Bebidas" :key="item.id">{{ item.name }}</option>
                            </select>
                        </div>
                    </div>
                </div>
                <button @click="encontroStore.plannedEncontro.step = 'payment'" class="mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Continuar para Pagamento</button>
            </div>

             <div v-if="encontroStore.plannedEncontro.step === 'payment'">
                 <h4 class="font-bold text-lg">Passo 4: Como deseja pagar?</h4>
                 <div class="flex flex-col gap-3 mt-4">
                     <button @click="encontroStore.setPayment('agora')" class="w-full text-left p-4 rounded-lg border-2 hover:border-indigo-500">
                        <p class="font-bold">Pagar Agora</p>
                        <p class="text-sm text-gray-500">Adicionar tudo ao carrinho e finalizar a compra.</p>
                     </button>
                     <button @click="encontroStore.setPayment('local')" class="w-full text-left p-4 rounded-lg border-2 hover:border-indigo-500">
                        <p class="font-bold">Pagar no Local</p>
                        <p class="text-sm text-gray-500">Apenas confirmar a reserva e o pré-pedido.</p>
                     </button>
                 </div>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'confirm'">
                <h4 class="font-bold text-lg text-green-600">Encontro Planeado!</h4>
                <p class="mt-2">Reserva para a mesa <span class="font-bold">{{ encontroStore.plannedEncontro.selectedTable.id }}</span> com pré-pedido para <span class="font-bold">{{ encontroStore.plannedEncontro.guests.length }}</span> pessoa(s).</p>
                <p class="mt-1">Pagamento selecionado: <span class="font-bold">{{ encontroStore.plannedEncontro.paymentOption === 'local' ? 'No Local' : 'Pagar Agora' }}</span>.</p>
                <button @click="$emit('confirmEncontro', encontroStore.plannedEncontro)" class="mt-4 bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">
                    Confirmar e Reservar
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useEncontroStore } from '@/stores/encontroStore';

const props = defineProps({
    restaurant: { type: Object, required: true }
});
const emit = defineEmits(['confirmEncontro', 'openTableSelectModal']);

const encontroStore = useEncontroStore();   
const guestCount = ref(1);

const menuByCategory = computed(() => {
    const categorized = { 'Entradas': [], 'Prato Principal': [], 'Sobremesas': [], 'Bebidas': [] };
    if (props.restaurant && props.restaurant.menu) {
        props.restaurant.menu.forEach(item => {
            if(categorized[item.category]) {
                categorized[item.category].push(item);
            }
        });
    }
    return categorized;
});
</script>