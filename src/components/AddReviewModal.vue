<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-lg w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Avaliar {{ restaurantName }}</h3>
                <p class="text-gray-500">Partilhe a sua experiência connosco!</p>
            </div>
            <form @submit.prevent="handleSubmit" class="p-6 space-y-4">
                <div>
                    <label class="block text-sm font-medium text-gray-700 mb-2">Sua nota</label>
                    <div class="flex items-center justify-center text-4xl star-rating">
                        <span v-for="star in 5" :key="star"
                              @click="form.rating = star"
                              @mouseover="hoverRating = star"
                              @mouseleave="hoverRating = 0"
                              class="cursor-pointer transition-colors"
                              :class="{'text-yellow-400': star <= (hoverRating || form.rating), 'text-gray-300': star > (hoverRating || form.rating)}">
                            ★
                        </span>
                    </div>
                </div>
                <div>
                    <label for="comment" class="block text-sm font-medium text-gray-700">Seu comentário (opcional)</label>
                    <textarea id="comment" v-model="form.comment" rows="4" placeholder="Como foi a sua visita?" class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"></textarea>
                </div>
                 <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3 -m-6 mt-6 pt-6">
                    <button type="button" @click="$emit('close')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300">Cancelar</button>
                    <button type="submit" :disabled="form.rating === 0" class="w-full bg-indigo-600 text-white px-6 py-3 rounded-lg font-bold hover:bg-indigo-700 disabled:bg-gray-300">Enviar Avaliação</button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { reactive, ref } from 'vue';

const props = defineProps({
    restaurantName: { type: String, required: true }
});
const emit = defineEmits(['close', 'submitReview']);

const form = reactive({
    rating: 0,
    comment: ''
});
const hoverRating = ref(0);

const handleSubmit = () => {
    if(form.rating > 0) {
        emit('submitReview', { ...form });
    }
};
</script>

<style scoped>
.star-rating span {
    transition: color 0.2s;
}
</style>