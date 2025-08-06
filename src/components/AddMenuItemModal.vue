<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Adicionar Item ao Cardápio</h3>
                <p class="text-gray-500">Novo item para a categoria: <span class="font-semibold text-indigo-600">{{ category }}</span></p>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
                <div>
                    <label for="name" class="block text-sm font-medium text-gray-700">Nome do Prato</label>
                    <input type="text" id="name" v-model="newItem.name" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>
                <div>
                    <label for="description" class="block text-sm font-medium text-gray-700">Descrição / Ingredientes</label>
                    <textarea id="description" v-model="newItem.description" required rows="3" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"></textarea>
                </div>
                 <div>
                    <label for="price" class="block text-sm font-medium text-gray-700">Preço</label>
                    <input type="number" step="0.01" id="price" v-model="newItem.price" required placeholder="Ex: 35.00" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Imagem do Prato</label>
                    <div class="w-full h-40 border-2 border-dashed rounded-lg flex items-center justify-center text-center p-2">
                        <img v-if="newItem.imageUrl" :src="newItem.imageUrl" class="max-h-full max-w-full object-contain">
                        <div v-else>
                            <p class="text-gray-500">Arraste uma imagem ou</p>
                            <label for="itemImageUpload" class="text-indigo-600 font-semibold cursor-pointer hover:underline">carregue um ficheiro</label>
                            <input type="file" id="itemImageUpload" @change="handleImageUpload" accept="image/*" class="hidden">
                        </div>
                    </div>
                </div>

                <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3 -m-6 mt-6 pt-6">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Adicionar Item</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';

const props = defineProps({
    category: { type: String, required: true }
});

const emit = defineEmits(['close', 'addMenuItem']);

const newItem = reactive({
    name: '',
    description: '',
    price: '',
    imageUrl: '',
});

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        newItem.imageUrl = e.target.result;
    };
    reader.readAsDataURL(file);
};

const handleSubmit = () => {
    // Adiciona a categoria ao objeto antes de o enviar
    const itemData = { ...newItem, category: props.category };
    emit('addMenuItem', itemData);
};
</script>