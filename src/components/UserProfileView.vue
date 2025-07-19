<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>
        
        <div class="bg-white rounded-2xl shadow-lg p-8 max-w-2xl mx-auto">
            <div class="flex flex-col sm:flex-row items-center gap-6">
                <div class="relative">
                    <img :src="editableUser.avatarUrl" class="w-32 h-32 rounded-full ring-4 ring-indigo-100">
                </div>
                <div class="text-center sm:text-left">
                    <h1 v-if="!isEditing" class="text-3xl font-bold text-gray-800">{{ editableUser.name }}</h1>
                    <input v-else type="text" v-model="editableUser.name" class="text-3xl font-bold text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500">
                    <p v-if="!isEditing" class="text-gray-500">{{ editableUser.email }}</p>
                    <input v-else type="email" v-model="editableUser.email" class="text-gray-500 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 mt-1 w-full">
                </div>
            </div>

            <div class="border-t my-8"></div>

            <div>
                <h2 class="text-xl font-bold text-gray-700 mb-4">Informações de Contato</h2>
                <div class="space-y-4">
                    <div class="flex items-center">
                        <span class="w-24 text-gray-500 font-semibold">Telefone</span>
                        <p v-if="!isEditing" class="text-gray-800">{{ editableUser.phone }}</p>
                        <input v-else type="tel" v-model="editableUser.phone" class="text-gray-800 border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500 flex-1">
                    </div>
                </div>
            </div>

            <div class="border-t my-8"></div>

            <div>
                <h2 class="text-xl font-bold text-gray-700 mb-4">Preferências de Culinária</h2>
                <div v-if="!isEditing" class="flex flex-wrap gap-2">
                    <span v-for="pref in editableUser.preferences" :key="pref" class="bg-indigo-100 text-indigo-700 text-sm font-medium px-3 py-1 rounded-full">{{ pref }}</span>
                </div>
                <div v-else>
                    <input type="text" v-model="preferencesAsString" @keydown.enter.prevent="addPreference" placeholder="Adicione uma preferência e pressione Enter" class="w-full border-b-2 border-indigo-200 focus:outline-none focus:border-indigo-500">
                    <div class="flex flex-wrap gap-2 mt-2">
                        <span v-for="(pref, index) in editableUser.preferences" :key="pref" class="bg-indigo-100 text-indigo-700 text-sm font-medium px-3 py-1 rounded-full flex items-center">
                            {{ pref }}
                            <button @click="removePreference(index)" class="ml-2 text-indigo-500 hover:text-indigo-800">&times;</button>
                        </span>
                    </div>
                </div>
            </div>

            <div class="border-t mt-8 pt-6 flex justify-end gap-4">
                <template v-if="!isEditing">
                    <button @click="isEditing = true" class="bg-indigo-600 text-white px-6 py-2 rounded-lg font-bold hover:bg-indigo-700">Editar Perfil</button>
                </template>
                <template v-else>
                    <button @click="cancelEdit" class="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button @click="saveProfile" class="bg-green-500 text-white px-6 py-2 rounded-lg font-bold hover:bg-green-600">Salvar Alterações</button>
                </template>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue';

const props = defineProps({
    user: { type: Object, required: true }
});
const emit = defineEmits(['updateUser', 'backToMain']);

const isEditing = ref(false);
// Cria uma cópia profunda para edição, para não alterar o original até salvar
const editableUser = reactive(JSON.parse(JSON.stringify(props.user)));

const preferencesAsString = computed({
    get: () => '',
    set: (value) => {
        // Usado apenas para capturar o input, a lógica está no addPreference
    }
});

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
    Object.assign(editableUser, JSON.parse(JSON.stringify(props.user)));
    isEditing.value = false;
};
</script>