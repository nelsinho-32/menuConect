<template>
    <div class="bg-white p-6 rounded-lg shadow-lg border border-gray-200 flex flex-col">
        <h3 class="font-bold text-xl text-indigo-600">{{ suggestion.title }}</h3>
        <p class="text-sm text-gray-500 mt-2"><span class="font-semibold">Mesa Sugerida:</span> {{ suggestion.table }}</p>
        
        <div class="mt-4 border-t pt-4 flex-grow">
            <p class="font-semibold text-gray-700 mb-2">Menu Sugerido:</p>
            <div class="space-y-3 text-sm">
                <EditableMenuItem 
                    label="Entrada" 
                    :item="suggestion.menu.starter" 
                    @regenerate="newItem => regenerateItem('starter', newItem)"
                />
                <EditableMenuItem 
                    label="Prato Principal" 
                    :item="suggestion.menu.main" 
                    @regenerate="newItem => regenerateItem('main', newItem)"
                />
                <EditableMenuItem 
                    label="Sobremesa" 
                    :item="suggestion.menu.dessert" 
                    @regenerate="newItem => regenerateItem('dessert', newItem)"
                />
                 <EditableMenuItem 
                    label="Bebida" 
                    :item="suggestion.menu.drink" 
                    @regenerate="newItem => regenerateItem('drink', newItem)"
                />
            </div>
        </div>

         <div class="mt-4 bg-indigo-50 p-3 rounded-lg">
            <p class="text-sm font-semibold text-indigo-800">✨ Dica Especial:</p>
            <p class="text-sm text-indigo-700">{{ suggestion.tip }}</p>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';
import EditableMenuItem from './EditableMenuItem.vue';

const props = defineProps({
    initialSuggestion: { type: Object, required: true },
    restaurantMenu: { type: Array, required: true },
    restaurantTheme: { type: String, default: 'geral' }
});

const suggestion = reactive(JSON.parse(JSON.stringify(props.initialSuggestion)));

const regenerateItem = (itemType, newItem) => {
    if (newItem && newItem.itemName) {
        suggestion.menu[itemType] = newItem.itemName;
    }
};
</script>