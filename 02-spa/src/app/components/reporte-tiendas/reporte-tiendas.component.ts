import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-reporte-tiendas',
  templateUrl: './reporte-tiendas.component.html',
})
export class ReporteTiendasComponent implements OnInit {

  tiendasPendientes:TiendaPendiente[]=[];
  pedidos:Pedido[]=[];
  detallePedidos:DetallePedido[]=[];
  solicitudesTraslado: SolicitudTraslado[]=[];
  tablaTiendasPendientes: TablaTiendaPendiente[]=[];
  tiendasPendientesFecha: TiendaPendienteFecha[]=[];
  pedidosPorCerrar: PedidoPorCerrar[]=[];
  infoPedidosSinTr: InfoPedidoSinTr[]=[];
  tiendasCorreo: TiendaCorreo[]=[];
  total:number=0;

  constructor(private http: HttpClient)
  {
    this.http.get("http://192.168.84.108:8080/servicios/tienda_pendiente")
    .subscribe((data: any) => {
      this.tiendasPendientes=data;
    });

    this.http.get("http://192.168.84.108:8080/servicios/tiendas_fecha")
    .subscribe((data: any) => {
      this.tiendasPendientesFecha=data;
    });

    this.http.get("http://192.168.84.108:8080/servicios/pedido_cerrar/")
    .subscribe((data: any) => {
      console.log(data)
      this.pedidosPorCerrar=data;
    });

    this.http.get("http://192.168.84.108:8080/servicios/pedido_sin_tr/")
    .subscribe((data: any) => {
      console.log(data)
      this.infoPedidosSinTr=data;
    });

    this.http.get("http://192.168.84.108:8080/servicios/tiendas_correo/")
    .subscribe((data: any) => {
      console.log(data)
      this.tiendasCorreo=data;
    });

  }

  actualizarTiendasPendienes()
  {
    this.tiendasPendientes=[]
    this.http.get("http://192.168.84.108:8080/servicios/update_tablas_tienda/").subscribe((data: any) =>
    {
      this.http.get("http://192.168.84.108:8080/servicios/tienda_pendiente").subscribe((data: any) =>
      {
        this.tiendasPendientes=data;
      });

      this.http.get("http://192.168.84.108:8080/servicios/tiendas_fecha").subscribe((data: any) =>
      {
        this.tiendasPendientesFecha=data;
      });

      this.http.get("http://192.168.84.108:8080/servicios/pedido_cerrar/").subscribe((data: any) =>
      {
        this.pedidosPorCerrar=data;
      });

      this.http.get("http://192.168.84.108:8080/servicios/pedido_sin_tr/").subscribe((data: any) =>
      {
        this.infoPedidosSinTr=data;
      });

    });
  }

  enviarCorreos(){
    this.http.get("http://192.168.84.108:8080/servicios/envio_correos/")
    .subscribe((data: any) => {
    });
  }

  enviarCorreo(tienda: string){
    this.http.get("http://192.168.84.108:8080/servicios/envio_correos/"+tienda)
    .subscribe((data: any) => {
    });
    this.http.get("http://192.168.84.108:8080/servicios/tiendas_correo/")
    .subscribe((data: any) => {
      this.tiendasCorreo=data;
    });

  }

  cerrarPedidos(){
    this.http.get("http://192.168.84.108:8080/servicios/cerrar_pedidos/")
    .subscribe((data: any) => {
    });
  }

  guardarFechaTrafico(fecha: string, carga: string, pedido: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/insert_fecha_trafico/"+fecha+"/"+carga+"/"+pedido+"/")
    .subscribe((data: any) => {
      this.http.get("http://192.168.84.108:8080/servicios/tiendas_fecha")
      .subscribe((data: any) => {
        this.tiendasPendientesFecha=data;
      });
    });
  }

  buscarPedido(tienda:string, carga:string, pedido:string)
  {
    let url: string="http://192.168.84.108:8080/servicios/pedido_tienda/";

    if(tienda=='')
    {
      tienda=' ';
    }
    if(carga=='')
    {
      carga=' ';
    }
    if(pedido=='')
    {
      pedido=' ';
    }

    url=url+tienda+"/"+carga+"/"+pedido+"/"
    this.http.get(url)
    .subscribe((data: any) => {
      this.pedidos=data;
      });
  }

  buscarDetallePedido(tienda:string, carga:string, pedido:string, contenedor:string, articulo:string, statusContenedor:string)
  {
    let url: string="http://192.168.84.108:8080/servicios/detalle_pedido_tienda/";

    if(tienda=='')
    {
      tienda=' ';
    }
    if(carga=='')
    {
      carga=' ';
    }
    if(pedido=='')
    {
      pedido=' ';
    }
    if(contenedor=='')
    {
      contenedor=' ';
    }
    if(articulo=='')
    {
      articulo=' ';
    }
    if(statusContenedor=='')
    {
      statusContenedor=' ';
    }

    url=url+tienda+"/"+carga+"/"+pedido+"/"+contenedor+"/"+articulo+"/"+statusContenedor+"/"
    this.http.get(url)
    .subscribe((data: any) => {
      this.detallePedidos=data;
      this.total=0;
      for (let index = 0; index < this.detallePedidos.length; index++)
      {
        this.total=this.total+Number(this.detallePedidos[index].piezas);
      }

      });
  }

