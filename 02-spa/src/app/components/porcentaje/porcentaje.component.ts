import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-porcentaje',
  templateUrl: './porcentaje.component.html'
})
export class PorcentajeComponent implements OnInit {

  container="";
  porcentaje="";
  contenedor!: Contenedor;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarPorcentaje(numContenedor:string){
    this.http.get("http://192.168.84.108:8080/servicios/prioritarios/"+numContenedor)
    .subscribe((data: any) => {
     this.contenedor=data;
     if (this.contenedor.container==null)
     {
      this.container="No existe"
     }
     else
     {
      this.container=this.contenedor.container;
     }
     this.porcentaje=this.contenedor.porcentaje;
    });
  }

}

interface Contenedor{
  container: string,
  porcentaje: string,
}
