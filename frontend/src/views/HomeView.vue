<script setup lang="ts">
import { Button } from '@/components/ui/button'
import logo from '@/assets/logo-ferremas.png' // ajusta la ruta si es distinta
import { RouterLink } from 'vue-router'
</script>

<template>
  <!-- Bienvenida principal -->
  <section class="flex flex-col mb-12 items-center justify-between">
    <div class="w-1/2 flex justify-center mb-5">
      <img :src="logo" alt="FERREMAS logo" class="w-48" />
    </div>
    <div class="w-1/2 flex flex-col justify- center items-center text-center">
      <p class="text-gray-600 text-lg">
        Tu distribuidora de confianza en productos de ferretería y construcción desde los años 80.
      </p>
    </div>
  </section>

  <!-- Secciones informativas -->
  <section class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Calidad y variedad</h2>
      <p class="text-gray-600">
        En FERREMAS contamos con una amplia gama de productos de marcas reconocidas como Bosch,
        Makita, Stanley y Sika. Herramientas manuales, materiales de construcción, equipos de
        seguridad y mucho más.
      </p>
      <RouterLink to="/mercado">
        <Button variant="outline">Explorar productos</Button>
      </RouterLink>
    </div>
    <img
      src="https://plus.unsplash.com/premium_photo-1663011078369-1613ac0a4758?q=80&w=2671&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
      alt="Productos"
      class="rounded-lg shadow w-full h-72 object-cover"
    />
  </section>

  <section class="grid grid-cols-1 md:grid-cols-2 gap-6 items-center">
    <img
      src="https://plus.unsplash.com/premium_photo-1682146423244-e927474d5719?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
      alt="Almacén Ferremas"
      class="rounded-lg shadow w-full h-72 object-cover order-last md:order-first"
    />
    <div class="space-y-4">
      <h2 class="text-2xl font-semibold">Una empresa con historia</h2>
      <p class="text-gray-600">
        Desde Santiago al resto de Chile, FERREMAS se ha expandido con 7 sucursales y una proyección
        nacional. Nos adaptamos a los tiempos con una tienda online intuitiva, fácil y segura.
      </p>
    </div>
  </section>
</template>
