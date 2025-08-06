import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEncontroStore = defineStore('encontro', () => {
  // Estado
  const plannedEncontro = ref(null);

  // Getters
  const isPlanning = computed(() => plannedEncontro.value !== null);

  // Ações
  function startPlanning(restaurant) {
    plannedEncontro.value = {
      restaurantId: restaurant.id,
      restaurantName: restaurant.name,
      step: 'table', // table -> guests -> menu -> payment
      selectedTable: null,
      guests: [{ id: 1, name: 'Convidado 1', menu: {} }],
      paymentOption: 'local',
    };
  }

  function setTable(table) {
    if (plannedEncontro.value) {
      plannedEncontro.value.selectedTable = table;
      plannedEncontro.value.step = 'guests';
    }
  }

  function setGuests(count) {
    if (plannedEncontro.value) {
      plannedEncontro.value.guests = [];
      for (let i = 1; i <= count; i++) {
        plannedEncontro.value.guests.push({ id: i, name: `Convidado ${i}`, menu: {} });
      }
      plannedEncontro.value.step = 'menu';
    }
  }
  
  function setGuestMenu(guestId, itemType, item) {
    if (plannedEncontro.value) {
        const guest = plannedEncontro.value.guests.find(g => g.id === guestId);
        if(guest) {
            guest.menu[itemType] = item;
        }
    }
  }

  function setPayment(option) {
      if(plannedEncontro.value) {
          plannedEncontro.value.paymentOption = option;
          plannedEncontro.value.step = 'confirm';
      }
  }

  function cancelPlanning() {
    plannedEncontro.value = null;
  }

  return {
    plannedEncontro,
    isPlanning,
    startPlanning,
    setTable,
    setGuests,
    setGuestMenu,
    setPayment,
    cancelPlanning
  }
})