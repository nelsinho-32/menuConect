<template>
    <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <button @click="$emit('backToMain')" class="mb-6 text-indigo-600 font-semibold hover:underline">&lt; Voltar para a página principal</button>

        <div class="flex justify-between items-center mb-4">
            <div>
                <h1 class="text-3xl font-bold">Reservar em {{ restaurant.name }}</h1>
                <p class="text-gray-500">Selecione uma mesa no mapa abaixo ou edite a disposição.</p>
            </div>
            <div class="flex flex-wrap gap-2">
                <button v-if="!isEditMode && canEditMap" @click="toggleEditMode" class="bg-indigo-600 text-white font-bold py-2 px-4 rounded-lg hover:bg-indigo-700">
                    ✏️ Editar Mapa
                </button>
                <template v-if="isEditMode">
                    <button @click="cycleFloorPattern" class="bg-yellow-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-yellow-600">
                        🎨 Mudar Chão
                    </button>
                    <button @click="cancelChanges" class="bg-gray-200 text-gray-800 font-bold py-2 px-4 rounded-lg hover:bg-gray-300">
                        ❌ Cancelar
                    </button>
                    <button @click="saveChanges" class="bg-green-500 text-white font-bold py-2 px-4 rounded-lg hover:bg-green-600">
                        ✔️ Salvar
                    </button>
                </template>
            </div>
        </div>

        <div v-if="isEditMode" class="bg-gray-100 p-4 rounded-lg mb-4 flex items-center gap-4 border border-gray-200">
            <h3 class="font-bold text-gray-700">Adicionar ao Mapa:</h3>
            <div class="flex gap-3">
                <div v-for="tool in toolbox" :key="tool.label"
                     :title="`Arrastar ${tool.label}`"
                     class="toolbox-item bg-white p-2 rounded shadow-sm border cursor-grab text-center flex flex-col items-center justify-center w-20 h-20"
                     draggable="true"
                     @dragstart="startDragNewElement($event, tool)">
                    <svg width="24" height="24" viewBox="0 0 16 16" fill="currentColor" v-html="tool.icon_svg"></svg>
                    <div class="text-xs mt-1">{{ tool.label }}</div>
                </div>
            </div>
        </div>

        <div class="bg-white p-6 rounded-lg shadow-lg relative overflow-hidden">
            <svg ref="svgMapRef" viewBox="0 0 400 300" class="w-full h-auto rounded" @mousemove="onMouseMove" @mouseup="endInteraction" @mouseleave="endInteraction" @dragover.prevent @drop="dropNewElement">
                <defs>
                    <pattern id="floor-marble" patternUnits="userSpaceOnUse" width="60" height="60">
                        <rect width="60" height="60" fill="#f8fafc"/>
                        <path d="M60 0 L0 60 M30 0 L0 30 M90 0 L0 90" stroke="#e2e8f0" stroke-width="1"/>
                    </pattern>
                    <pattern id="floor-darkwood" patternUnits="userSpaceOnUse" width="80" height="20">
                        <rect width="80" height="20" fill="#4a5568"/>
                        <line x1="0" y1="10" x2="80" y2="10" stroke="#2d3748" stroke-width="0.5"/>
                    </pattern>
                    <pattern id="floor-tiles" patternUnits="userSpaceOnUse" width="40" height="40">
                        <rect width="40" height="40" fill="#e2e8f0"/>
                        <rect width="20" height="20" fill="#cbd5e0"/>
                        <rect x="20" y="20" width="20" height="20" fill="#cbd5e0"/>
                    </pattern>
                </defs>

                <rect width="100%" height="100%" :fill="`url(#${selectedFloorPatternId})`" />

                <g v-for="element in mapElements" :key="element.id"
                   @mousedown.left="isEditMode ? startDrag($event, element) : null"
                   class="group relative"
                   :class="{'draggable-item': isEditMode}"
                   filter="url(#dropShadow)"
                   :transform="`rotate(${element.rotation}, ${element.x + element.width / 2}, ${element.y + element.height / 2})`">
                    <rect :x="element.x" :y="element.y" :width="element.width" :height="element.height" :fill="element.fill" :rx="element.rx || 0"/>
                    <g :transform="`translate(${element.x + element.width/2}, ${element.y + element.height/2 - 5}) scale(0.9)`">
                         <svg width="20" height="20" viewBox="0 0 16 16" :fill="element.textColor" x="-10" y="-10" v-html="element.icon_svg"></svg>
                    </g>
                    <text :x="element.x + element.width / 2" :y="element.y + element.height - 5" text-anchor="middle" font-size="8" :fill="element.textColor" class="font-semibold pointer-events-none">{{ element.label }}</text>

                    <g v-if="isEditMode" class="opacity-0 group-hover:opacity-100 transition-opacity">
                        <line :x1="element.x + element.width / 2" :y1="element.y + element.height / 2" :x2="element.x + element.width / 2" :y2="element.y - 15" stroke="#3b82f6" stroke-width="2" />
                        <circle :cx="element.x + element.width / 2" :cy="element.y - 15" r="5" fill="#3b82f6" @mousedown.stop="startRotate($event, element)" class="cursor-alias" />
                        <circle :cx="element.x + element.width + 5" :cy="element.y - 5" r="7" fill="#ef4444" @mousedown.stop="removeElement(element.id)" class="cursor-pointer" />
                        <text :x="element.x + element.width + 5" :y="element.y - 2" class="pointer-events-none" text-anchor="middle" fill="white" font-size="10">X</text>
                    </g>
                </g>

                <g v-for="table in tables" :key="table.id"
                   @click="isEditMode ? null : selectTable(table)"
                   @mousedown.left="isEditMode ? startDrag($event, table) : null"
                   class="group relative"
                   :class="{'draggable-item': isEditMode, 'cursor-pointer': !isEditMode}"
                   filter="url(#dropShadow)">
                    <rect :x="table.x" :y="table.y" :width="table.width" :height="table.height" :rx="table.shape === 'round' ? '50%' : '3'" :fill="getTableColor(table)"/>
                    <text :x="table.x + table.width / 2" :y="table.y + table.height / 2 + 4" text-anchor="middle" font-size="10" fill="white" class="font-bold pointer-events-none">{{ table.id }}</text>
                </g>
            </svg>
        </div>

        <TableActionModal
            v-if="selectedTable && isActionModalOpen"
            :table="selectedTable"
            :user-reservations="userReservations"
            @close="isActionModalOpen = false"
            @book="openBookingView"
            @join-waitlist="joinWaitlist"
            @cancel="cancelReservation"
            @viewTable="openTableView"
            @openConfig="openTableConfig"
        />
        <BookingModal
            v-if="selectedTable && isBookingModalOpen"
            :table="selectedTable"
            :restaurant="restaurant"
            @close="isBookingModalOpen = false"
            @confirm-booking="confirmBooking"
        />
        <TableViewModal
            v-if="selectedTable && isTableViewModalOpen"
            :tableId="selectedTable.id"
            :images="selectedTable.images"
            @close="isTableViewModalOpen = false"
        />
        <TableConfigModal
            v-if="selectedTable && isTableConfigModalOpen"
            :table="selectedTable"
            @close="isTableConfigModalOpen = false"
            @save="handleSaveTableConfig"
        />
    </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { useUserStore } from '@/stores/userStore';
