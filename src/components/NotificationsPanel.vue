<template>
    <div v-if="isOpen" class="absolute top-14 right-0 w-80 bg-white rounded-lg shadow-xl border border-gray-100 py-2 z-50">
        <div class="px-4 py-2 font-bold text-gray-800 border-b">Notificações</div>
        <div class="max-h-80 overflow-y-auto">
            <div v-if="notifications.length === 0" class="text-center py-6 text-gray-500 text-sm">
                Nenhuma notificação nova.
            </div>
            <div v-else>
                <div v-for="notification in notifications" :key="notification.id" class="flex items-start gap-3 px-4 py-3 hover:bg-gray-50 border-b">
                    <div class="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" :class="notification.bgColor">
                        <span class="text-lg">{{ notification.icon }}</span>
                    </div>
                    <div>
                        <p class="text-sm text-gray-700">{{ notification.message }}</p>
                        <p class="text-xs text-gray-400 mt-1">{{ notification.time }}</p>
                    </div>
                </div>
            </div>
        </div>
        <div class="px-4 py-2 text-center border-t">
            <button class="text-sm font-semibold text-indigo-600 hover:underline">Ver todas</button>
        </div>
    </div>
</template>

<script setup>
defineProps({
    isOpen: { type: Boolean, default: false },
    notifications: { type: Array, default: () => [] }
});
</script>