import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ArticulosService, Articulo } from "../../servicios/articulos.service";

@Component({
  selector: 'app-articulos',
  templateUrl: './articulos.component.html'
})
export class ArticulosComponent implements OnInit {

  articulos:Articulo[]=[];

/*  constructor( private articulosService: ArticulosService) {
  }*/

  constructor(private http: HttpClient){
    this.http.get("http://192.168.84.108:8080/servicios/articles")
//      this.http.get("http://localhost:8000/servicios/articles")
         .subscribe((data: any) => {
          console.log(data);
          this.articulos=data;
          console.log(this.articulos[0]);
         });
}


  ngOnInit(): void {
    //this.articulos = this.articulosService.getArticulos();
  }

}