import TableActionModal from './TableActionModal.vue';
import BookingModal from './BookingModal.vue';
import TableViewModal from './TableViewModal.vue';
import TableConfigModal from './TableConfigModal.vue';

const props = defineProps({ restaurant: Object, userReservations: Object });
// CORREÇÃO: Adicionado o evento 'updateMap'
const emit = defineEmits(['backToMain', 'bookTable', 'joinWaitlist', 'cancelReservation', 'updateMap']);

const userStore = useUserStore();
const authStore = useAuthStore();

const icons = {
    bar: `<path d="M12.5 1a1 1 0 0 1 1 1v5.333a2.5 2.5 0 0 1-5 0V2a1 1 0 0 1 1-1h3zm-.5 4.333V2H9.5v3.333a1.5 1.5 0 0 0 3 0z"/><path d="M13 12.5a1 1 0 0 1 1-1h.5a1 1 0 0 1 0 2h-.5a1 1 0 0 1-1-1zm-10 0a1 1 0 0 1 1-1h.5a1 1 0 0 1 0 2H4a1 1 0 0 1-1-1zM5 6a1 1 0 0 1 1-1h5a1 1 0 0 1 0 2H6a1 1 0 0 1-1-1z"/>`,
    kitchen: `<path d="M1.163 7.828a.5.5 0 0 0 .426.216h12.822a.5.5 0 0 0 .426-.216l-6.411-4.664a.5.5 0 0 0-.578 0l-6.411 4.664zM16 9.5a.5.5 0 0 0-.5-.5h-15a.5.5 0 0 0 0 1h15a.5.5 0 0 0 .5-.5zM2 13.5a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 0-1h-11a.5.5 0 0 0-.5.5z"/>`,
    wc_male: `<path d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"/>`,
    wc_female: `<path d="M3.5 1a.5.5 0 0 1 .5.5v2.5a.5.5 0 0 1-1 0V1.5a.5.5 0 0 1 .5-.5zM12 4a2 2 0 1 0 0-4 2 2 0 0 0 0 4z"/><path d="M12 5.5a.5.5 0 0 1 .5.5v2a.5.5 0 0 1-1 0v-2a.5.5 0 0 1 .5-.5zm-3 4a.5.5 0 0 0 0 1h6a.5.5 0 0 0 0-1H9z"/><path fill-rule="evenodd" d="M12.5 16a.5.5 0 0 1-.5.5h-5a.5.5 0 0 1 0-1h1.5v-2a.5.5 0 0 1 .5-.5h2a.5.5 0 0 1 .5.5v2h1.5a.5.5 0 0 1 .5.5z"/>`,
    entrance: `<path d="M9.293 12.293a1 1 0 0 1 1.414 0l4 4a1 1 0 0 1-1.414 1.414L10 14.414l-3.293 3.293a1 1 0 0 1-1.414-1.414l4-4z"/><path d="M9.293 3.707a1 1 0 0 0 1.414 0l4 4a1 1 0 0 0-1.414 1.414L10 5.828 6.707 9.121a1 1 0 0 0-1.414-1.414l4-4z"/>`,
    cashier: `<path d="M1 3a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v8a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V3zm1 0v8h12V3H2zm12 9.5a.5.5 0 0 1-.5.5h-13a.5.5 0 0 1 0-1h13a.5.5 0 0 1 .5.5zM4 5a1 1 0 0 0 0 2h8a1 1 0 1 0 0-2H4z"/>`,
    table_square: `<path d="M14 1a1 1 0 0 1 1 1v12a1 1 0 0 1-1 1H2a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h12zM2 0a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V2a2 2 0 0 0-2-2H2z"/><path d="M9 13V1H7v12h2z"/>`,
    table_round: `<path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>`,
};

