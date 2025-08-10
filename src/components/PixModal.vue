<template>
    <div @click.self="$emit('close')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-sm w-full shadow-2xl text-center">
            <div class="p-6 border-b">
                <h3 class="text-2xl font-bold text-gray-800">Pagar com Pix</h3>
                <p class="text-gray-500">Aponte a câmara ou copie o código.</p>
            </div>

            <div class="p-6">
                <p class="text-gray-600">Valor Total:</p>
                <p class="text-4xl font-extrabold text-indigo-600 mb-4">R$ {{ total.toFixed(2).replace('.',',') }}</p>

                <div class="flex justify-center">
                    <svg width="200" height="200" viewBox="0 0 256 256" class="rounded-lg shadow-inner bg-gray-50 p-2">
                        <rect x="32" y="32" width="192" height="192" fill="#FFFFFF"/>
                        <rect x="50" y="50" width="40" height="40" fill="#000000"/>
                        <rect x="166" y="50" width="40" height="40" fill="#000000"/>
                        <rect x="50" y="166" width="40" height="40" fill="#000000"/>
                        <path fill="#000000" d="M128,114h14v14h-14Z M100,114h14v14h-14Z M72,114h14v14h-14Z M128,142h14v14h-14Z M100,142h14v14h-14Z M156,128h14v14h-14Z M128,100h14v14h-14Z M114,128h14v14h-14Z M142,114h14v14h-14Z M114,100h14v14h-14Z"/>
                    </svg>
                </div>

                <div class="mt-4">
                    <p class="text-sm text-gray-500">O QR Code expira em: <span class="font-bold text-red-600">{{ countdown }}</span></p>
                </div>
                
                <div class="mt-4 bg-gray-100 p-3 rounded-lg">
                    <p class="text-sm text-gray-500 text-left mb-1">Pix Copia e Cola:</p>
                    <div class="flex items-center">
                        <input id="pix-code" type="text" readonly :value="pixCode" class="w-full bg-transparent text-sm text-gray-700 truncate">
                        <button @click="copyPixCode" class="ml-2 text-indigo-600 hover:text-indigo-800 flex-shrink-0" :title="copyButtonText">
                            <svg v-if="!copied" xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/><path d="M9.5 1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-3a.5.5 0 0 1-.5-.5v-1a.5.5 0 0 1 .5-.5h3z"/></svg>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 16 16" fill="currentColor"><path d="M12.736 3.97a.733.733 0 0 1 1.047 0c.286.289.29.756.01 1.05L7.88 12.01a.733.733 0 0 1-1.065.02L3.217 8.384a.757.757 0 0 1 0-1.06.733.733 0 0 1 1.047 0l3.052 3.093 5.4-6.425a.247.247 0 0 1 .02-.022z"/></svg>
                        </button>
                    </div>
                </div>
            </div>

            <div class="p-6 bg-gray-50 rounded-b-2xl flex gap-3">
                <button @click="$emit('paymentSuccess')" class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Pagamento Efetuado</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

const props = defineProps({
  cart: { type: Array, required: true }
});
const emit = defineEmits(['close', 'paymentSuccess']);

const pixCode = ref("00020126580014br.gov.bcb.pix0136...");
const copied = ref(false);
const copyButtonText = ref('Copiar código');
const countdown = ref('05:00');
let timerInterval = null;

// --- AQUI ESTÁ A CORREÇÃO ---
const subtotal = computed(() => {
    return props.cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
});

const deliveryFee = computed(() => {
    // Conta quantos restaurantes únicos no carrinho têm pelo menos um item para delivery
    const deliveryRestaurants = new Set();
    props.cart.forEach(item => {
        if (item.dineOption === 'delivery' || !item.dineOption) {
            deliveryRestaurants.add(item.restaurantId);
        }
    });
    return deliveryRestaurants.size * 5.00;
});

const total = computed(() => subtotal.value + deliveryFee.value);
// --- FIM DA CORREÇÃO ---

const copyPixCode = () => {
    navigator.clipboard.writeText(pixCode.value);
    copied.value = true;
    copyButtonText.value = 'Copiado!';
    setTimeout(() => {
        copied.value = false;
        copyButtonText.value = 'Copiar código';
    }, 2000);
};

const startTimer = () => {
    let duration = 5 * 60; // 5 minutos em segundos
    timerInterval = setInterval(() => {
        const minutes = Math.floor(duration / 60);
        const seconds = duration % 60;
        countdown.value = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
        duration--;
        if (duration < 0) {
            clearInterval(timerInterval);
            countdown.value = 'Expirado';
        }
    }, 1000);
};

onMounted(startTimer);
onUnmounted(() => clearInterval(timerInterval));
</script>