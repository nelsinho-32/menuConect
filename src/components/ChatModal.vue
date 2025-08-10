<template>
    <div v-if="chatStore.isChatOpen" class="fixed bottom-4 right-4 w-96 h-[32rem] bg-white rounded-2xl shadow-2xl flex flex-col z-50">
        <div class="p-4 bg-indigo-600 text-white rounded-t-2xl flex justify-between items-center">
            <div>
                <h3 class="font-bold text-lg">Chat de Suporte</h3>
                <p class="text-xs opacity-80">{{ chatStore.chatContext }}</p>
            </div>
            <button @click="chatStore.closeChat()" class="text-white opacity-70 hover:opacity-100">&times;</button>
        </div>

        <div class="flex-grow p-4 overflow-y-auto bg-gray-50">
            <div v-for="(msg, index) in chatStore.messages" :key="index" 
                class="flex mb-3"
                :class="msg.from === userStore.userRole ? 'justify-end' : 'justify-start'">
                <div class="max-w-xs px-4 py-2 rounded-2xl"
                     :class="msg.from === userStore.userRole 
                        ? 'bg-indigo-500 text-white' 
                        : 'bg-gray-200 text-gray-800'">
                    <p class="text-sm">{{ msg.text }}</p>
                    <p class="text-xs opacity-70 text-right mt-1">{{ msg.time }}</p>
                </div>
            </div>
        </div>

        <div class="p-4 border-t bg-white rounded-b-2xl">
            <form @submit.prevent="handleSend" class="flex items-center gap-2">
                <input type="text" v-model="newMessage" placeholder="Digite a sua mensagem..." class="w-full px-3 py-2 border border-gray-300 rounded-full focus:ring-indigo-500 focus:border-indigo-500">
                <button type="submit" class="bg-indigo-600 text-white p-3 rounded-full hover:bg-indigo-700 flex-shrink-0">
                    <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11zM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493z"/></svg>
                </button>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useChatStore } from '@/stores/chatStore';
import { useUserStore } from '@/stores/userStore';

const chatStore = useChatStore();
const userStore = useUserStore();
const newMessage = ref('');

const handleSend = () => {
    chatStore.sendMessage(newMessage.value);
    newMessage.value = '';
};
</script>