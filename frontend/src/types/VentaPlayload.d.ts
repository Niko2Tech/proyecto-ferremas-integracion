export interface ProductoEnCarrito {
  producto_id: number
  cantidad: number
}

export interface VentaPayload {
  cliente_id: number
  productos: ProductoEnCarrito[]
  direccion_envio?: string
  correo_contacto?: string
}
