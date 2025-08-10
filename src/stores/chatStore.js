import { defineStore } from 'pinia'
import { ref, reactive, watch } from 'vue'
import { useUserStore } from './userStore'

export const useChatStore = defineStore('chat', () => {
  const userStore = useUserStore();
  
  // --- STATE (Estado) ---
  const isChatOpen = ref(false);
  const chatContext = ref('Geral');
  const messages = reactive([]);

  // --- PERSISTÊNCIA (Local Storage) ---
  
  // Observa qualquer alteração nas mensagens e guarda-as
  watch(messages, (newMessages) => {
    localStorage.setItem('menuConnectChatMessages', JSON.stringify(newMessages));
  }, { deep: true });

  // Carrega as mensagens guardadas quando a store é iniciada
  const loadMessagesFromLocalStorage = () => {
    const savedMessages = localStorage.getItem('menuConnectChatMessages');
    if (savedMessages) {
        messages.push(...JSON.parse(savedMessages));
    } else {
        // Mensagem inicial se não houver histórico
        messages.push({ from: 'empresa', text: `Olá! Bem-vindo ao nosso suporte. Como podemos ajudar?`, time: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' }) });
    }
  };
  
  // --- ACTIONS (Ações) ---
  function openChat(context = 'Ajuda Geral') {
    chatContext.value = context;
    isChatOpen.value = true;
  }

  function closeChat() {
    isChatOpen.value = false;
  }

  function sendMessage(text) {
    if(!text.trim()) return;

    const now = new Date();
    const time = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

    messages.push({ from: userStore.userRole, text, time });

    // Simula uma resposta automática
    setTimeout(() => {
        const otherParty = userStore.userRole === 'cliente' ? 'empresa' : 'cliente';
        messages.push({
            from: otherParty,
            text: 'Recebemos a sua mensagem. Um dos nossos atendentes irá responder em breve.',
            time: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
        });
    }, 1500);
  }

  // Carrega as mensagens ao iniciar
  loadMessagesFromLocalStorage();

  return { isChatOpen, chatContext, messages, openChat, closeChat, sendMessage }
})