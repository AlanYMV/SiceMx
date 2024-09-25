import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-cargas',
  templateUrl: './cargas.component.html'
})
export class CargasComponent implements OnInit {

  numCarga:string='';

  cargas:Carga[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarCarga(carga:string){
    console.log(carga);
    this.http.get("http://192.168.84.108:8080/servicios/carga/"+carga)
//    this.http.get("http://localhost:8000/servicios/carga/"+carga)
    .subscribe((data: any) => {
     this.cargas=data;
     console.log(this.cargas.length);
     if(this.cargas.length>0)
     {
       this.numCarga=carga;
     }
     else
     {
       this.numCarga='';
     }
    });
  }

}

interface Carga{
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

