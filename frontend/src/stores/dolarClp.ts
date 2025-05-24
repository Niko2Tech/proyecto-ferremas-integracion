import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useDolarStore = defineStore('dolar', () => {
  const tipoCambio = ref(0)
  const isDollar = ref(false)

  const fetchTipoCambio = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/api/utils/dolar')
      if (!response.ok) {
        throw new Error('Error al obtener el tipo de cambio')
      }
      const data = await response.json()
      tipoCambio.value = data.bid // Asegúrate de que el backend devuelva `bid`
    } catch (error) {
      console.error('Error al obtener el tipo de cambio:', error)
    }
  }

  const toggleCurrency = () => {
    isDollar.value = !isDollar.value
  }

  return {
    tipoCambio,
    isDollar,
    fetchTipoCambio,
    toggleCurrency,
  }
})
