<template>
    <div @click.self="$emit('close-modal')" class="fixed inset-0 modal-backdrop flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full shadow-2xl">
             <div class="p-6 border-b"><h3 class="text-2xl font-bold text-gray-800">Finalizar Pedido</h3></div>
             <div class="p-6">
                <h4 class="font-bold text-lg mb-4">Resumo do Pedido</h4>
                <div class="space-y-2 text-gray-600 mb-6">
                    <div class="flex justify-between">
                        <span>1x {{ dish.dishName }}</span>
                        <span>R$ {{ parseFloat(dish.price).toFixed(2).replace('.',',') }}</span>
                    </div>
                    <div class="flex justify-between font-bold border-t pt-2 mt-2">
                        <span>Total</span>
                        <span>R$ {{ parseFloat(dish.price).toFixed(2).replace('.',',') }}</span>
                    </div>
                 </div>
                 <!-- A lógica completa de pagamento (Pix, etc.) iria aqui -->
             </div>
             <div class="p-6 bg-gray-50 rounded-b-2xl flex flex-col sm:flex-row gap-3">
                <button @click="$emit('close-modal')" class="w-full bg-gray-200 text-gray-700 px-6 py-3 rounded-lg font-bold hover:bg-gray-300 transition-colors">Cancelar</button>
                <button class="w-full bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition-colors">Confirmar Pedido</button>
             </div>
        </div>
    </div>
</template>
<script setup>
defineProps({
  dish: {
    type: Object,
    required: true
  }
});
defineEmits(['close-modal']);
</script>