import { defineStore } from 'pinia'
import type { Herramienta } from '@/types/herramienta'
import { useDolarStore } from './dolarClp'

export const useProductoStore = defineStore('productos', {
  state: () => ({
    productos: [] as Herramienta[],
  }),

  getters: {
    productosConvertidos(state) {
      const dolarStore = useDolarStore()
      return state.productos.map((producto) => {
        const precio = dolarStore.isDollar
          ? producto.precio / dolarStore.tipoCambio
          : producto.precio
        return {
          ...producto,
          precioConvertido: precio,
        }
      })
    },
  },

  actions: {
    async fetchProductos() {
      const res = await fetch('http://localhost:8000/api/productos')
      const data = await res.json()
      this.productos = data
    },
    reducirStock(producto_id: number, cantidad: number) {
      const producto = this.productos.find((p) => p.id === producto_id)
      if (producto && producto.stock >= cantidad) producto.stock -= cantidad
    },
    aumentarStock(producto_id: number, cantidad: number) {
      const producto = this.productos.find((p) => p.id === producto_id)
      if (producto) producto.stock += cantidad
    },
  },
})
