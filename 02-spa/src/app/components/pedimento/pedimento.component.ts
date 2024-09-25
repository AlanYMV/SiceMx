import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-pedimento',
  templateUrl: './pedimento.component.html',
})
export class PedimentoComponent implements OnInit {

  numContenedorSalida:string='';

  contenedores:ContenedorSalida[]=[];

  constructor(private http: HttpClient) {

  }

  ngOnInit(): void {
    this.http.get("http://192.168.84.108:8080/servicios/contenedores_salida/%20")
    .subscribe((data: any) => {
     this.contenedores=data;
    });
  }

  buscarContenedorSalida(contenedorSalida:string){
    if (contenedorSalida.length ==0)
    {
      contenedorSalida= '%20';
    }
    this.http.get("http://192.168.84.108:8080/servicios/contenedores_salida/"+contenedorSalida)
    .subscribe((data: any) => {
     this.contenedores=data;
    });
  }
}

interface ContenedorSalida
{
  contenedorSalida: string,
}

