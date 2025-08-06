<template>
    <section class="my-12">
        <h2 class="section-title mb-6">✨ Planeie seu Encontro</h2>
        
        <div class="border-b border-gray-200 mb-6">
            <nav class="-mb-px flex space-x-6" aria-label="Tabs">
                <button @click="activeTab = 'ai'" :class="getTabClass('ai')">Sugestão da IA</button>
                <button @click="activeTab = 'manual'" :class="getTabClass('manual')">Planear Manualmente</button>
            </nav>
        </div>

        <div v-if="activeTab === 'ai'">
            <div v-if="isLoading" class="flex items-center justify-center p-10 bg-white rounded-lg shadow-lg">
                <div class="loader-dark"></div>
                <p class="ml-4 text-gray-600">A criar experiências únicas para você...</p>
            </div>
            <div v-else-if="error" class="p-10 bg-red-50 text-red-700 rounded-lg shadow-lg text-center">
                <p class="font-bold">Oops! Algo deu errado ao gerar as sugestões.</p>
                <p class="text-sm mt-2">{{ error }}</p>
                <button @click="generateSuggestions" class="mt-4 bg-red-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-red-600">Tentar Novamente</button>
            </div>
            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <EncontroCard 
                    v-for="(suggestion, index) in suggestions" 
                    :key="index"
                    :initial-suggestion="suggestion"
                    :restaurant-menu="restaurant.menu"
                    :restaurant-theme="restaurant.cuisine"
                />
            </div>
        </div>

        <div v-if="activeTab === 'manual'">
            <ManualEncontroPlanner 
                :restaurant="restaurant" 
                @confirm-encontro="payload => $emit('confirmEncontro', payload)"
                @open-table-select-modal="isTableSelectModalOpen = true"
            />
        </div>

        <SelectTableModal
            v-if="isTableSelectModalOpen"
            :restaurant="restaurant"
            @close="isTableSelectModalOpen = false"
            @table-selected="handleTableSelection"
        />
    </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useEncontroStore } from '@/stores/encontroStore'; // 1. IMPORTAR O ARMAZÉM
import { callGemini } from '../../services/geminiService'; 
import EncontroCard from '../EncontroCard.vue';
import ManualEncontroPlanner from '../ManualEncontroPlanner.vue';
import SelectTableModal from '../SelectTableModal.vue';

const props = defineProps({
    restaurant: { type: Object, required: true }
});

defineEmits(['confirmEncontro']);

const encontroStore = useEncontroStore(); // 2. INICIALIZAR O ARMAZÉM
const activeTab = ref('ai');
const isLoading = ref(true);
const suggestions = ref([]);
const error = ref(null);
const isTableSelectModalOpen = ref(false);

const getTabClass = (tabName) => [
    tabName === activeTab.value 
        ? 'border-indigo-500 text-indigo-600' 
        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
    'whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm'
];

async function generateSuggestions() {
    isLoading.value = true;
    error.value = null;
    suggestions.value = [];

    const schema = {
      type: "ARRAY",
      items: {
        type: "OBJECT",
        properties: {
          title: { type: "STRING" },
          table: { type: "STRING" },
          menu: { 
            type: "OBJECT",
            properties: {
              starter: { type: "STRING" },
              main: { type: "STRING" },
              dessert: { type: "STRING" },
              drink: { type: "STRING" }
            }
          },
          tip: { type: "STRING" }
        }
      }
    };
    const prompt = `Aja como um concierge de encontros para o restaurante '${props.restaurant.name}', um local de '${props.restaurant.cuisine}'. Crie exatamente 3 sugestões de "encontros" temáticos. Para cada um, forneça um título criativo, uma sugestão de mesa (ex: "Mesa 5, perto da janela"), um menu completo (entrada, prato principal, sobremesa, bebida) e uma dica especial curta. Baseie as sugestões de pratos e bebidas no cardápio do restaurante: ${JSON.stringify(props.restaurant.menu)}.`;
    
    try {
        const result = await callGemini(prompt, schema);
        if (result && result.length) {
            suggestions.value = result;
        } else {
            throw new Error("A IA não retornou sugestões válidas.");
        }
    } catch (err) {
        error.value = err.message || "Não foi possível gerar sugestões no momento.";
    } finally {
        isLoading.value = false;
    }
}

onMounted(generateSuggestions);

const handleTableSelection = (table) => {
    encontroStore.setTable(table);
    isTableSelectModalOpen.value = false;
};
</script>