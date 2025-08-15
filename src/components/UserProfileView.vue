<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        
        <div class="bg-white rounded-2xl shadow-lg p-8 max-w-2xl mx-auto">
            <div class="flex flex-col sm:flex-row items-center gap-6">
                <div class="relative group">
                    <img :src="editableUser.avatarUrl || 'https://placehold.co/256x256/cccccc/ffffff?text=?'" class="w-32 h-32 rounded-full ring-4 ring-indigo-100 object-cover">
                    <label v-if="isEditing" for="avatarUpload" class="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center text-white cursor-pointer opacity-0 group-hover:opacity-100 transition-opacity">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" viewBox="0 0 16 16"><path d="M15 12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h1.172a3 3 0 0 0 2.12-.879l.83-.828A1 1 0 0 1 6.827 3h2.344a1 1 0 0 1 .707.293l.828.828A3 3 0 0 0 12.828 5H14a1 1 0 0 1 1 1v6zM2 4a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2h-1.172a2 2 0 0 1-1.414-.586l-.828-.828A2 2 0 0 0 9.172 2H6.828a2 2 0 0 0-1.414.586l-.828-.828A2 2 0 0 1 3.172 4H2z"/><path d="M8 11a2.5 2.5 0 1 1 0-5 2.5 2.5 0 0 1 0 5zm0 1a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7zM3 6.5a.5.5 0 1 1-1 0 .5.5 0 0 1 1 0z"/></svg>
                        <span class="ml-2 text-sm">Alterar</span>
                    </label>
                    <input type="file" id="avatarUpload" @change="handleAvatarUpload" accept="image/*" class="hidden">
                </div>
                <div class="text-center sm:text-left flex-grow">
                    <h1 v-if="!isEditing" class="text-3xl font-bold text-gray-800">{{ editableUser.name }}</h1>
                    <input v-else type="text" v-model="editableUser.name" class="text-3xl font-bold text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 w-full">
                    
                    <p v-if="!isEditing" class="text-gray-500">{{ editableUser.email }}</p>
                    <input v-else type="email" v-model="editableUser.email" class="text-gray-500 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 mt-1 w-full">
                </div>
            </div>

            <div class="border-t my-8"></div>

            <div>
                <h2 class="text-xl font-bold text-gray-700 mb-4">Informações de Contato</h2>
                <div class="space-y-4">
                    <div class="flex items-center">
                        <span class="w-24 text-gray-500 font-semibold flex-shrink-0">Telefone</span>
                        <p v-if="!isEditing" class="text-gray-800">{{ editableUser.phone || 'Não informado' }}</p>
                        <input v-else type="tel" v-model="editableUser.phone" class="text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 flex-1">
                    </div>
                    <div class="flex items-center">
                        <span class="w-24 text-gray-500 font-semibold flex-shrink-0">Localização</span>
                         <p v-if="!isEditing" class="text-gray-800">{{ locationString }}</p>
                         <div v-else class="flex gap-2 flex-1">
                            <input type="text" v-model="editableUser.city" placeholder="Cidade" class="text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 w-2/3">
                            <input type="text" v-model="editableUser.uf" placeholder="UF" maxlength="2" class="text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 w-1/3">
                         </div>
                    </div>
                </div>
            </div>

            <div class="border-t my-8"></div>

            <div>
                <h2 class="text-xl font-bold text-gray-700 mb-4">Preferências de Culinária</h2>
                <div v-if="!isEditing" class="flex flex-wrap gap-2">
                    <span v-if="!editableUser.preferences || editableUser.preferences.length === 0" class="text-gray-500 text-sm">Nenhuma preferência adicionada.</span>
                    <span v-for="pref in editableUser.preferences" :key="pref" class="bg-indigo-100 text-indigo-700 text-sm font-medium px-3 py-1 rounded-full">{{ pref }}</span>
                </div>
                <div v-else>
                    <input type="text" @keydown.enter.prevent="addPreference" placeholder="Adicione uma preferência e pressione Enter" class="w-full border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500">
                    <div class="flex flex-wrap gap-2 mt-2">
                        <span v-for="(pref, index) in editableUser.preferences" :key="pref" class="bg-indigo-100 text-indigo-700 text-sm font-medium px-3 py-1 rounded-full flex items-center">
                            {{ pref }}
                            <button @click="removePreference(index)" class="ml-2 text-indigo-500 hover:text-indigo-800 text-lg leading-none">&times;</button>
                        </span>
                    </div>
                </div>
            </div>

            <div class="border-t mt-8 pt-6 flex justify-end gap-4">
                <button v-if="!isEditing" @click="isEditing = true" class="bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-indigo-700">Editar Perfil</button>
                <template v-else>
                    <button @click="cancelEdit" class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button @click="saveProfile" class="bg-green-500 text-white px-6 py-2 rounded-lg font-bold hover:bg-green-600">Salvar Alterações</button>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue';

const props = defineProps({
    user: { type: Object, required: true }
});
const emit = defineEmits(['updateUser', 'backToMain']);

const isEditing = ref(false);
const editableUser = reactive({
    name: '',
    email: '',
    phone: '',
    city: '',
    uf: '',
    avatarUrl: '',
    preferences: []
});

// Sincroniza o estado local com as props quando elas mudam
watch(() => props.user, (newUser) => {
    if (newUser) {
        Object.assign(editableUser, JSON.parse(JSON.stringify(newUser)));
        if (!editableUser.preferences) {
            editableUser.preferences = [];
        }
    }
}, { immediate: true, deep: true });

const locationString = computed(() => {
    if (editableUser.city && editableUser.uf) return `${editableUser.city}, ${editableUser.uf.toUpperCase()}`;
    if (editableUser.city) return editableUser.city;
    return 'Não informado';
});

const handleAvatarUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;
    const reader = new FileReader();
    reader.onload = (e) => {
        editableUser.avatarUrl = e.target.result;
    };
    reader.readAsDataURL(file);
};

const addPreference = (event) => {
    const newPref = event.target.value.trim();
    if (newPref && !editableUser.preferences.includes(newPref)) {
        editableUser.preferences.push(newPref);
    }
    event.target.value = '';
};

const removePreference = (index) => {
    editableUser.preferences.splice(index, 1);
};

const saveProfile = () => {
    emit('updateUser', JSON.parse(JSON.stringify(editableUser)));
    isEditing.value = false;
};

const cancelEdit = () => {
    // Restaura os dados originais da prop
    Object.assign(editableUser, JSON.parse(JSON.stringify(props.user)));
    isEditing.value = false;
};
</script>