import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute, Params } from '@angular/router';

@Component({
  selector: 'app-detalle-ola',
  templateUrl: './detalle-ola.component.html'
})
export class DetalleOlaComponent implements OnInit {

  ola:string='';

  constructor(private http: HttpClient, private rutaActiva: ActivatedRoute)
  {
    this.rutaActiva.params.subscribe(
      (params: Params) => {
        this.ola = params['numOla'];
      }
    );
  }

  ngOnInit(): void {
  }

}
