export interface ConfirmacionPago {
  mensaje: string
  estado: string
  monto: number
  orden: string
  total_dolar: number
}

export interface DetalleVenta {
  producto_id: number
  cantidad: number
  precio_unitario: number
}

export interface VentaConfirmada {
  id: number
  cliente_id: number
  total: number
  total_dolar: number
  estado: string
  orden_compra: string
  fecha: string
  direccion_envio?: string
  correo_contacto?: string
  detalles: DetalleVenta[]
}
