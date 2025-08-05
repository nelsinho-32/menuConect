<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Configurar Mesa</h3>
                <p class="text-gray-500">Altere o número e as imagens da mesa.</p>
            </div>

            <div class="p-6 space-y-6">
                <div>
                    <label for="table-id" class="block text-sm font-medium text-gray-700 mb-1">Número da Mesa</label>
                    <input type="text" id="table-id" v-model="editableTable.id" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm">
                </div>

                <div>
                    <h4 class="text-sm font-medium text-gray-700 mb-2">Imagens da Mesa</h4>
                    <div v-if="editableTable.images.length" class="grid grid-cols-3 gap-4 max-h-48 overflow-y-auto pr-2">
                        <div v-for="(image, index) in editableTable.images" :key="index" class="relative group">
                            <img :src="image" class="w-full h-24 object-cover rounded-lg border">
                            <button @click="removeImage(index)" class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
                            </button>
                        </div>
                    </div>
                     <p v-else class="text-sm text-gray-400 text-center py-4">Nenhuma imagem adicionada.</p>
                     </div>
                
                <div>
                    <label for="imageUpload" class="w-full text-sm bg-indigo-50 text-indigo-700 px-4 py-2 rounded-lg font-bold hover:bg-indigo-100 cursor-pointer text-center block">
                        + Carregar nova imagem
                    </label>
                    <input type="file" id="imageUpload" @change="handleImageUpload" accept="image/png, image/jpeg, image/webp" class="hidden">
                    </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                <button @click="save" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600">Salvar Alterações</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue';

const props = defineProps({
  table: { type: Object, required: true }
});

const emit = defineEmits(['close', 'save']);

const editableTable = reactive({ id: '', images: [], originalId: '' });

onMounted(() => {
    const tableCopy = JSON.parse(JSON.stringify(props.table));
    editableTable.id = tableCopy.id;
    editableTable.images = tableCopy.images || [];
    editableTable.originalId = tableCopy.id;
});

// INÍCIO: NOVA FUNÇÃO PARA PROCESSAR UPLOAD
const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (e) => {
        // O resultado (e.target.result) é uma string base64 que representa a imagem
        editableTable.images.push(e.target.result);
    };
    reader.readAsDataURL(file);

    // Limpa o input para permitir o upload do mesmo ficheiro novamente
    event.target.value = '';
};
// FIM: NOVA FUNÇÃO PARA PROCESSAR UPLOAD

const removeImage = (index) => {
    editableTable.images.splice(index, 1);
};

const save = () => {
    emit('save', editableTable);
    emit('close');
};
</script>