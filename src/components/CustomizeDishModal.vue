<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/60 flex items-center justify-center p-4 z-[60]">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
            <div class="p-6 border-b text-center">
                <h3 class="text-2xl font-bold text-gray-800">Personalize seu Pedido</h3>
                <p class="text-gray-500">{{ dish.dishName }}</p>
            </div>

            <div class="p-6 space-y-4">
                <div>
                    <h4 class="font-semibold text-gray-700 mb-2">Ingredientes</h4>
                    <div v-if="editableIngredients.length > 0" class="space-y-2">
                        <label v-for="(ingredient, index) in editableIngredients" :key="index" class="flex items-center p-3 rounded-lg transition-colors" :class="ingredient.enabled ? 'bg-green-50' : 'bg-gray-100 text-gray-400'">
                            <input type="checkbox" v-model="ingredient.enabled" class="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500">
                            <span class="ml-3 text-sm" :class="{'line-through': !ingredient.enabled}">{{ ingredient.name }}</span>
                        </label>
                    </div>
                    <p v-else class="text-sm text-gray-400">Nenhum ingrediente listado para este prato.</p>
                </div>

                <div>
                    <label for="notes" class="block text-sm font-medium text-gray-700">Observações (opcional)</label>
                    <textarea id="notes" v-model="notes" rows="2" placeholder="Ex: Sem cebola, ponto da carne, etc." class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"></textarea>
                </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                <button @click="saveCustomization" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700">Confirmar e Adicionar</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue';

const props = defineProps({
  dish: { type: Object, required: true }
});

const emit = defineEmits(['close', 'addToCart']);

const notes = ref('');
// Transforma a string de ingredientes num array de objetos para podermos usar checkboxes
const editableIngredients = reactive(
    (props.dish.description || '')
        .split(',')
        .map(item => item.trim())
        .filter(item => item) // Remove itens vazios
        .map(name => ({ name, enabled: true }))
);

const saveCustomization = () => {
    const enabledIngredients = editableIngredients
        .filter(i => i.enabled)
        .map(i => i.name)
        .join(', ');

    const finalCustomization = {
        ingredients: enabledIngredients,
        notes: notes.value.trim()
    };

    emit('addToCart', { dish: props.dish, quantity: 1, customization: finalCustomization });
};
</script>