const mapElements = reactive([]);
const tables = reactive([]);
const selectedFloorPatternId = ref('');

onMounted(() => {
    if (props.restaurant) {
        // Usa `Object.assign` para copiar as propriedades para os arrays reativos
        Object.assign(mapElements, JSON.parse(JSON.stringify(props.restaurant.mapElements || [])));
        Object.assign(tables, JSON.parse(JSON.stringify(props.restaurant.tables || [])));
        selectedFloorPatternId.value = props.restaurant.floorPatternId || 'floor-marble';
    }
});

// --- NOVA PROPRIEDADE COMPUTADA PARA PERMISSÕES ---
const canEditMap = computed(() => {
    if (!authStore.currentUser) return false;
    // Admin pode sempre editar qualquer mapa
    if (authStore.currentUser.role === 'admin') return true;
    // Empresa só pode editar se o ID do restaurante corresponder ao seu
    if (authStore.currentUser.role === 'empresa') {
        return authStore.currentUser.restaurant_id === props.restaurant.id;
    }
    // Clientes não podem editar
    return false;
});

const toolbox = reactive([
    { type: 'element', label: 'WC 🚺', width: 40, height: 40, fill: '#fecaca', textColor: '#b91c1c', rx: 3, rotation: 0, icon_svg: icons.wc_female },
    { type: 'element', label: 'WC 🚹', width: 40, height: 40, fill: '#bfdbfe', textColor: '#1e40af', rx: 3, rotation: 0, icon_svg: icons.wc_male },
    { type: 'element', label: 'Bar', width: 100, height: 30, fill: '#a8a29e', textColor: 'white', rx: 5, rotation: 0, icon_svg: icons.bar },
    { type: 'table', label: 'Mesa Quad.', width: 35, height: 35, shape: 'square', status: 'available', icon_svg: icons.table_square, images: [] },
    { type: 'table', label: 'Mesa Red.', width: 40, height: 40, shape: 'round', status: 'available', icon_svg: icons.table_round, images: [] },
]);

const selectedTable = ref(null);
const isActionModalOpen = ref(false);
const isBookingModalOpen = ref(false);
const isTableViewModalOpen = ref(false);
const isTableConfigModalOpen = ref(false);
const isEditMode = ref(false);
const activeInteraction = ref(null);
const activeElement = ref(null);
const offset = reactive({ x: 0, y: 0 });
const svgMapRef = ref(null);
let originalState = {};
let draggedNewElementType = null;

const toggleEditMode = () => {
    isEditMode.value = !isEditMode.value;
    if (isEditMode.value) {
        originalState = {
            tables: JSON.parse(JSON.stringify(tables)),
            mapElements: JSON.parse(JSON.stringify(mapElements)),
            floorPatternId: selectedFloorPatternId.value,
        };
    }
};

const getSVGPoint = (evt) => {
    const svg = svgMapRef.value;
    if (!svg) return { x: 0, y: 0 };
    const pt = svg.createSVGPoint();
    pt.x = evt.clientX;
    pt.y = evt.clientY;
    return pt.matrixTransform(svg.getScreenCTM().inverse());
};

const startDrag = (evt, element) => {
    activeInteraction.value = 'drag';
    activeElement.value = element;
    const point = getSVGPoint(evt);
    offset.x = point.x - element.x;
    offset.y = point.y - element.y;
};

