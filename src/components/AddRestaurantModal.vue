<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-2xl w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Adicionar Novo Restaurante</h3>
                <p class="text-gray-500">Preencha os dados do novo estabelecimento.</p>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-4 max-h-[80vh] overflow-y-auto">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label for="name" class="block text-sm font-medium text-gray-700">Nome do Restaurante</label>
                        <input type="text" id="name" v-model="newRestaurant.name" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                    <div>
                        <label for="cuisine" class="block text-sm font-medium text-gray-700">Tipo de Cozinha</label>
                        <input type="text" id="cuisine" v-model="newRestaurant.cuisine" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 pt-4">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Imagem Principal</label>
                        <div class="w-full h-40 border-2 border-dashed rounded-lg flex items-center justify-center text-center p-2" :class="{'border-indigo-400': isDraggingMain}">
                            <img v-if="newRestaurant.imageUrl" :src="newRestaurant.imageUrl" class="max-h-full max-w-full object-contain">
                            <div v-else>
                                <p class="text-gray-500">Arraste uma imagem ou</p>
                                <label for="mainImageUpload" class="text-indigo-600 font-semibold cursor-pointer hover:underline">carregue um ficheiro</label>
                                <input type="file" id="mainImageUpload" @change="handleImageUpload($event, 'main')" accept="image/*" class="hidden">
                            </div>
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Logótipo</label>
                        <div class="w-full h-40 border-2 border-dashed rounded-lg flex items-center justify-center text-center p-2">
                            <img v-if="newRestaurant.logoUrl" :src="newRestaurant.logoUrl" class="max-h-full max-w-full object-contain">
                            <div v-else>
                                <p class="text-gray-500">Arraste um logótipo ou</p>
                                <label for="logoUpload" class="text-indigo-600 font-semibold cursor-pointer hover:underline">carregue um ficheiro</label>
                                <input type="file" id="logoUpload" @change="handleImageUpload($event, 'logo')" accept="image/*" class="hidden">
                            </div>
                        </div>
                    </div>
                </div>

                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Imagens da Galeria (para o carrossel)</label>
                    <div class="w-full min-h-[10rem] border-2 border-dashed rounded-lg p-4">
                        <div v-if="newRestaurant.galleryUrls.length" class="grid grid-cols-3 md:grid-cols-5 gap-4">
                             <div v-for="(image, index) in newRestaurant.galleryUrls" :key="index" class="relative group">
                                <img :src="image" class="w-full h-24 object-cover rounded-lg border">
                                <button @click="removeGalleryImage(index)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                                </button>
                            </div>
                        </div>
                         <div v-else class="text-center py-8">
                            <p class="text-gray-500">Arraste imagens ou</p>
                            <label for="galleryUpload" class="text-indigo-600 font-semibold cursor-pointer hover:underline">carregue ficheiros</label>
                         </div>
                        <input type="file" id="galleryUpload" @change="handleImageUpload($event, 'gallery')" accept="image/*" multiple class="hidden">
                    </div>
                    <div>
                        <label for="lat" class="block text-sm font-medium text-gray-700">Latitude</label>
                        <input type="text" id="lat" v-model="newRestaurant.location.lat" required placeholder="-7.123456" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                    <div>
                        <label for="lng" class="block text-sm font-medium text-gray-700">Longitude</label>
                        <input type="text" id="lng" v-model="newRestaurant.location.lng" required placeholder="-34.123456" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    </div>
                    <label for="city" class="block text-sm font-medium text-gray-700">Cidade (Ex: João Pessoa, PB)</label>
                    <input type="text" id="city" v-model="newRestaurant.city" required class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                </div>

                <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3 -m-6 mt-6 pt-6">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Adicionar Restaurante</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const emit = defineEmits(['close', 'addRestaurant']);

const isDraggingMain = ref(false);

const newRestaurant = reactive({
    name: '',
    cuisine: '',
     location: { lat: '', lng: '' },
    imageUrl: '',
    logoUrl: '',
    galleryUrls: [],
});

const handleImageUpload = (event, type) => {
    const files = event.target.files;
    if (!files) return;

    if (type === 'gallery') {
        [...files].forEach(file => {
            const reader = new FileReader();
            reader.onload = (e) => newRestaurant.galleryUrls.push(e.target.result);
            reader.readAsDataURL(file);
        });
    } else {
        const file = files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            if (type === 'main') newRestaurant.imageUrl = e.target.result;
            if (type === 'logo') newRestaurant.logoUrl = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

const removeGalleryImage = (index) => {
    newRestaurant.galleryUrls.splice(index, 1);
};

const handleSubmit = () => {
    emit('addRestaurant', { ...newRestaurant });
};
</script>