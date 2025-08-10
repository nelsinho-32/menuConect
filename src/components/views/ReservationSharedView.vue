<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h1 class="text-3xl font-bold">Você foi convidado para um Encontro!</h1>
            <p class="text-gray-500">Organizado por: <span class="font-semibold">{{ encounter.organizerName }}</span></p>

            <div class="mt-6 border-t pt-4">
                <h2 class="text-xl font-bold">Detalhes da Reserva</h2>
                <p><strong>Restaurante:</strong> {{ encounter.restaurantName }}</p>
                <p><strong>Mesa:</strong> {{ encounter.selectedTable.id }}</p>
                <p><strong>Data:</strong> {{ new Date(encounter.dateTime).toLocaleString('pt-BR') }}</p>
            </div>

            <div class="mt-6 border-t pt-4">
                <h2 class="text-xl font-bold">Seu Pedido</h2>
                <p class="text-sm text-gray-500 mb-4">Você pode alterar os seus itens abaixo.</p>
                <div class="bg-gray-50 p-4 rounded-lg">
                    <div class="grid grid-cols-2 gap-x-4 gap-y-2 text-sm">
                        <MenuItemSelector 
                            label="Sua Entrada" 
                            :selected-item="myGuestInfo.menu.starter" 
                            @select="() => $emit('openMenuItemSelectModal', { guest: myGuestInfo, category: 'Entradas', menuItems: menuByCategory.Entradas })" 
                        />
                        <MenuItemSelector 
                            label="Seu Prato Principal" 
                            :selected-item="myGuestInfo.menu.main" 
                            @select="() => $emit('openMenuItemSelectModal', { guest: myGuestInfo, category: 'Prato Principal', menuItems: menuByCategory['Prato Principal'] })" 
                        />
                        <MenuItemSelector 
                            label="Sua Sobremesa" 
                            :selected-item="myGuestInfo.menu.dessert" 
                            @select="() => $emit('openMenuItemSelectModal', { guest: myGuestInfo, category: 'Sobremesas', menuItems: menuByCategory.Sobremesas })" 
                        />
                        <MenuItemSelector 
                            label="Sua Bebida" 
                            :selected-item="myGuestInfo.menu.drink" 
                            @select="() => $emit('openMenuItemSelectModal', { guest: myGuestInfo, category: 'Bebidas', menuItems: menuByCategory.Bebidas })" 
                        />
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';
import MenuItemSelector from '../MenuItemSelector.vue';

const props = defineProps({
    encounter: { type: Object, required: true },
    currentUser: { type: Object, required: true },
    restaurant: { type: Object, required: true }
});

defineEmits(['backToMain', 'openMenuItemSelectModal']);

const myGuestInfo = computed(() => {
    return props.encounter.guests.find(g => g.id === props.currentUser.id) || {};
});

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