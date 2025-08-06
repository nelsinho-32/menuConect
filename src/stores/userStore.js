import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  // Estado: O tipo de utilizador atual. Começa como 'cliente'.
  const userRole = ref('cliente') // pode ser 'cliente' ou 'empresa'

  // Getter: Uma forma fácil de verificar se o utilizador é uma empresa.
  const isCompanyUser = () => {
    return userRole.value === 'empresa'
  }

  // Ação: A função que nos permite mudar o tipo de utilizador.
  const setUserRole = (role) => {
    if (['cliente', 'empresa'].includes(role)) {
      userRole.value = role
      console.log(`Papel do utilizador alterado para: ${role}`)
    }
  }

  return { userRole, isCompanyUser, setUserRole }
})