<template>
    <div class="flex flex-col">
        <label class="text-xs font-semibold text-gray-500 mb-1">{{ label }}</label>
        <button 
            type="button"
            @click="$emit('select')" 
            class="w-full text-left p-2 border rounded-md bg-white hover:border-indigo-400 h-10 truncate"
        >
            <span v-if="selectedItem" class="text-gray-800">{{ selectedItem }}</span>
            <span v-else class="text-gray-400">Escolher...</span>
        </button>
    </div>
</template>

<script setup>
defineProps({
    label: String,
    selectedItem: String,
});
defineEmits(['select']);
</script>