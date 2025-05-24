<script setup lang="ts">
import Cart from '@/components/CartComponent.vue'
import { RouterLink, useRoute } from 'vue-router'
import { computed } from 'vue'
import CambioDolarComponent from '@/components/CambioDolarComponent.vue'
import logo from '@/assets/logo-ferremas.png'
const route = useRoute()

// Verifica si la ruta actual es una en la que se desactiva el carrito
const carritoDesactivado = computed(() => {
  return ['/', '/crear-producto'].includes(route.path)
})
</script>

<template>
  <header
    class="p-4 flex items-center bg-secondary text-secondary-foreground sticky z-10 top-0 shadow-md"
  >
    <!-- Columna izquierda -->
    <div class="w-1/3">
      <RouterLink to="/" class="flex items-center gap-2">
        <img :src="logo" alt="FERREMAS logo" class="w-48 h-full" />
      </RouterLink>
    </div>

    <!-- Centro: navegación centrada -->
    <nav class="w-1/3 flex justify-center gap-4 items-center">
      <router-link to="/" class="text-lg">Inicio</router-link>
      <router-link to="/mercado" class="text-lg">Productos</router-link>
      <router-link to="/crear-producto" class="text-lg">Crear producto</router-link>
    </nav>

    <!-- Columna derecha: conversor + carrito -->
    <div class="w-1/3 flex justify-end gap-2 items-center">
      <CambioDolarComponent />
      <div :class="{ 'opacity-50 pointer-events-none grayscale': carritoDesactivado }">
        <Cart />
      </div>
    </div>
  </header>
</template>
