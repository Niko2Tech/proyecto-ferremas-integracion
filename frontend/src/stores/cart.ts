import { defineStore } from 'pinia'
import type { Herramienta } from '@/types/herramienta'
import { useDolarStore } from './dolarClp'

export const useCartStore = defineStore('cart', {
  state: () => ({
    items: [] as { producto: Herramienta; cantidad: number }[],
  }),

  getters: {
    total: (state) => {
      const dolarStore = useDolarStore()
      return state.items.reduce((sum, item) => {
        const precio = dolarStore.isDollar
          ? item.producto.precio / dolarStore.tipoCambio
          : item.producto.precio
        return sum + precio * item.cantidad
      }, 0)
    },
    cantidadTotal: (state) => state.items.reduce((sum, item) => sum + item.cantidad, 0),
  },

  actions: {
    agregarProducto(herramienta: Herramienta) {
      const existente = this.items.find((item) => item.producto.id === herramienta.id)
      if (existente) {
        existente.cantidad++
      } else {
        this.items.push({ producto: herramienta, cantidad: 1 })
      }
    },
    quitarProducto(producto_id: number) {
      const index = this.items.findIndex((item) => item.producto.id === producto_id)
      if (index !== -1) {
        if (this.items[index].cantidad > 1) {
          this.items[index].cantidad--
        } else {
          this.items.splice(index, 1)
        }
      }
    },
    limpiarCarrito() {
      this.items = []
    },
  },
})
