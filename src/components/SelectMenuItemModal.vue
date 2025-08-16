<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-2xl w-full shadow-2xl">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Escolha um item para <span class="text-indigo-600">{{ category }}</span></h3>
            </div>

            <div class="p-6 max-h-[60vh] overflow-y-auto space-y-3">
                <div v-for="item in menuItems" :key="item.id" 
                    @click="$emit('itemSelected', item)"
                    class="bg-white p-4 rounded-lg shadow-sm flex gap-4 border-2 border-transparent hover:border-indigo-500 cursor-pointer transition-all">
                    
                    <img v-if="item.imageUrl" :src="item.imageUrl" :alt="item.name" class="w-24 h-24 object-cover rounded-md flex-shrink-0">
                    
                    <div class="flex-grow flex flex-col">
                        <div>
                            <h4 class="font-bold text-lg">{{ item.name || item.dishName }}</h4>
                            <p class="text-sm text-gray-500 mt-1">{{ item.description }}</p>
                        </div>
                        <div class="mt-auto">
                             <p class="font-bold text-indigo-600 text-lg">R$ {{ parseFloat(item.price).toFixed(2).replace('.', ',') }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    menuItems: { type: Array, required: true },
    category: { type: String, required: true }
});
defineEmits(['close', 'itemSelected']);
</script>