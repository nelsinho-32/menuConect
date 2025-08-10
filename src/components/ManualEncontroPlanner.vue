<template>
    <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200">
        <div v-if="!encontroStore.isPlanning">
            <h3 class="font-bold text-xl text-gray-800">Planeie o Encontro Perfeito</h3>
            <p class="text-gray-500 mt-2">Escolha a mesa, os pratos para cada convidado e a forma de pagamento. Ideal para surpreender alguém!</p>
            <button @click="encontroStore.startPlanning(restaurant)" class="mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                Começar a Planear
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
            
            <div v-if="encontroStore.plannedEncontro.step === 'dateTime'">
                <h4 class="font-bold text-lg">Passo 2: Defina a data e hora</h4>
                 <p class="text-sm text-gray-500 mb-4">Mesa selecionada: <span class="font-bold text-indigo-600">{{ encontroStore.plannedEncontro.selectedTable.id }}</span></p>
                 <div class="grid grid-cols-2 gap-4">
                     <div>
                        <label for="date" class="block text-xs font-medium text-gray-700">Data</label>
                        <input type="date" id="date" v-model="bookingDate" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm">
                    </div>
                    <div>
                        <label for="time" class="block text-xs font-medium text-gray-700">Horário</label>
                        <input type="time" id="time" v-model="bookingTime" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm sm:text-sm">
                    </div>
                 </div>
                 <button @click="confirmDateTime" class="mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Continuar</button>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'guests'">
                <h4 class="font-bold text-lg">Passo 3: Para quantas pessoas?</h4>
                <div class="flex items-center gap-4">
                    <input type="number" v-model.number="guestCount" min="1" max="10" class="w-24 p-2 border rounded-md">
                    <button @click="encontroStore.setGuests(guestCount)" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Continuar</button>
                </div>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'menu'">
                <h4 class="font-bold text-lg">Passo 4: Monte o pedido para cada convidado</h4>
                 <div class="space-y-4 mt-4 max-h-96 overflow-y-auto pr-2">
                    <div v-for="guest in encontroStore.plannedEncontro.guests" :key="guest.id" class="bg-gray-50 p-4 rounded-lg">
                        <p class="font-semibold text-gray-800">{{ guest.name }}</p>
                        <div class="grid grid-cols-2 gap-x-4 gap-y-2 mt-2 text-sm">
                            <MenuItemSelector label="Entrada" :selected-item="guest.menu.starter" @select="() => $emit('openMenuItemSelectModal', { guest, category: 'Entradas', menuItems: menuByCategory.Entradas })" @customize="() => $emit('openCustomizeModal', { guest, item: guest.menu.starter, categoryKey: 'starter' })" />
                            <MenuItemSelector label="Prato Principal" :selected-item="guest.menu.main" @select="() => $emit('openMenuItemSelectModal', { guest, category: 'Prato Principal', menuItems: menuByCategory['Prato Principal'] })" @customize="() => $emit('openCustomizeModal', { guest, item: guest.menu.main, categoryKey: 'main' })" />
                            <MenuItemSelector label="Sobremesa" :selected-item="guest.menu.dessert" @select="() => $emit('openMenuItemSelectModal', { guest, category: 'Sobremesas', menuItems: menuByCategory.Sobremesas })" @customize="() => $emit('openCustomizeModal', { guest, item: guest.menu.dessert, categoryKey: 'dessert' })" />
                            <MenuItemSelector label="Bebida" :selected-item="guest.menu.drink" @select="() => $emit('openMenuItemSelectModal', { guest, category: 'Bebidas', menuItems: menuByCategory.Bebidas })" @customize="() => $emit('openCustomizeModal', { guest, item: guest.menu.drink, categoryKey: 'drink' })" />
                        </div>
                    </div>
                </div>
                <button @click="encontroStore.plannedEncontro.step = 'payment'" class="mt-4 bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Continuar para Pagamento</button>
            </div>

            <div v-if="encontroStore.plannedEncontro.step === 'payment'">
                 <h4 class="font-bold text-lg">Passo 5: Como deseja pagar?</h4>
                 <div class="flex flex-col gap-3 mt-4">
                     <button @click="encontroStore.setPayment('agora')" class="w-full text-left p-4 rounded-lg border-2 hover:border-indigo-500 transition-colors">
                        <p class="font-bold">Pagar Agora</p>
                        <p class="text-sm text-gray-500">Adicionar tudo ao carrinho e finalizar a compra.</p>
                     </button>
                     <button @click="encontroStore.setPayment('local')" class="w-full text-left p-4 rounded-lg border-2 hover:border-indigo-500 transition-colors">
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
import MenuItemSelector from './MenuItemSelector.vue';

const props = defineProps({ restaurant: { type: Object, required: true } });
const emit = defineEmits(['confirmEncontro', 'openTableSelectModal', 'openMenuItemSelectModal', 'openCustomizeModal']);

const encontroStore = useEncontroStore();
const guestCount = ref(1);

const today = new Date();
const bookingDate = ref(today.toISOString().split('T')[0]);
const bookingTime = ref(`${String(today.getHours()).padStart(2, '0')}:${String(today.getMinutes()).padStart(2, '0')}`);

const confirmDateTime = () => {
    encontroStore.setDateTime(bookingDate.value, bookingTime.value);
};

const menuByCategory = computed(() => {
    const categorized = { 'Entradas': [], 'Prato Principal': [], 'Sobremesas': [], 'Bebidas': [], 'Novidades': [] };
    if (props.restaurant && props.restaurant.menu) {
        props.restaurant.menu.forEach(item => {
            const category = item.category || 'Novidades';
            if (categorized.hasOwnProperty(category)) {
                categorized[category].push(item);
            }
        });
    }
    return categorized;
});
</script>