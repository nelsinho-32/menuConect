import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { useAuthStore } from './authStore';

export const useEncontroStore = defineStore('encontro', () => {
  const authStore = useAuthStore();
  const plannedEncontro = ref(null);
  const isPlanning = computed(() => plannedEncontro.value !== null);

  function startPlanning(restaurant, organizer) {
    plannedEncontro.value = {
      restaurantId: restaurant.id,
      restaurantName: restaurant.name,
      step: 'table',
      organizerName: organizer.name,
      selectedTable: null,
      dateTime: null,
      guests: [{ id: organizer.id, name: organizer.name, menu: {}, isPlaceholder: false }],
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
        // CORREÇÃO: Monta a string no formato que o backend espera, sem conversão de fuso horário.
        plannedEncontro.value.dateTime = `${date} ${time}:00`;
        plannedEncontro.value.step = 'guests';
    }
}

  async function saveEncontroToAPI() {
    if (!plannedEncontro.value || !authStore.token) {
      return Promise.reject("Dados do encontro ou autenticação em falta.");
    }
    try {
      const response = await fetch('http://localhost:5000/api/encontros', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authStore.token}`
        },
        body: JSON.stringify(plannedEncontro.value)
      });
      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.error || "Falha ao salvar o encontro.");
      }
      // Limpa o planeador após o sucesso
      cancelPlanning();
      return data; // Retorna os dados de sucesso
    } catch (error) {
      console.error("Erro ao salvar encontro:", error);
      return Promise.reject(error.message);
    }
  }

  function cancelPlanning() {
    plannedEncontro.value = null;
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
    if (!plannedEncontro.value) return;

    // Encontra o índice do convidado na lista
    const guestIndex = plannedEncontro.value.guests.findIndex(g => g.id === guestId);

    if (guestIndex > -1) {
        // Pega numa cópia do convidado que queremos alterar
        const updatedGuest = { ...plannedEncontro.value.guests[guestIndex] };
        
        // Atualiza o menu nesse convidado copiado
        updatedGuest.menu = {
            ...updatedGuest.menu,
            [itemType]: item
        };

        // Substitui o objeto antigo pelo novo na lista.
        // Isto garante que a reatividade do Vue é acionada de forma limpa.
        plannedEncontro.value.guests[guestIndex] = updatedGuest;
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
    setGuests, inviteGuest, setGuestMenu, setPayment, cancelPlanning, saveEncontroToAPI
  }
})