import { createRouter, createWebHistory } from 'vue-router'
import MarketView from '@/views/MarketView.vue'
import ConfirmView from '@/views/ConfirmView.vue'
import HomeView from '@/views/HomeView.vue'
import ProductView from '@/views/ProductView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },
    {
      path: '/mercado',
      name: 'market',
      component: MarketView,
    },
    {
      path: '/crear-producto',
      name: 'create-product',
      component: ProductView,
    },
    {
      path: '/confirmar',
      name: 'confirm',
      component: ConfirmView,
    },
  ],
})

export default router
