<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Icon } from '@iconify/vue'
import { Button } from '@/components/ui/button'

defineProps({
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: false,
    default: '',
  },
  isVisible: {
    type: Boolean,
    required: true,
  },
})

const emit = defineEmits(['close'])

const closeModal = () => {
  emit('close')
}
</script>

<template>
  <Transition name="slide-fade">
    <div
      v-if="isVisible"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/30 backdrop-blur-sm"
    >
      <Card class="min-w-[400px] transform transition-all duration-300 ease-out" @click.stop>
        <CardHeader class="flex justify-between items-center">
          <CardTitle>{{ title }}</CardTitle>
          <Button variant="ghost" class="" @click="closeModal">
            <Icon icon="material-symbols:close" width="48" height="48" />
          </Button>
        </CardHeader>
        <CardContent class="gap-2 flex flex-col">
          <CardDescription>{{ description }}</CardDescription>
          <slot name="content" />
        </CardContent>
        <CardFooter class="flex justify-between">
          <slot name="footer" />
        </CardFooter>
      </Card>
    </div>
  </Transition>
</template>

<style scoped>
.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(-1rem);
}
.slide-fade-enter-to {
  opacity: 1;
  transform: translateY(0);
}

.slide-fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-1rem);
}
</style>
