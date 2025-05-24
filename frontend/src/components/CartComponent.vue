<script setup lang="ts">
import { Button } from '@/components/ui/button'
import { Icon } from '@iconify/vue'
import Modal from '@/components/ModalComponent.vue'
import { ref } from 'vue'
import { useCartStore } from '@/stores/cart'
import { useProductoStore } from '@/stores/productos'
import { useDolarStore } from '@/stores/dolarClp'
import { formatCurrency } from '@/lib/utils'
import type { VentaPayload } from '@/types/VentaPlayload'

const productoStore = useProductoStore()
const cart = useCartStore()
const dolarStore = useDolarStore()
const isVisible = ref(false)

const openModal = () => {
  isVisible.value = true
}

const eliminarProducto = (id: number) => {
  cart.quitarProducto(id)
  productoStore.aumentarStock(id, 1)
}

const redirigirAWebpay = (url: string, token: string) => {
  const form = document.createElement('form')
  form.method = 'POST'
  form.action = url

  const input = document.createElement('input')
  input.type = 'hidden'
  input.name = 'token_ws'
  input.value = token

  form.appendChild(input)
  document.body.appendChild(form)
  form.submit()
}

const comprar = async () => {
  if (!cart.items.length) return

  // Validación básica
  if (!correo.value || !cliente.value.direccion) {
    alert('Por favor completa los datos de contacto.')
    return
  }

  // Lógica para modo CLIENTE
  if (modoCompra.value === 'cliente') {
    if (!cliente.value.nombre) {
      alert('Por favor completa todos los campos del cliente.')
      return
    }

    if (!clienteEncontrado.value) {
      try {
        const res = await fetch('http://127.0.0.1:8000/api/clientes/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            nombre: cliente.value.nombre,
            correo: cliente.value.correo,
            telefono: cliente.value.telefono,
            direccion: cliente.value.direccion,
            recibe_promociones: cliente.value.recibe_promociones,
          }),
        })

        if (!res.ok) {
          const errorData = await res.json()
          console.error('Error al crear cliente:', errorData)
          alert('Error al crear el cliente. Verifica los datos.')
          return
        }

        const data = await res.json()
        cliente.value.id = data.id
      } catch (error) {
        console.error('Error al registrar el cliente:', error)
        alert('No se pudo registrar el cliente.')
        return
      }
    }
  }

  // Preparar datos de la venta
  const ventaPayload: VentaPayload = {
    cliente_id: modoCompra.value === 'cliente' ? cliente.value.id : 1,
    productos: cart.items.map((item) => ({
      producto_id: item.producto.id,
      cantidad: item.cantidad,
    })),
  }

  if (modoCompra.value === 'invitado') {
    ventaPayload.correo_contacto = correo.value
    ventaPayload.direccion_envio = cliente.value.direccion
  }

  try {
    const ventaRes = await fetch('http://localhost:8000/api/ventas/crear', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(ventaPayload),
    })

    if (!ventaRes.ok) {
      const errorText = await ventaRes.text()
      console.error('Error al crear venta:', errorText)
      alert('Error al registrar la venta.')
      return
    }

    const venta = await ventaRes.json()

    const transRes = await fetch('http://localhost:8000/api/webpay/iniciar', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ venta_id: venta.id, isDolar: dolarStore.isDollar }),
    })

    if (!transRes.ok) {
      console.error('Error al iniciar la transacción:', transRes.statusText)
      alert('Error al iniciar el pago.')
      return
    }

    const trans = await transRes.json()
    redirigirAWebpay(trans.url, trans.token)
  } catch (err) {
    console.error('Error en el proceso de compra:', err)
    alert('Hubo un error al procesar la compra.')
  }
}

const modoCompra = ref<'invitado' | 'cliente'>('invitado')

// Datos básicos del formulario
const correo = ref('')
const cliente = ref({
  id: 0,
  nombre: '',
  correo: '',
  telefono: '',
  direccion: '',
  recibe_promociones: false,
})

// funcion para obtener los datos del cliente por su correo
const clienteEncontrado = ref(false)
const clienteCargando = ref(false)

const buscarClientePorCorreo = async () => {
  if (!correo.value || !correo.value.includes('@')) return

  clienteCargando.value = true
  clienteEncontrado.value = false

  try {
    const res = await fetch('http://127.0.0.1:8000/api/clientes/obtener_por_correo', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ correo: correo.value }),
    })

    if (!res.ok) throw new Error('Cliente no encontrado')

    const data = await res.json()
    cliente.value = {
      id: data.id,
      nombre: data.nombre,
      correo: data.correo,
      telefono: data.telefono,
      direccion: data.direccion,
      recibe_promociones: data.recibe_promociones,
    }
    clienteEncontrado.value = true
  } catch (err) {
    console.error('Error al buscar cliente:', err)
    cliente.value = {
      id: 0,
      nombre: '',
      correo: correo.value,
      telefono: '',
      direccion: '',
      recibe_promociones: false,
    }
  } finally {
    clienteCargando.value = false
  }
}
</script>

