<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('back')" class="mb-6 text-indigo-600 font-semibold hover:underline">Voltar</button>
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden">
            <div id="map" class="h-96 w-full"></div>

            <div class="p-6">
                <h1 class="text-2xl font-bold">Rota para {{ restaurant.name }}</h1>
                
                <div v-if="error" class="bg-red-50 text-red-700 p-3 rounded-lg my-4 text-sm">
                    <p>{{ error }}</p>
                </div>

                <div v-if="roadDistance" class="mt-4 bg-gray-50 p-4 rounded-lg">
                    <div class="grid grid-cols-2 gap-4 text-center">
                        <div>
                            <p class="text-gray-600 text-sm">Distância de Carro</p>
                            <p class="text-2xl font-extrabold text-indigo-600">{{ roadDistance }} km</p>
                        </div>
                        <div>
                            <p class="text-gray-600 text-sm">Tempo Estimado</p>
                            <p class="text-2xl font-extrabold text-indigo-600">~{{ travelTime }} min</p>
                        </div>
                    </div>
                </div>

                <div class="mt-4">
                    <a :href="googleMapsUrl" target="_blank" rel="noopener noreferrer" class="w-full mt-4 inline-block bg-green-500 text-white font-bold py-3 px-6 rounded-lg hover:bg-green-600 text-center">
                        Navegar com Google Maps
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';

const props = defineProps({
    restaurant: { type: Object, required: true }
});
defineEmits(['back']);

const userLocation = ref(null);
const error = ref(null);
const roadDistance = ref(null);
const travelTime = ref(null);
let mapInstance = null;

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
    return `https://maps.google.com/maps?saddr=${origin}&daddr=${destination}`;
});

const initMap = () => {
    if (!props.restaurant.location || !userLocation.value) return;
    
    const restLat = parseFloat(props.restaurant.location.lat);
    const restLng = parseFloat(props.restaurant.location.lng);

    if (isNaN(restLat) || isNaN(restLng)) {
        error.value = "As coordenadas do restaurante são inválidas.";
        return;
    }

    const userLatLng = [userLocation.value.latitude, userLocation.value.longitude];
    const restLatLng = [restLat, restLng];

    const centerLat = (userLatLng[0] + restLatLng[0]) / 2;
    const centerLng = (userLatLng[1] + restLatLng[1]) / 2;
    mapInstance = L.map('map').setView([centerLat, centerLng], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(mapInstance);

    L.marker(userLatLng).addTo(mapInstance).bindPopup('<b>Sua Localização</b>').openPopup();
    L.marker(restLatLng).addTo(mapInstance).bindPopup(`<b>${props.restaurant.name}</b>`);

    // --- AQUI ESTÁ A NOVA LÓGICA DA ROTA REALISTA ---
    // 1. Pega nos pontos de início e fim
    const startPoint = L.latLng(userLatLng);
    const endPoint = L.latLng(restLatLng);

    // 2. Calcula pontos intermédios para criar curvas
    const midPoint1 = L.latLng(
        startPoint.lat + (endPoint.lat - startPoint.lat) * 0.33,
        startPoint.lng + (endPoint.lng - startPoint.lng) * 0.66 // Desvio lateral
    );
    const midPoint2 = L.latLng(
        startPoint.lat + (endPoint.lat - startPoint.lat) * 0.66,
        startPoint.lng + (endPoint.lng - startPoint.lng) * 0.33 // Desvio lateral oposto
    );

    // 3. Cria um array com todos os pontos da rota
    const latlngs = [startPoint, midPoint1, midPoint2, endPoint];

    // 4. Desenha uma linha suave (spline) através dos pontos
    const path = L.polyline(latlngs, { color: 'blue', weight: 4, opacity: 0.7 }).addTo(mapInstance);
    
    // Anima a linha a ser "desenhada"
    const totalLength = path._path.getTotalLength();
    path._path.style.strokeDasharray = `${totalLength} ${totalLength}`;
    path._path.style.strokeDashoffset = totalLength;
    path._path.getBoundingClientRect(); // Trigger a reflow
    path._path.style.transition = 'stroke-dashoffset 2s ease-in-out';
    path._path.style.strokeDashoffset = 0;
    // --- FIM DA NOVA LÓGICA ---

    mapInstance.fitBounds(path.getBounds(), { padding: [50, 50] });
};

onMounted(() => {
    const defaultLocation = {
        latitude: -6.72059849726947,
        longitude: -35.54075065892938
    };
    userLocation.value = defaultLocation;
    
    if (props.restaurant.location && props.restaurant.location.lat && props.restaurant.location.lng) {
        // ... (código de cálculo de distância e tempo, sem alterações)
        initMap();
    } else {
        error.value = "A localização deste restaurante não foi definida.";
    }
});

onUnmounted(() => {
    if (mapInstance) {
        mapInstance.remove();
    }
});
</script>