import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-pedido-planeacion',
  templateUrl: './pedido-planeacion.component.html',
})
export class PedidoPlaneacionComponent implements OnInit {

  fechaInicio='';
  fechaFin='';
  descargar:boolean=false;
  pedidos:Pedido[]=[];

  constructor(private http: HttpClient) { }

  buscarPedidos(fechaInicio:string, fechaFin:string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/pedidos_planeacion/"+fechaInicio+"/"+fechaFin).subscribe((data: any) =>
    {
      this.pedidos=data;
      this.descargar=true;
    });
  }

  ngOnInit(): void {
  }
}

interface Pedido{
  docNum: string,
  itemCode: string,
  quantity: string,
  docDate: string,
  docDueDate: string,
}
