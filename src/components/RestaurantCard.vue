<template>
    <div @click="$emit('viewRestaurant', restaurant)" class="restaurant-card bg-gray-900 rounded-2xl shadow-lg overflow-hidden group cursor-pointer relative h-80">
        <img :src="restaurant.imageUrl" :alt="restaurant.name"
            class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-300 ease-in-out">
        
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/40 to-transparent"></div>

        <button @click.stop.prevent="$emit('toggleFavorite', restaurant)"
            class="absolute top-3 right-3 bg-white/20 backdrop-blur-sm p-2 rounded-full text-white hover:bg-white/30 transition-colors z-10">
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" viewBox="0 0 16 16">
                <path v-if="isFavorited" d="M3.612 15.443c-.343.197-.734-.044-.657-.449l.75-4.226-3.06-2.925c-.28-.266-.125-.715.225-.76l4.24-.607 1.89-3.834c.175-.354.63-.354.805 0l1.89 3.834 4.24.607c.35.045.504.494.225.76l-3.06 2.925.75 4.226c.077.405-.314.646-.657.449L8 13.197l-4.388 2.246z"/>
                <path v-else d="M2.866 14.85c-.078.444.36.791.746.593l4.39-2.256 4.389 2.256c.386.198.824-.149.746-.592l-.83-4.73 3.522-3.356c.33-.314.16-.888-.282-.95l-4.898-.696L8.465.792a.513.513 0 0 0-.927 0L5.354 5.12l-4.898.696c-.441.062-.612.636-.283.95l3.523 3.356-.83 4.73zm4.905-2.767-3.686 1.894.694-3.957a.565.565 0 0 0-.163-.505L1.71 6.745l4.052-.576a.525.525 0 0 0 .393-.288L8 2.223l1.847 3.658a.525.525 0 0 0 .393.288l4.052.575-2.906 2.77a.565.565 0 0 0-.163.506l.694 3.957-3.686-1.894a.503.503 0 0 0-.461 0z"/>
            </svg>
        </button>

        <div class="relative w-full h-full flex flex-col justify-between p-5 text-white">
            <div>
                <div class="flex items-center gap-4">
                    <img :src="restaurant.logoUrl" :alt="`Logo de ${restaurant.name}`"
                        class="w-16 h-16 rounded-full object-cover border-4 border-white/20 shadow-md flex-shrink-0">
                    <div class="flex-grow">
                        <p class="text-sm font-semibold text-white/80">{{ restaurant.cuisine.toUpperCase() }}</p>
                        <h3 class="font-bold text-xl leading-tight mt-1">{{ restaurant.name }}</h3>
                    </div>
                </div>

                <div class="mt-2 flex items-center text-xs text-white/80">
                    <div class="flex items-center gap-1.5">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M8 16s6-5.686 6-10A6 6 0 0 0 2 6c0 4.314 6 10 6 10zm0-7a3 3 0 1 1 0-6 3 3 0 0 1 0 6z"/></svg>
                        <span>{{ restaurant.city }}</span>
                    </div>
                    <span class="mx-2">·</span>
                    <div v-if="distanceInKm" class="flex items-center gap-1.5">
                        <svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M.5 1a.5.5 0 0 0 0 1h1.11l.401 1.604 1.498 7.985A.5.5 0 0 0 4 12h1a2 2 0 1 0 0 4 2 2 0 0 0 0-4h7a2 2 0 1 0 0 4 2 2 0 0 0 0-4h1a.5.5 0 0 0 .491-.408l1.5-8A.5.5 0 0 0 14.5 3H2.89l-.405-1.621A.5.5 0 0 0 2 1H.5zM6 14a1 1 0 1 1-2 0 1 1 0 0 1 2 0zm7 0a1 1 0 1 1-2 0 1 1 0 0 1 2 0zM9 5.5V7h1.5a.5.5 0 0 1 0 1H9v1.5a.5.5 0 0 1-1 0V8H6.5a.5.5 0 0 1 0-1H8V5.5a.5.5 0 0 1 1 0z"/></svg>
                        <span>~{{ distanceInKm }} km</span>
                    </div>
                </div>
            </div>

            <div class="flex gap-2 opacity-1 group-hover:opacity-100 transition-opacity duration-300">
                <button @click.stop.prevent="$emit('requestReservation', restaurant)" class="w-full bg-white/20 backdrop-blur text-white px-4 py-2 rounded-lg font-bold hover:bg-white/30 text-sm">Reservar Mesa</button>
                <button @click.stop.prevent="$emit('openMenuModal', restaurant)" class="w-full bg-white/20 backdrop-blur text-white px-4 py-2 rounded-lg font-bold hover:bg-white/30 text-sm">Ver Cardápio</button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    restaurant: { type: Object, required: true },
    isFavorited: { type: Boolean, default: false }
});

defineEmits(['toggleFavorite', 'requestReservation', 'viewRestaurant', 'openMenuModal']);

const userLocation = {
    latitude: -6.72059849726947,
    longitude: -35.54075065892938
};

const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) * Math.sin(dLon / 2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
    const straightLineDistance = R * c;
    
    const roadDistanceFactor = 1.4;
    return (straightLineDistance * roadDistanceFactor).toFixed(1);
};

const distanceInKm = computed(() => {
    if (props.restaurant.location && props.restaurant.location.lat && props.restaurant.location.lng) {
        return calculateDistance(
            userLocation.latitude,
            userLocation.longitude,
            props.restaurant.location.lat,
            props.restaurant.location.lng
        );
    }
    return null;
});
</script>