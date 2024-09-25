import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-peso-contenedor',
  templateUrl: './peso-contenedor.component.html',
})
export class PesoContenedorComponent  implements OnInit {

  peso="";
  tolerancia="";
  tipoContenedor="";
  pesoContenedor!: PesoContenedor;

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarContenedor(contenedor:string){
    this.http.get("http://192.168.84.108:8080/servicios/peso_caja/"+contenedor)
    .subscribe((data: any) => {
     this.pesoContenedor=data;
     this.peso=this.pesoContenedor.peso;
     this.tolerancia=this.pesoContenedor.tolerancia;
     this.tipoContenedor=this.pesoContenedor.tipoContenedor;
    });
  }

  limpiar()
  {
    this.peso="";
    this.tolerancia="";
    this.tipoContenedor="";
  }
}

interface PesoContenedor{
  peso: string,
  tolerancia: string,
  tipoContenedor: string;
}
