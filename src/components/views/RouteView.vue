<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('back')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar</button>
        <h1 class="text-3xl font-bold mb-2">Como Chegar</h1>
        <p class="text-gray-500 mb-8">Rota calculada para {{ restaurant.name }}</p>

        <div v-if="error" class="bg-red-50 text-red-700 p-4 rounded-lg mb-6">
            <p class="font-bold">Não foi possível obter a sua localização.</p>
            <p class="text-sm">{{ error }}</p>
        </div>

        <div class="space-y-6">
            <!-- Card de Origem -->
            <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 rounded-full bg-blue-100 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="text-blue-600" viewBox="0 0 16 16"><path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>
                    </div>
                    <div>
                        <p class="text-sm text-gray-500">Origem</p>
                        <h3 class="font-bold text-lg">Sua Localização Padrão</h3>
                    </div>
                </div>
            </div>

            <!-- Ícone de Seta -->
            <div class="text-center text-gray-300">
                <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="currentColor" class="mx-auto" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 4a.5.5 0 0 1 .5.5v5.793l2.146-2.147a.5.5 0 0 1 .708.708l-3 3a.5.5 0 0 1-.708 0l-3-3a.5.5 0 1 1 .708-.708L7.5 10.293V4.5A.5.5 0 0 1 8 4z"/></svg>
            </div>

            <!-- Card de Destino -->
            <div class="bg-white p-6 rounded-lg shadow-md">
                <div class="flex items-center gap-4">
                    <img :src="restaurant.logoUrl" class="w-12 h-12 rounded-full object-cover">
                    <div>
                        <p class="text-sm text-gray-500">Destino</p>
                        <h3 class="font-bold text-lg">{{ restaurant.name }}</h3>
                    </div>
                </div>
            </div>
        </div>

        <!-- AQUI ESTÁ A ALTERAÇÃO: Exibe a distância real e o tempo de viagem -->
        <div v-if="roadDistance" class="mt-8 text-center bg-gray-50 p-6 rounded-lg">
            <div class="grid grid-cols-2 gap-4">
                <div>
                    <p class="text-gray-600">Distância de Carro</p>
                    <p class="text-3xl font-extrabold text-indigo-600">{{ roadDistance }} km</p>
                </div>
                 <div>
                    <p class="text-gray-600">Tempo Estimado</p>
                    <p class="text-3xl font-extrabold text-indigo-600">~{{ travelTime }} min</p>
                </div>
            </div>
            <a :href="googleMapsUrl" target="_blank" rel="noopener noreferrer" class="mt-6 inline-block bg-green-500 text-white font-bold py-3 px-6 rounded-lg hover:bg-green-600">
                Abrir Rota no Google Maps
            </a>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';

const props = defineProps({
    restaurant: { type: Object, required: true }
});
defineEmits(['back']);

const userLocation = ref(null);
const loading = ref(true);
const error = ref(null);
const roadDistance = ref(null);
const travelTime = ref(null);

const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371; // Raio da Terra em km
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    return R * c;
};

const googleMapsUrl = computed(() => {
    if (!userLocation.value || !props.restaurant.location) return '#';
    const origin = `${userLocation.value.latitude},${userLocation.value.longitude}`;
    const destination = `${props.restaurant.location.lat},${props.restaurant.location.lng}`;
    return `https://www.google.com/maps/dir/?api=1&origin=${origin}&destination=${destination}`;
});

onMounted(() => {
    const defaultLocation = {
        latitude: -6.72059849726947,
        longitude: -35.54075065892938
    };
    userLocation.value = defaultLocation;
    
    if (props.restaurant.location && props.restaurant.location.lat && props.restaurant.location.lng) {
        const straightLineDistance = calculateDistance(
            defaultLocation.latitude,
            defaultLocation.longitude,
            props.restaurant.location.lat,
            props.restaurant.location.lng
        );

        // AQUI ESTÁ A NOVA LÓGICA DE ESTIMATIVA
        const roadDistanceFactor = 1.4; // Fator de sinuosidade (ajuste conforme a sua região)
        const averageSpeedKmh = 40; // Velocidade média em km/h em cidade

        roadDistance.value = (straightLineDistance * roadDistanceFactor).toFixed(1);
        travelTime.value = Math.round((parseFloat(roadDistance.value) / averageSpeedKmh) * 60);

    } else {
        error.value = "A localização deste restaurante não foi definida.";
    }
    
    loading.value = false;
});
</script>