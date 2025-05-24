<script setup lang="ts">
import { ref } from 'vue'
import { toast } from 'vue-sonner'
import { useRouter } from 'vue-router'
import { Button } from '@/components/ui/button'
import { Label } from '@/components/ui/label'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardContent, CardFooter, CardTitle } from '@/components/ui/card'

const router = useRouter()

const codigo = ref('')
const marca = ref('')
const nombre = ref('')
const precio = ref(0)
const stock = ref(0)
const categoria = ref('')
const imagen = ref<File | null>(null)
const imagenPreview = ref('')

const subirImagen = async (): Promise<string | null> => {
  if (!imagen.value) return null
  const formData = new FormData()
  formData.append('file', imagen.value)

  try {
    const res = await fetch('http://localhost:8000/api/upload/imagen/', {
      method: 'POST',
      body: formData,
    })
    const data = await res.json()
    return data.imagen_url
  } catch (err) {
    console.log(err)
    toast.error('Error al subir la imagen')
    return null
  }
}

const validarCampos = (): boolean => {
  if (
    !codigo.value ||
    !marca.value ||
    !nombre.value ||
    !precio.value ||
    !stock.value ||
    !categoria.value ||
    !imagen.value
  ) {
    toast.warning('Completa todos los campos antes de continuar')
    return false
  }
  return true
}

const crearProducto = async () => {
  if (!validarCampos()) return

  const url = await subirImagen()
  if (!url) return

  const nuevoProducto = {
    codigo: codigo.value,
    marca: marca.value,
    nombre: nombre.value,
    precio: precio.value,
    stock: stock.value,
    categoria: categoria.value,
    imagen_url: url,
  }

  try {
    const res = await fetch('http://localhost:8000/api/productos/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(nuevoProducto),
    })
    if (!res.ok) throw new Error()
    toast.success('Producto creado exitosamente')
    router.push('/mercado')
  } catch (e) {
    console.log(e)
    toast.error('Error al crear producto')
  }
}

const handleImagenChange = (e: Event) => {
  const target = e.target as HTMLInputElement
  const file = target.files?.[0]
  if (!file) return
  imagen.value = file
  imagenPreview.value = URL.createObjectURL(file)
}
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Crear producto</CardTitle>
    </CardHeader>

    <CardContent class="space-y-4">
      <div class="flex flex-col gap-2">
        <Label for="codigo">Código</Label>
        <Input id="codigo" v-model="codigo" placeholder="Código" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="nombre">Nombre</Label>
        <Input id="nombre" v-model="nombre" placeholder="Nombre" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="marca">Marca</Label>
        <Input id="marca" v-model="marca" placeholder="Marca" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="categoria">Categoría</Label>
        <Input id="categoria" v-model="categoria" placeholder="Categoría" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="precio">Precio CLP</Label>
        <Input id="precio" v-model.number="precio" type="number" placeholder="Precio" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="stock">Stock</Label>
        <Input id="stock" v-model.number="stock" type="number" placeholder="Stock" />
      </div>

      <div class="flex flex-col gap-2">
        <Label for="imagen">Imagen</Label>
        <Input id="imagen" type="file" accept="image/*" @change="handleImagenChange" />
      </div>

      <img
        v-if="imagenPreview"
        :src="imagenPreview"
        class="w-[350px] h-full object-cover rounded"
      />
    </CardContent>

    <CardFooter class="flex justify-end">
      <Button variant="default" @click="crearProducto">Crear producto</Button>
    </CardFooter>
  </Card>
</template>
