<script setup lang="ts">
import { RouterView } from 'vue-router'
import { Toaster } from '@/components/ui/sonner'
import Header from '@/components/HeaderComponent.vue'
import Footer from '@/components/Footer.vue'
import { useDolarStore } from '@/stores/dolarClp'
import { onMounted } from 'vue'

const dolarStore = useDolarStore()

onMounted(async () => {
  await dolarStore.fetchTipoCambio()
})
</script>

<template>
  <Toaster />
  <Header />
  <main class="container mx-auto p-4 min-h-screen">
    <RouterView />
  </main>
  <Footer />
</template>

<style scoped></style>
