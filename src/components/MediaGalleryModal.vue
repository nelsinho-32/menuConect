<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-[60]">
        <div class="bg-white rounded-2xl max-w-4xl w-full shadow-2xl max-h-[90vh] flex flex-col">
            <div class="p-6 border-b flex justify-between items-center">
                <h3 class="text-2xl font-bold text-gray-800">Galeria de Mídia</h3>
                <button @click="$emit('close')" class="text-gray-400 hover:text-red-500">&times;</button>
            </div>

            <div class="p-6 flex-grow overflow-y-auto">
                <div class="bg-gray-50 border-2 border-dashed rounded-lg p-4 mb-6">
                    <label for="galleryImageUpload" class="cursor-pointer text-center block text-indigo-600 font-semibold hover:text-indigo-800">
                        + Carregar Nova Imagem
                    </label>
                    <input type="file" id="galleryImageUpload" @change="handleUpload" accept="image/*" class="hidden">
                </div>

                <div v-if="mediaStore.state.isLoading" class="text-center">A carregar galeria...</div>
                <div v-else-if="mediaStore.state.items.length === 0" class="text-center text-gray-400 py-10">
                    Nenhuma imagem na galeria.
                </div>
                <div v-else class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
                    <div v-for="media in mediaStore.state.items" :key="media.id"
                        class="relative group aspect-square border-2 border-transparent hover:border-indigo-500 rounded-lg transition-all"
                        @click="$emit('imageSelected', media.image_url)">
                        
                        <img :src="media.image_url" class="w-full h-full object-cover rounded-md cursor-pointer">
                        
                        <div class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 flex items-center justify-center transition-opacity cursor-pointer">
                            <span class="text-white font-bold">Selecionar</span>
                        </div>
                        
                        <button @click.stop="handleDelete(media.id)" title="Excluir Imagem"
                            class="absolute top-1 right-1 bg-red-500 text-white rounded-full p-1 opacity-0 group-hover:opacity-100 transition-opacity">
                            <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                                <path d="M5.5 5.5A.5.5 0 0 1 6 6v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm2.5 0a.5.5 0 0 1 .5.5v6a.5.5 0 0 1-1 0V6a.5.5 0 0 1 .5-.5zm3 .5a.5.5 0 0 0-1 0v6a.5.5 0 0 0 1 0V6z"/>
                                <path fill-rule="evenodd" d="M14.5 3a1 1 0 0 1-1 1H13v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V4h-.5a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1H6a1 1 0 0 1 1-1h2a1 1 0 0 1 1 1h3.5a1 1 0 0 1 1 1v1zM4.118 4 4 4.059V13a1 1 0 0 0 1 1h6a1 1 0 0 0 1-1V4.059L11.882 4H4.118zM2.5 3V2h11v1h-11z"/>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMediaStore } from '@/stores/mediaStore';

const emit = defineEmits(['close', 'imageSelected']);
const mediaStore = useMediaStore();

onMounted(() => {
    mediaStore.fetchMedia();
});

const handleUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;
    try {
        await mediaStore.uploadMedia(file);
    } catch (error) {
        alert(`Erro: ${error}`);
    }
    event.target.value = ''; // Limpa o input para permitir o mesmo upload novamente
};

const handleDelete = async (mediaId) => {
    if (confirm("Tem a certeza que deseja excluir esta imagem permanentemente?")) {
        try {
            await mediaStore.deleteMedia(mediaId);
        } catch (error) {
            alert(`Erro: ${error}`);
        }
    }
};
</script>