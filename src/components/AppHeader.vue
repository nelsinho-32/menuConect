<!-- src/components/AppHeader.vue -->
<template>
  <header class="bg-white shadow-sm sticky top-0 z-40">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center py-4">
        <div class="flex items-center space-x-2">
          <svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-indigo-600"><path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/></svg>
          <h1 class="text-2xl font-bold text-gray-900">Menu <span class="brand-text">Connect</span></h1>
        </div>
        <div class="flex items-center gap-6">
          <div @click="$emit('toggle-cart', true)" class="relative cursor-pointer">
            <svg xmlns="http://www.w3.org/2000/svg" width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-gray-600 hover:text-indigo-600"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>
            <span v-if="cartItemCount > 0" class="absolute -top-2 -right-2 bg-red-500 text-white text-xs font-bold rounded-full h-5 w-5 flex items-center justify-center">{{ cartItemCount }}</span>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>
<script setup>
defineProps({
  cartItemCount: {
    type: Number,
    required: true
  }
});
defineEmits(['toggle-cart']);
</script>