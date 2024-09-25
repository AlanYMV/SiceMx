import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-recibo-tienda',
  templateUrl: './recibo-tienda.component.html'
})
export class ReciboTiendaComponent implements OnInit {

  recibosTienda:ReciboTienda[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarRecibos(fechaInicio:string, fechaFin:string){
    this.recibosTienda=[];
    this.http.get("http://192.168.84.108:8080/servicios/recibo_tienda/"+fechaInicio+"/"+fechaFin)
    .subscribe((data: any) => {
     this.recibosTienda=data;
    });
  }
}

interface ReciboTienda{
  carga: string,
  pedido: string,
  llegadaTransportista: string,
  inicioScaneo: string,
  finScaneo: string,
  cierreCamion: string,
}
