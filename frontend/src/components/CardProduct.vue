<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import type { PropType } from 'vue'
import type { Herramienta } from '@/types/herramienta'
import { useCartStore } from '@/stores/cart'
import { useProductoStore } from '@/stores/productos'
import { useDolarStore } from '@/stores/dolarClp'
import { toast } from 'vue-sonner'
import { formatCurrency } from '@/lib/utils'

const productoStore = useProductoStore()
const dolarStore = useDolarStore()
const cart = useCartStore()
const props = defineProps({
  herramienta: {
    type: Object as PropType<Herramienta>,
    required: true,
  },
})

const agregarAlCarrito = () => {
  if (props.herramienta.stock <= 0) return
  cart.agregarProducto(props.herramienta)
  productoStore.reducirStock(props.herramienta.id, 1)
  toast.success(`${props.herramienta.nombre} agregado al carrito`, {
    action: {
      label: 'Cerrar',
      onClick: () => {
        console.log('Ver carrito clicado')
      },
    },
  })
}

const URL_BACK_IMG = 'http://localhost:8000'
</script>

<template>
  <Card class="w-[350px]">
    <CardHeader>
      <img
        :src="URL_BACK_IMG + props.herramienta.imagen_url"
        alt="Imagen de la herramienta"
        class="w-full h-48 object-cover"
      />
    </CardHeader>
    <CardContent class="gap-2 flex flex-col">
      <CardTitle>{{ props.herramienta.nombre }}</CardTitle>
      <div class="flex justify-between">
        <CardDescription>{{ props.herramienta.categoria }}</CardDescription>
        <CardDescription>{{ props.herramienta.marca }}</CardDescription>
      </div>
      <div class="flex justify-between">
        <p>
          Precio:
          {{
            formatCurrency(
              dolarStore.isDollar
                ? props.herramienta.precio / dolarStore.tipoCambio
                : props.herramienta.precio,
              dolarStore.isDollar ? 'USD' : 'CLP',
            )
          }}
        </p>
        <p>Stock disponible: {{ props.herramienta.stock }}</p>
      </div>
    </CardContent>
    <CardFooter class="flex justify-end">
      <Button
        :variant="props.herramienta.stock > 0 ? 'outline' : 'secondary'"
        :disabled="props.herramienta.stock === 0"
        @click="agregarAlCarrito"
      >
        Agregar al carrito
      </Button>
    </CardFooter>
  </Card>
</template>
