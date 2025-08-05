<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Adicionar Novo Prato</h3>
                <p class="text-gray-500">Preencha os dados do novo item do cardápio.</p>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
                <div>
                    <label for="dishName" class="block text-sm font-medium text-gray-700">Nome do Prato</label>
                    <input type="text" id="dishName" v-model="newDish.dishName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label for="restaurantName" class="block text-sm font-medium text-gray-700">Restaurante</label>
                        <select id="restaurantName" v-model="newDish.restaurantName" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                            <option disabled value="">Selecione um restaurante</option>
                            <option v-for="restaurant in restaurants" :key="restaurant.id" :value="restaurant.name">
                                {{ restaurant.name }}
                            </option>
                        </select>
                    </div>
                    <div>
                        <label for="price" class="block text-sm font-medium text-gray-700">Preço</label>
                        <input type="number" step="0.01" id="price" v-model="newDish.price" required placeholder="Ex: 25.50" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                </div>
                
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Imagem do Prato</label>
                    <div class="w-full h-40 border-2 border-dashed rounded-lg flex items-center justify-center text-center p-2">
                        <img v-if="newDish.imageUrl" :src="newDish.imageUrl" class="max-h-full max-w-full object-contain">
                        <div v-else>
                            <p class="text-gray-500">Arraste uma imagem ou</p>
                            <label for="dishImageUpload" class="text-indigo-600 font-semibold cursor-pointer hover:underline">carregue um ficheiro</label>
                            <input type="file" id="dishImageUpload" @change="handleImageUpload" accept="image/*" class="hidden">
                        </div>
                    </div>
                </div>

                <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3 -m-6 mt-6 pt-6">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Adicionar Prato</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive } from 'vue';

const props = defineProps({
    restaurants: { type: Array, required: true }
});

const emit = defineEmits(['close', 'addDish']);

const newDish = reactive({
    dishName: '',
    restaurantName: '',
    price: '',
    imageUrl: '',
});

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        newDish.imageUrl = e.target.result;
    };
    reader.readAsDataURL(file);
};

const handleSubmit = () => {
    emit('addDish', { ...newDish });
};
</script>