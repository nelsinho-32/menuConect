import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEncontroStore = defineStore('encontro', () => {
  const plannedEncontro = ref(null);
  const isPlanning = computed(() => plannedEncontro.value !== null);

  function startPlanning(restaurant) {
    plannedEncontro.value = {
      restaurantId: restaurant.id,
      restaurantName: restaurant.name,
      step: 'table', // table -> dateTime -> guests -> menu -> payment -> confirm
      selectedTable: null,
      dateTime: null,
      guests: [{ id: 1, name: 'Convidado 1', menu: {} }],
      paymentOption: 'local',
    };
  }

  function setTable(table) {
    if (plannedEncontro.value) {
      plannedEncontro.value.selectedTable = table;
      plannedEncontro.value.step = 'dateTime';
    }
  }

  function setDateTime(date, time) {
    if (plannedEncontro.value) {
      const [year, month, day] = date.split('-').map(Number);
      const [hours, minutes] = time.split(':').map(Number);
      plannedEncontro.value.dateTime = new Date(year, month - 1, day, hours, minutes);
      plannedEncontro.value.step = 'guests';
    }
  }

  function setGuests(count) {
    if (plannedEncontro.value) {
      plannedEncontro.value.guests = Array.from({ length: count }, (_, i) => ({
        id: i + 1, name: `Convidado ${i + 1}`, menu: {}
      }));
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
    plannedEncontro, isPlanning, startPlanning, setTable, setDateTime,
    setGuests, setGuestMenu, setPayment, cancelPlanning
  }
})