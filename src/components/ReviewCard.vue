<template>
    <div class="flex items-start gap-4 border-t py-4">
        <img :src="review.userAvatarUrl || 'https://placehold.co/256x256/cccccc/ffffff?text=?'" 
             alt="Avatar do usuário" 
             class="w-12 h-12 rounded-full object-cover flex-shrink-0">
        <div class="flex-grow">
            <div class="flex items-center justify-between">
                <h4 class="font-bold text-gray-800">{{ review.userName }}</h4>
                <div class="flex items-center" :title="`${review.rating} de 5 estrelas`">
                    <span v-for="n in 5" :key="n" class="text-xl" :class="n <= review.rating ? 'text-yellow-400' : 'text-gray-300'">★</span>
                </div>
            </div>
            <p class="text-sm text-gray-600 mt-1">{{ review.comment }}</p>
            <p class="text-xs text-gray-400 text-right mt-2">{{ formattedDate }}</p>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    review: { type: Object, required: true }
});

const formattedDate = computed(() => {
    if (!props.review.created_at) return '';
    return new Date(props.review.created_at).toLocaleDateString('pt-BR', {
        day: '2-digit', month: 'long', year: 'numeric'
    });
});
</script>