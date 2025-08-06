<template>
    <div @click.self="$emit('close')" class="fixed inset-0 bg-black/70 flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-3xl w-full shadow-2xl relative">
             <button @click="$emit('close')" class="absolute -top-4 -right-4 bg-white rounded-full p-1 text-gray-700 hover:text-red-500 z-10">
                <svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
            </button>
            <div class="p-6">
                <h3 class="text-2xl font-bold text-gray-800">Selecione uma Mesa Disponível</h3>
                <p class="text-gray-500">Clique na mesa que deseja reservar.</p>
            </div>

            <div class="p-4 bg-gray-50">
                 <svg viewBox="0 0 400 300" class="w-full h-auto rounded">
                    <defs>
                        <pattern id="modal-floor-marble" patternUnits="userSpaceOnUse" width="60" height="60">
                            <rect width="60" height="60" fill="#f8fafc"/>
                            <path d="M60 0 L0 60 M30 0 L0 30 M90 0 L0 90" stroke="#e2e8f0" stroke-width="1"/>
                        </pattern>
                    </defs>
                    <rect width="100%" height="100%" :fill="`url(#${restaurant.floorPatternId || 'modal-floor-marble'})`" />
                    <g v-for="element in restaurant.mapElements" :key="element.id" :transform="`rotate(${element.rotation}, ${element.x + element.width / 2}, ${element.y + element.height / 2})`">
                        <rect :x="element.x" :y="element.y" :width="element.width" :height="element.height" :fill="element.fill" :rx="element.rx || 0"/>
                         <g :transform="`translate(${element.x + element.width/2}, ${element.y + element.height/2 - 5}) scale(0.9)`">
                            <svg width="20" height="20" viewBox="0 0 16 16" :fill="element.textColor" x="-10" y="-10" v-html="element.icon_svg"></svg>
                        </g>
                    </g>
                    <g v-for="table in restaurant.tables" :key="table.id" 
                       class="group"
                       :class="table.status === 'available' ? 'cursor-pointer' : 'cursor-not-allowed'"
                       @click="table.status === 'available' ? selectTable(table) : null">
                        <rect 
                            :x="table.x" :y="table.y" :width="table.width" :height="table.height" 
                            :rx="table.shape === 'round' ? '50%' : '3'" 
                            :fill="getTableColor(table)" 
                            :class="{'group-hover:opacity-70 transition-opacity': table.status === 'available'}"
                        />
                        <text :x="table.x + table.width / 2" :y="table.y + table.height / 2 + 4" text-anchor="middle" font-size="10" fill="white" class="font-bold pointer-events-none">{{ table.id }}</text>
                    </g>
                </svg>
            </div>
        </div>
    </div>
</template>

<script setup>
const props = defineProps({
    restaurant: { type: Object, required: true }
});
const emit = defineEmits(['close', 'tableSelected']);

const getTableColor = (table) => {
    if (table.status === 'available') return '#4ade80'; // Verde
    return '#a8a29e'; // Cinza
};

const selectTable = (table) => {
    emit('tableSelected', table);
};
</script>