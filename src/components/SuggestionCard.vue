<template>
    <div class="bg-indigo-50 p-4 rounded-lg border border-indigo-100">
        <h4 class="font-bold text-lg text-indigo-800">{{ suggestion.dishName }}</h4>
        <p class="text-sm font-semibold text-gray-500">{{ suggestion.restaurantName }}</p>
        <p class="text-sm text-gray-700 mt-2">✨ {{ suggestion.reason }}</p>
    </div>
</template>
<script setup>
defineProps({
    suggestion: { type: Object, required: true }
});
</script>