  descargarDetallePedido(tienda:string, carga:string, pedido:string, contenedor:string, articulo:string, statusContenedor:string)
  {
    let url: string="http://192.168.84.108:8080/servicios/detalle_pedido_tienda_file/";

    if(tienda=='')
    {
      tienda=' ';
    }
    if(carga=='')
    {
      carga=' ';
    }
    if(pedido=='')
    {
      pedido=' ';
    }
    if(contenedor=='')
    {
      contenedor=' ';
    }
    if(articulo=='')
    {
      articulo=' ';
    }
    if(statusContenedor=='')
    {
      statusContenedor=' ';
    }

    url=url+tienda+"/"+carga+"/"+pedido+"/"+contenedor+"/"+articulo+"/"+statusContenedor+"/"
    this.http.get(url)
    .subscribe((data: any) => {
      this.detallePedidos=data;
      });
  }

  buscarTransaccionTR(documento:string, origenSolicitud:string, destinoSolicitud:string, origenTraslado:string, destinoTraslado:string)
  {
    let url: string="http://192.168.84.108:8080/servicios/solicitud_traslado/";

    if(documento=='')
    {
      documento=' ';
    }
    if(origenSolicitud=='')
    {
      origenSolicitud=' ';
    }
    if(destinoSolicitud=='')
    {
      destinoSolicitud=' ';
    }
    if(origenTraslado=='')
    {
      origenTraslado=' ';
    }
    if(destinoTraslado=='')
    {
      destinoTraslado=' ';
    }

    url=url+documento+"/"+origenSolicitud+"/"+destinoSolicitud+"/"+origenTraslado+"/"+destinoTraslado+"/"
    this.http.get(url)
    .subscribe((data: any) => {
      console.log(data)
      this.solicitudesTraslado=data;
      });
  }

  getDiferencias(){
    this.http.get("http://192.168.84.108:8080/servicios/pedido_cerrar/")
    .subscribe((data: any) => {
      this.pedidosPorCerrar=data;
    });
    this.http.get("http://192.168.84.108:8080/servicios/pedido_sin_tr/")
    .subscribe((data: any) => {
      this.infoPedidosSinTr=data;
    });

  }

  buscarTablaTiendasPendientes(fecha:string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/tabla_tiendas/"+fecha).subscribe((data: any) =>
    {
      this.tablaTiendasPendientes=data;
    });

  }

  ngOnInit(): void {
  }

}

interface TiendaPendiente{
  solicitudEstatus: string,
  carga: string,
  pedido: string,
  nombreAlmacen: string,
  fechaEmbarque: string,
  fechaPlaneada: string,
  transito: string,
  crossDock: string,
  fechaEntrega: string,
}

interface Pedido{
  anio: string,
  estatus: string,
  mes: string,
  fechaCedis: string,
  carga: string,
  tienda: string,
  pedido: string,
  tipoPedido: string,
  solicitudTraslado: string,
  contenedoresPendientes: string,
  contenedoresRecibidos: string,
  itemsPendientes: string,
  piezasPendientes: string,
  itemsRecibidos: string,
  piezasRecibidas: string,
}

interface DetallePedido{
  estatusPedido: string,
  tienda: string,
  carga: string,
  pedido: string,
  contenedor: string,
  item: string,
  itemDescripcion: string,
  estatusContenedor: string,
  piezas: string,
  qc: string
  usuarioPicking: string
  fechaPicking: string
  usuarioQc: string
  fechaQc: string
}

interface SolicitudTraslado{
  documentoSolicitud: string,
  status: string,
  origenSolicitud: string,
  destinoSolicitud: string,
  articulosSolicitud: string,
  cantidadSolicitud: string,
  comentarios: string,
  fechaSolicitud: string,
  fechaVencimiento: string,
  origenTraslado: string,
  destinoTraslado: string,
  articulosTraslado: string,
  cantidadTraslado: string,
}

interface TablaTiendaPendiente{
  nombreAlmacen: string,
  fechaEntrega: string,
  numPedidos: string,
  piezas: string,
  contenedores: string,
}

interface TiendaPendienteFecha{
  carga: string,
  pedido: string,
  nombreAlmacen: string,
  fechaEmbarque: string,
  fechaEntrega: string,
}

interface PedidoPorCerrar{
  pedido: string,
  estatusPedido: string,
  tienda: string,
  carga: string,
  documento: string,
  estatusDocumento: string,
}

interface InfoPedidoSinTr
{
  pedido: string,
  tienda: string,
  almacen: string,
  bnext: string,
  dockEntry: string,
}

interface TiendaCorreo
{
  nombreTienda: string,
}
