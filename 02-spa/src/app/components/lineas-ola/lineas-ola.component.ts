import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-lineas-ola',
  templateUrl: './lineas-ola.component.html'
})
export class LineasOlaComponent implements OnInit {

  numOla:string='';

  lineasOla:LineaOla[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarLineasOla(ola:string){
    this.http.get("http://192.168.84.108:8080/servicios/lineas_ola/"+ola)
    .subscribe((data: any) => {
     this.lineasOla=data;
     if(this.lineasOla.length>0)
     {
       this.numOla=ola;
     }
     else
     {
       this.numOla='';
     }
    });
  }

}

interface LineaOla{
  ola: string,
  pedido: string,
  item: string,
  descripcion: string,
  cantidad: string,
  status: string,
}
