<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="max-w-3xl mx-auto">
            <h1 class="text-3xl font-bold">Marketing via WhatsApp</h1>

            <div v-if="managedRestaurant" class="bg-white p-6 rounded-2xl shadow-lg mt-8">
                <div v-if="!isSendingMode" class="space-y-4">
                    <div>
                        <label for="message" class="block text-sm font-medium text-gray-700">Sua Mensagem</label>
                        <textarea id="message" v-model="message" rows="5" placeholder="Olá! Temos uma nova promoção..."
                            class="mt-1 block w-full rounded-md border-gray-300"></textarea>
                    </div>

                    <div>
                        <label class="block text-sm font-medium text-gray-700">Anexar Imagem (Opcional)</label>
                        <div class="mt-1 flex items-start gap-4">
                            <div
                                class="w-32 h-32 border-2 border-dashed rounded-lg flex items-center justify-center text-center p-2 bg-gray-50">
                                <img v-if="imageUrl" :src="imageUrl" class="max-h-full max-w-full object-contain">
                                <p v-else class="text-xs text-gray-400">Nenhuma imagem selecionada</p>
                            </div>
                            <div class="flex-grow">
                                <button @click="isGalleryOpen = true"
                                    class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                                    Selecionar da Galeria
                                </button>
                                <button v-if="imageUrl" @click="imageUrl = null"
                                    class="w-full mt-2 bg-gray-200 text-gray-700 font-bold py-2 px-4 rounded-lg hover:bg-gray-300">
                                    Remover Imagem
                                </button>
                            </div>
                        </div>
                    </div>

                    <div>
                        <button @click="handlePrepare" :disabled="!message.trim() || whatsappStore.state.isLoading"
                            class="w-full bg-green-600 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-700 disabled:bg-gray-400">
                            🚀 Preparar Envio
                        </button>
                    </div>
                </div>

                <div v-else class="text-center">
                    <h3 class="font-bold text-lg text-gray-800">Envio Guiado</h3>
                    <p class="text-sm text-gray-600 mb-4">
                        Encontramos <span class="font-bold">{{ totalRecipients }}</span> cliente(s).
                    </p>
                    <div class="bg-gray-50 p-6 rounded-lg">
                        <p class="text-sm">Enviando para:</p>
                        <p class="text-2xl font-bold text-indigo-700 my-2">{{ currentRecipient.name }}</p>
                        <p class="text-gray-500 font-mono text-sm">{{ currentRecipient.phone }}</p>

                        <a :href="currentWhatsAppLink" target="_blank"
                            class="w-full mt-4 inline-block bg-green-500 text-white font-bold py-3 px-4 rounded-lg hover:bg-green-600">
                            Abrir WhatsApp ({{ currentRecipientIndex + 1 }} de {{ totalRecipients }})
                        </a>
                    </div>

                    <div class="mt-4 flex gap-3">
                        <button @click="isSendingMode = false"
                            class="w-full bg-gray-200 text-gray-700 font-bold py-2 px-4 rounded-lg hover:bg-gray-300">Cancelar</button>
                        <button v-if="!isLastRecipient" @click="goToNextRecipient"
                            class="w-full bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">Próximo
                            &rarr;</button>
                        <button v-else @click="isSendingMode = false"
                            class="w-full bg-blue-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-blue-700">Finalizar</button>
                    </div>
                </div>

                <MediaGalleryModal v-if="isGalleryOpen" @close="isGalleryOpen = false"
                    @imageSelected="selectImageFromGallery" />
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useWhatsappStore } from '@/stores/whatsappStore';
import { useManagementStore } from '@/stores/managementStore';
import { useRestaurantStore } from '@/stores/restaurantStore';
import { callGemini } from '@/services/geminiService';
import MediaGalleryModal from '@/components/MediaGalleryModal.vue';

const emit = defineEmits(['navigateTo']);

const whatsappStore = useWhatsappStore();
const managementStore = useManagementStore();
const restaurantStore = useRestaurantStore();

const message = ref('');
const imageUrl = ref(null);
const isSendingMode = ref(false);
const currentRecipientIndex = ref(0);
const isGettingTips = ref(false);
const engagementTips = ref([]);
const isGalleryOpen = ref(false);

const managedRestaurant = computed(() => {
    if (!managementStore.managedRestaurantId) return null;
    return restaurantStore.restaurants.find(r => r.id === managementStore.managedRestaurantId);
});

const handlePrepare = async () => {
    if (!managedRestaurant.value) {
        alert("Nenhum restaurante selecionado.");
        return;
    }
    
    const result = await whatsappStore.sendMessageToCustomers(message.value, imageUrl.value);

    if (result && result.recipients.length > 0) {
        currentRecipientIndex.value = 0;
        isSendingMode.value = true;
    } else if (result && result.recipients.length === 0) {
        alert("Nenhum cliente com número de telefone válido foi encontrado para este restaurante.");
    }
};

const getEngagementTips = async () => {
    isGettingTips.value = true;
    engagementTips.value = [];
    try {
        const schema = {
            type: "OBJECT",
            properties: {
                tips: {
                    type: "ARRAY",
                    items: { type: "STRING" }
                }
            }
        };
        const prompt = "Aja como um especialista em marketing para restaurantes. Forneça 3 dicas curtas e práticas (uma frase cada) para escrever uma mensagem de WhatsApp eficaz para anunciar uma promoção para clientes.";
        const result = await callGemini(prompt, schema);
        if (result && result.tips) {
            engagementTips.value = result.tips;
        }
    } catch (error) {
        alert("Não foi possível obter dicas da IA no momento.");
    } finally {
        isGettingTips.value = false;
    }
};

const selectImageFromGallery = (url) => {
    imageUrl.value = url;
    isGalleryOpen.value = false;
};

// Funções para o modo de envio guiado
const totalRecipients = computed(() => whatsappStore.state.lastSentResult?.recipients.length || 0);

const currentRecipient = computed(() => {
    if (!isSendingMode.value || totalRecipients.value === 0) return null;
    return whatsappStore.state.lastSentResult.recipients[currentRecipientIndex.value];
});

const isLastRecipient = computed(() => currentRecipientIndex.value === totalRecipients.value - 1);

const currentWhatsAppLink = computed(() => {
    if (!currentRecipient.value) return '#';
    const phone = currentRecipient.value.phone;
    const text = whatsappStore.state.lastSentResult.message_content;
    
    let cleanPhone = phone.replace(/\D/g, '');
    if (cleanPhone.length <= 11) {
        cleanPhone = '55' + cleanPhone;
    }
    const encodedText = encodeURIComponent(text);
    return `https://wa.me/${cleanPhone}?text=${encodedText}`;
});

const goToNextRecipient = () => {
    if (!isLastRecipient.value) {
        currentRecipientIndex.value++;
    }
};
</script>