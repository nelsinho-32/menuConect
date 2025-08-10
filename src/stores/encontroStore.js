import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEncontroStore = defineStore('encontro', () => {
  const plannedEncontro = ref(null);
  const isPlanning = computed(() => plannedEncontro.value !== null);

  function startPlanning(restaurant, organizer) {
    plannedEncontro.value = {
      restaurantId: restaurant.id,
      restaurantName: restaurant.name,
      step: 'table', // table -> dateTime -> guests -> invites -> menu -> payment -> confirm
      organizerName: organizer.name,
      selectedTable: null,
      dateTime: null,
      // O organizador já começa como o primeiro convidado
      guests: [{ id: organizer.id, name: organizer.name, menu: {} }],
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

  function setGuests(count, organizer) {
    if (plannedEncontro.value) {
      const guests = [{ id: organizer.id, name: organizer.name, menu: {} }];
      for (let i = 1; i < count; i++) {
        guests.push({ id: `guest-${i}`, name: `Convidado ${i + 1}`, menu: {}, isPlaceholder: true });
      }
      plannedEncontro.value.guests = guests;
      plannedEncontro.value.step = 'invites';
    }
  }

  function inviteGuest(guestIndex, userToInvite) {
    if (plannedEncontro.value && plannedEncontro.value.guests[guestIndex]) {
        plannedEncontro.value.guests[guestIndex] = {
            id: userToInvite.id,
            name: userToInvite.name,
            menu: {}
        };
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
    setGuests, inviteGuest, setGuestMenu, setPayment, cancelPlanning
  }
})