const startRotate = (evt, element) => {
    activeInteraction.value = 'rotate';
    activeElement.value = element;
};

const onMouseMove = (evt) => {
    if (!activeElement.value || !isEditMode.value) return;
    evt.preventDefault();
    const point = getSVGPoint(evt);

    if (activeInteraction.value === 'drag') {
        activeElement.value.x = point.x - offset.x;
        activeElement.value.y = point.y - offset.y;
    } else if (activeInteraction.value === 'rotate') {
        const centerX = activeElement.value.x + activeElement.value.width / 2;
        const centerY = activeElement.value.y + activeElement.value.height / 2;
        const angle = Math.atan2(point.y - centerY, point.x - centerX) * (180 / Math.PI) + 90;
        activeElement.value.rotation = angle;
    }
};

const endInteraction = () => {
    activeElement.value = null;
    activeInteraction.value = null;
};

const saveChanges = () => {
    // CORREÇÃO: Emite um evento com os dados atualizados para o App.vue
    const updatedLayout = {
        mapElements: JSON.parse(JSON.stringify(mapElements)),
        tables: JSON.parse(JSON.stringify(tables)),
        floorPatternId: selectedFloorPatternId.value
    };
    emit('updateMap', updatedLayout);
    toggleEditMode();
};

const cancelChanges = () => {
    if (originalState) {
        tables.length = 0; tables.push(...originalState.tables);
        mapElements.length = 0; mapElements.push(...originalState.mapElements);
        selectedFloorPatternId.value = originalState.floorPatternId;
    }
    toggleEditMode();
};

const floorPatterns = ['floor-marble', 'floor-darkwood', 'floor-tiles'];
const cycleFloorPattern = () => {
    const currentIndex = floorPatterns.indexOf(selectedFloorPatternId.value);
    const nextIndex = (currentIndex + 1) % floorPatterns.length;
    selectedFloorPatternId.value = floorPatterns[nextIndex];
};

const removeElement = (elementId) => {
    const index = mapElements.findIndex(el => el.id === elementId);
    if (index > -1) mapElements.splice(index, 1);
};

const startDragNewElement = (evt, tool) => {
    draggedNewElementType = tool;
    evt.dataTransfer.effectAllowed = 'move';
};

const dropNewElement = (evt) => {
    if (!draggedNewElementType) return;
    const point = getSVGPoint(evt);
    
    const newPiece = {
        ...draggedNewElementType,
        id: `${draggedNewElementType.type}-${Date.now()}`,
        x: point.x - draggedNewElementType.width / 2,
        y: point.y - draggedNewElementType.height / 2,
    };
    
    if (draggedNewElementType.type === 'table') {
        newPiece.id = (tables.length > 0 ? Math.max(...tables.map(t => parseInt(t.id) || 0)) : 0) + 1;
        tables.push(newPiece);
    } else {
        mapElements.push(newPiece);
    }
    draggedNewElementType = null;
};

const openTableView = () => {
    isActionModalOpen.value = false;
    isTableViewModalOpen.value = true;
};

const openTableConfig = () => {
    isActionModalOpen.value = false;
    isTableConfigModalOpen.value = true;
};

const handleSaveTableConfig = (updatedTableData) => {
    const tableIndex = tables.findIndex(t => t.id === updatedTableData.originalId);
    if (tableIndex !== -1) {
        tables[tableIndex].id = updatedTableData.id;
        tables[tableIndex].images = updatedTableData.images;
    }
    isTableConfigModalOpen.value = false;
};

const getTableColor = (table) => {
    if (props.userReservations?.bookedTable?.tableId === table.id) return '#60a5fa';
    if (table.status === 'available') return '#4ade80';
    return '#a8a29e';
};

const selectTable = (table) => { 
    selectedTable.value = table; 
    isActionModalOpen.value = true; 
};

const openBookingView = () => { 
    isActionModalOpen.value = false; 
    isBookingModalOpen.value = true; 
};

const confirmBooking = (bookingDetails) => { 
    emit('bookTable', { ...bookingDetails, restaurant: props.restaurant, table: selectedTable.value }); 
    isBookingModalOpen.value = false; 
};

const joinWaitlist = () => { 
    emit('joinWaitlist', { restaurant: props.restaurant, table: selectedTable.value }); 
    isActionModalOpen.value = false; 
};

const cancelReservation = () => { 
    emit('cancelReservation'); 
    isActionModalOpen.value = false; 
};
</script>

<style scoped>
.draggable-item { cursor: grab; }
.draggable-item:active { cursor: grabbing; filter: drop-shadow(0 0 10px rgba(79, 70, 229, 0.7)); }
.toolbox-item { transition: transform 0.2s ease; user-select: none; }
.toolbox-item:hover { transform: scale(1.1); }
</style>