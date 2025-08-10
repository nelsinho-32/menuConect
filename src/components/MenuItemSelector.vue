<template>
    <div class="flex flex-col">
        <label class="text-xs font-semibold text-gray-500 mb-1">{{ label }}</label>
        <div class="flex items-center gap-2">
            <button
                type="button"
                @click="$emit('select')"
                class="w-full text-left p-2 border rounded-md bg-white hover:border-indigo-400 h-10 truncate"
            >
                <span v-if="selectedItem" class="text-gray-800">{{ selectedItem.name || selectedItem }}</span>
                <span v-else class="text-gray-400">Escolher...</span>
            </button>
            <button
                v-if="selectedItem"
                @click="$emit('customize')"
                type="button"
                title="Personalizar item"
                class="p-2 rounded-md bg-gray-200 hover:bg-gray-300"
            >
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M9.405 1.05c-.413-1.4-2.397-1.4-2.81 0l-.1.34a1.464 1.464 0 0 1-2.105.872l-.31-.17c-1.283-.698-2.686.705-1.987 1.987l.169.311a1.464 1.464 0 0 1-.872 2.105l-.34.1c-1.4.413-1.4 2.397 0 2.81l.34.1a1.464 1.464 0 0 1 .872 2.105l-.17.31c-.698 1.283.705 2.686 1.987 1.987l.311-.169a1.464 1.464 0 0 1 2.105.872l.1.34c.413 1.4 2.397 1.4 2.81 0l.1-.34a1.464 1.464 0 0 1 2.105-.872l.31.17c1.283.698 2.686-.705-1.987-1.987l-.169-.311a1.464 1.464 0 0 1 .872-2.105l.34-.1c1.4-.413 1.4-2.397 0-2.81l-.34-.1a1.464 1.464 0 0 1-.872-2.105l.17-.31c.698-1.283-.705-2.686-1.987-1.987l-.311.169a1.464 1.464 0 0 1-2.105-.872l-.1-.34zM8 10.93a2.929 2.929 0 1 1 0-5.86 2.929 2.929 0 0 1 0 5.858z"/>
                </svg>
            </button>
        </div>
    </div>
</template>

<script setup>
defineProps({
    label: String,
    selectedItem: [String, Object],
});
defineEmits(['select', 'customize']);
</script>