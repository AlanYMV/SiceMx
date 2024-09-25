import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pedidos',
  templateUrl: './pedidos.component.html'
})
export class PedidosComponent implements OnInit {

  numPedido:string='';

  pedidos:Pedido[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarPedido(pedido:string){
    console.log(pedido);
    this.http.get("http://192.168.84.108:8080/servicios/pedido/"+pedido)
    .subscribe((data: any) => {
     this.pedidos=data;
     console.log(this.pedidos.length);
     if(this.pedidos.length>0)
     {
       this.numPedido=pedido;
     }
     else
     {
       this.numPedido='';
     }
    });
  }

}

interface Pedido{
  cantidad: string,
  idUnidadEmbalaje: string,
  descripcionMaterialCarga: string,
  pesoArticulo: string,
  idUnidadPeso: string,
  claveProductoServicio: string,
  claveUnidadMedidaEmbalaje: string,
  claveUnidad: string,
  materialPeligroso: string,
  pedido: string,
  tienda: string,
  nombreTienda: string,
  codigoPostal: string,
  pais: string,
  estado: string,
  direccion: string,
  unidadMedida: string,
  idOrigen: string,
  idDestino: string,
  volumen: string,
  unidadVolumen: string
}
