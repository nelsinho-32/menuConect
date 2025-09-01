<template>
    <div v-if="isOpen" class="absolute top-14 right-0 w-80 bg-white rounded-lg shadow-xl border border-gray-100 flex flex-col z-50 h-[32rem]">
        <div class="px-4 py-2 font-bold text-gray-800 border-b">Amigos</div>
        
        <div class="overflow-y-auto flex-grow">
            <div v-if="pendingRequests.length > 0" class="p-2">
                <h3 class="px-2 text-xs font-semibold text-gray-500 uppercase">Pedidos Pendentes</h3>
                <div v-for="request in pendingRequests" :key="request.id" class="flex items-center justify-between p-2 rounded-lg hover:bg-gray-100">
                    <div class="flex items-center gap-2">
                        <img :src="request.avatarUrl" class="w-8 h-8 rounded-full">
                        <p class="font-semibold text-sm text-gray-800">{{ request.name }}</p>
                    </div>
                    <button @click="$emit('accept-friend-request', request.id)" class="bg-green-500 text-white text-xs font-bold px-2 py-1 rounded-md hover:bg-green-600">
                        Aceitar
                    </button>
                </div>
            </div>

            <div class="p-2">
                <h3 class="px-2 text-xs font-semibold text-gray-500 uppercase">Meus Amigos</h3>
                <div v-if="friends.length === 0 && pendingRequests.length === 0" class="text-center text-gray-400 text-sm py-4">
                    Ainda não tem amigos.
                </div>
                <div v-for="friend in friends" :key="friend.id" class="flex items-center gap-3 px-2 py-2 rounded-lg hover:bg-gray-100">
                    <img :src="friend.avatarUrl" class="w-8 h-8 rounded-full">
                    <p class="font-semibold text-sm text-gray-800">{{ friend.name }}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    isOpen: { type: Boolean, default: false },
    friends: { type: Array, default: () => [] },
    pendingRequests: { type: Array, default: () => [] }
});

defineEmits(['accept-friend-request']);
</script>