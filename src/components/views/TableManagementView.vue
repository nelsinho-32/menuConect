<!-- <template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="flex justify-between items-center mb-6">
            <h1 class="text-3xl font-bold">Gestão de Mesas</h1>
            <div v-if="restaurantStore.restaurants.length > 0">
                <select v-model="selectedRestaurantId" class="border-gray-300 rounded-md shadow-sm focus:border-indigo-500 focus:ring-indigo-500">
                    <option :value="null" disabled>Selecione um restaurante</option>
                    <option v-for="restaurant in restaurantStore.restaurants" :key="restaurant.id" :value="restaurant.id">
                        {{ restaurant.name }}
                    </option>
                </select>
            </div>
        </div>

        <div v-if="!selectedRestaurant" class="text-center bg-white p-10 rounded-lg shadow-md">
            <p class="text-gray-500">Por favor, selecione um restaurante para ver a disposição das mesas.</p>
        </div>

        <div v-else>
            <h2 class="text-2xl font-bold mb-4">Estado do Salão: <span class="text-indigo-600">{{ selectedRestaurant.name }}</span></h2>
            <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-6">
                
                <div v-for="table in selectedRestaurant.tables" :key="table.id" 
                    @click="$emit('openTableDetailModal', table)"
                    class="bg-white p-4 rounded-lg shadow-md border-t-4 cursor-pointer hover:shadow-xl transition-shadow"
                    :class="getStatusBorderColor(table.status)">
                    
                    <div class="flex justify-between items-center">
                        <h3 class="font-bold text-lg">Mesa {{ table.id }}</h3>
                        <span class="text-xs font-semibold px-2 py-1 rounded-full" :class="getStatusBgColor(table.status)">
                            {{ getStatusText(table.status) }}
                        </span>
                    </div>

                    <div class="mt-4 text-center">
                        <p class="text-xs text-gray-400">Clique para ver detalhes</p>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useRestaurantStore } from '@/stores/restaurantStore';

// A prop 'orderHistory' foi removida, pois não é mais necessária aqui
defineEmits(['openTableDetailModal']);

const restaurantStore = useRestaurantStore();
const selectedRestaurantId = ref(restaurantStore.restaurants.length > 0 ? restaurantStore.restaurants[0].id : null);

const selectedRestaurant = computed(() => {
    return restaurantStore.restaurants.find(r => r.id === selectedRestaurantId.value);
});

const getStatusBorderColor = (status) => {
    if (status === 'available') return 'border-green-400';
    if (status === 'occupied') return 'border-gray-400';
    if (status === 'cleaning') return 'border-yellow-400';
    return 'border-gray-200';
};
const getStatusBgColor = (status) => {
    if (status === 'available') return 'bg-green-100 text-green-800';
    if (status === 'occupied') return 'bg-gray-200 text-gray-800';
    if (status === 'cleaning') return 'bg-yellow-100 text-yellow-800';
    return 'bg-gray-100 text-gray-800';
}
const getStatusText = (status) => {
    if (status === 'available') return 'Disponível';
    if (status === 'occupied') return 'Ocupada';
    if (status === 'cleaning') return 'A Limpar';
    return 'Indefinido';
}
</script> -->