<script setup lang="ts">
import CardProduct from '@/components/CardProduct.vue'
import { onMounted } from 'vue'
import { useProductoStore } from '@/stores/productos'

const productoStore = useProductoStore()

onMounted(() => {
  productoStore.fetchProductos()
})
</script>

<template>
  <section class="">
    <h1 class="text-2xl font-bold">Herramientas</h1>
    <article class="flex flex-wrap gap-4 mt-4">
      <CardProduct
        v-for="herramienta in productoStore.productos"
        :key="herramienta.id"
        :herramienta="herramienta"
      />
    </article>
  </section>
</template>
