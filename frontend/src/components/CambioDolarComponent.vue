<script setup lang="ts">
import { useDolarStore } from '@/stores/dolarClp'
import { Button } from './ui/button'
import { onMounted } from 'vue'

const cambioDolarStore = useDolarStore()

onMounted(() => {
  if (!cambioDolarStore.tipoCambio) {
    cambioDolarStore.fetchTipoCambio()
  }
})

const toggleMoneda = () => {
  cambioDolarStore.toggleCurrency()
}
</script>

<template>
  <div class="flex gap-4 justify-center items-center border p-2 rounded-md">
    <p class="text-sm text-muted-foreground">Tipo de cambio: {{ cambioDolarStore.tipoCambio }}</p>
    <Button variant="outline" @click="toggleMoneda">
      {{ cambioDolarStore.isDollar ? 'Mostrar CLP' : 'Mostrar USD' }}
    </Button>
  </div>
</template>