<template>
  <Button variant="outline" class="p-2" @click="openModal">
    Carrito
    <Icon icon="mdi-light:cart" width="48" height="48" />
    <span
      v-if="cart.cantidadTotal > 0"
      class="ml-2 text-sm absolute right-2 top-2 bg-red-500 text-white rounded-full px-2"
    >
      {{ cart.cantidadTotal }}
    </span>
  </Button>

  <Modal :isVisible="isVisible" title="Carrito" @close="isVisible = false">
    <template #content>
      <div class="flex justify-between h-[450px]">
        <div class="flex flex-col items-center w-[450px]">
          <div class="flex justify-center gap-4 mb-6">
            <Button
              variant="outline"
              :class="modoCompra === 'invitado' ? 'ring-2 ring-primary' : ''"
              @click="modoCompra = 'invitado'"
            >
              Comprar como Invitado
            </Button>
            <Button
              variant="outline"
              :class="modoCompra === 'cliente' ? 'ring-2 ring-primary' : ''"
              @click="modoCompra = 'cliente'"
            >
              Comprar como Cliente
            </Button>
          </div>
          <div class="flex flex-col items-center px-4 w-full">
            <Transition name="fade" mode="out-in">
              <div v-if="modoCompra === 'invitado'" key="invitado" class="w-full">
                <p class="text-lg font-semibold mb-2">Datos del envío (Invitado)</p>
                <input
                  v-model="correo"
                  placeholder="Correo"
                  class="border rounded p-2 w-full mb-2"
                />
                <input
                  v-model="cliente.direccion"
                  placeholder="Dirección"
                  class="border rounded p-2 w-full mb-2"
                />
              </div>

              <div v-else key="cliente" class="w-full">
                <p class="text-lg font-semibold mb-2">Datos del Cliente</p>
                <p class="text-sm text-muted-foreground mb-2" v-if="clienteCargando">
                  Buscando cliente...
                </p>
                <p class="text-sm text-green-600 mb-2" v-if="clienteEncontrado">
                  Cliente encontrado ✅
                </p>
                <p
                  class="text-sm text-red-600 mb-2"
                  v-if="!clienteEncontrado && correo && !clienteCargando"
                >
                  Cliente no registrado o correo inválido ❌
                </p>
                <input
                  v-model="correo"
                  placeholder="Correo"
                  class="border rounded p-2 w-full mb-2"
                  @blur="buscarClientePorCorreo"
                />
                <input
                  v-model="cliente.nombre"
                  placeholder="Nombre"
                  class="border rounded p-2 w-full mb-2"
                />
                <input
                  v-model="cliente.telefono"
                  placeholder="Teléfono"
                  class="border rounded p-2 w-full mb-2"
                />
                <input
                  v-model="cliente.direccion"
                  placeholder="Dirección"
                  class="border rounded p-2 w-full mb-2"
                />
                <label class="flex items-center gap-2">
                  <input type="checkbox" v-model="cliente.recibe_promociones" />
                  ¿Desea recibir promociones?
                </label>
              </div>
            </Transition>
          </div>
        </div>
        <div class="bg-black w-0.5 mx-2"></div>
        <div class="w-[450px]">
          <p class="text-lg font-semibold mb-2 h-full" v-if="!cart.items.length">
            No hay productos
          </p>
          <div class="h-full" v-else>
            <p class="text-lg font-semibold mb-2">Productos en el carrito</p>
            <div
              v-for="item in cart.items"
              :key="item.producto.id"
              class="mb-2 border-b pb-2 flex justify-between gap-5"
            >
              <div>
                <p class="font-bold">{{ item.producto.nombre }}</p>
                <p>
                  Cantidad: {{ item.cantidad }} —
                  {{
                    formatCurrency(
                      dolarStore.isDollar
                        ? (item.producto.precio / dolarStore.tipoCambio) * item.cantidad
                        : item.producto.precio * item.cantidad,
                      dolarStore.isDollar ? 'USD' : 'CLP',
                    )
                  }}
                </p>
              </div>
              <Button variant="outline" @click="eliminarProducto(item.producto.id)">
                <Icon icon="lsicon:minus-filled" class="text-xl" />
              </Button>
            </div>
            <div class="mt-4 font-bold text-end">
              Total:
              {{ formatCurrency(cart.total, dolarStore.isDollar ? 'USD' : 'CLP') }}
            </div>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <Button variant="secondary" @click="isVisible = false">Cerrar</Button>
      <Button
        variant="default"
        class="ml-2"
        :disabled="
          !cart.items.length ||
          (modoCompra === 'cliente' && !cliente.correo) ||
          (modoCompra === 'invitado' && !correo)
        "
        @click="comprar"
      >
        Comprar
      </Button>
    </template>
  </Modal>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
