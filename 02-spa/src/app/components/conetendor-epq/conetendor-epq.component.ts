import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-conetendor-epq',
  templateUrl: './conetendor-epq.component.html',
})
export class ConetendorEpqComponent implements OnInit {

  contenedoresEpq:ContenedorEpq[]=[];


  constructor(private http: HttpClient)
  {
    this.http.get("http://192.168.84.108:8080/servicios/contenedor_epq_day/").subscribe((data: any) => 
    {
        this.contenedoresEpq=data;
    });
  }
  ngOnInit(): void {
  }

}

interface ContenedorEpq{
  contenedor: string,
  activityDateTime: string,
  pedido: string,
  ola: string,
}

