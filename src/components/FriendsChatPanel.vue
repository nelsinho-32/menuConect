<template>
    <div v-if="isOpen" class="absolute top-14 right-0 w-80 bg-white rounded-lg shadow-xl border border-gray-100 flex flex-col z-50 h-[32rem]">
        <div class="px-4 py-2 font-bold text-gray-800 border-b">Amigos</div>
        
        <div class="overflow-y-auto border-b">
            <div v-for="friend in friends" :key="friend.id" 
                 @click="selectedFriend = friend"
                 class="flex items-center gap-3 px-4 py-3 cursor-pointer"
                 :class="selectedFriend && selectedFriend.id === friend.id ? 'bg-indigo-50' : 'hover:bg-gray-50'">
                <div class="relative">
                    <img :src="friend.avatarUrl" class="w-10 h-10 rounded-full">
                    <span v-if="friend.online" class="absolute bottom-0 right-0 w-3 h-3 bg-green-500 rounded-full border-2 border-white"></span>
                </div>
                <div>
                    <p class="font-semibold text-sm text-gray-800">{{ friend.name }}</p>
                    <p class="text-xs text-gray-500">{{ friend.status }}</p>
                </div>
            </div>
        </div>

        <div v-if="selectedFriend" class="flex-grow flex flex-col">
            <div class="p-2 text-center border-b text-sm font-semibold">{{ selectedFriend.name }}</div>
            <div class="flex-grow p-2 text-center text-xs text-gray-400 flex items-center justify-center">
                <p>Chat com {{ selectedFriend.name }} em breve...</p>
            </div>
            <div class="p-2 border-t">
                <input type="text" placeholder="Escreva uma mensagem..." class="w-full text-sm p-2 border rounded-full">
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

defineProps({
    isOpen: { type: Boolean, default: false },
    friends: { type: Array, default: () => [] }
});

const selectedFriend = ref(null);
</script>