<script setup lang="ts">
import { useRoute } from 'vue-router'
import { ref, onMounted } from 'vue'
import type { ConfirmacionPago, VentaConfirmada } from '@/types/webpay'
import { useDolarStore } from '@/stores/dolarClp'
import Button from '@/components/ui/button/Button.vue'

const route = useRoute()
const confirmacion = ref<ConfirmacionPago | null>(null)
const venta = ref<VentaConfirmada | null>(null)
const error = ref(false)

const dolarStore = useDolarStore()

onMounted(async () => {
  const tokenWs = route.query.token_ws as string
  if (!tokenWs) {
    error.value = true
    return
  }

  try {
    const res = await fetch(`http://localhost:8000/api/webpay/confirmar?token_ws=${tokenWs}`)
    if (!res.ok) throw new Error()
    const data = await res.json()
    confirmacion.value = data

    const resVenta = await fetch(`http://localhost:8000/api/ventas/orden/${data.orden}`)
    if (!resVenta.ok) throw new Error()
    const ventaData = await resVenta.json()
    venta.value = ventaData

    // Si la venta tiene valor en dólar, activa vista en dólar
    if (ventaData.total_dolar > 0 && !dolarStore.isDollar) {
      dolarStore.toggleCurrency()
    }
  } catch (e) {
    console.error('Error al confirmar el pago:', e)
    error.value = true
  }
})

function formatMoney(monto: number, moneda: 'CLP' | 'USD') {
  return new Intl.NumberFormat('es-CL', {
    style: 'currency',
    currency: moneda,
    maximumFractionDigits: moneda === 'USD' ? 2 : 0,
  }).format(monto)
}
</script>

<template>
  <main class="container mx-auto max-w-xl mt-12 px-4">
    <div v-if="error" class="bg-red-100 text-red-700 p-4 rounded shadow">
      <h2 class="text-xl font-bold">Error al confirmar el pago</h2>
      <p>Por favor intenta nuevamente o comunícate con soporte.</p>
      <div class="mt-4">
        <router-link to="/" class="">
          <Button variant="outline">Volver al inicio</Button>
        </router-link>
      </div>
    </div>

    <div v-else-if="!confirmacion || !venta" class="text-center py-16">
      <p class="text-gray-500">Confirmando tu pago, por favor espera...</p>
    </div>

    <div v-else class="bg-white border border-gray-200 rounded-lg p-6 shadow space-y-4">
      <h2 class="text-2xl font-bold mb-2">
        ¡{{ confirmacion.estado === 'AUTHORIZED' ? 'Pago exitoso' : 'Estado de pago' }}!
      </h2>
      <p><span class="font-semibold">Mensaje:</span> {{ confirmacion.mensaje }}</p>
      <p>
        <span class="font-semibold">Estado:</span>
        <span
          :class="{
            'text-green-600': confirmacion.estado === 'AUTHORIZED',
            'text-yellow-600': confirmacion.estado !== 'AUTHORIZED',
          }"
        >
          {{ confirmacion.estado }}
        </span>
      </p>

      <div class="flex items-center gap-2" v-if="venta.total_dolar > 0">
        <span class="text-sm">Visualizar en:</span>
        <button
          class="px-2 py-1 border rounded text-xs"
          :class="{ 'bg-blue-100': dolarStore.isDollar }"
          @click="dolarStore.isDollar = true"
        >
          USD
        </button>
        <button
          class="px-2 py-1 border rounded text-xs"
          :class="{ 'bg-blue-100': !dolarStore.isDollar }"
          @click="dolarStore.isDollar = false"
        >
          CLP
        </button>
      </div>

      <p>
        <span class="font-semibold">Monto pagado:</span>
        {{
          dolarStore.isDollar
            ? formatMoney(venta.total_dolar, 'USD')
            : formatMoney(confirmacion.monto, 'CLP')
        }}
      </p>

      <p><span class="font-semibold">Correo:</span> {{ venta.correo_contacto }}</p>
      <p><span class="font-semibold">Dirección:</span> {{ venta.direccion_envio }}</p>

      <div class="mt-4">
        <p class="font-semibold">Productos:</p>
        <ul class="list-disc list-inside">
          <li v-for="detalle in venta.detalles" :key="detalle.producto_id">
            Producto ID {{ detalle.producto_id }} – Cantidad: {{ detalle.cantidad }} – Precio
            unitario:
            {{
              dolarStore.isDollar
                ? formatMoney(detalle.precio_unitario / dolarStore.tipoCambio, 'USD')
                : formatMoney(detalle.precio_unitario, 'CLP')
            }}
          </li>
        </ul>
      </div>

      <p><span class="font-semibold">Orden de compra:</span> {{ confirmacion.orden }}</p>

      <div class="mt-6">
        <router-link to="/">
          <Button variant="outline">Volver al inicio</Button>
        </router-link>
      </div>
    </div>
  </main>
</template>
