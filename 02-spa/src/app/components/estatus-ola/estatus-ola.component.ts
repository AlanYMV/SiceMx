import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-estatus-ola',
  templateUrl: './estatus-ola.component.html'
})
export class EstatusOlaComponent implements OnInit {

  estatusOla:estatusOla[]=[];

  constructor(private http: HttpClient)
  {
    this.http.get("http://192.168.84.108:8080/servicios/estatus_ola")
       .subscribe((data: any) => {
        console.log(data);
        this.estatusOla=data;
       });
  }

  ngOnInit(): void {
  }

}

interface estatusOla{
  ola: string,
  semana: string,
  pedidos: string,
  contenedores: number,
  pickingPending: string,
  inPicking: string,
  packingPending: string,
  inPacking: string,
  stagingPending: string,
  loadingPending: string,
  shipConfirmPending: string,
  loadConfirmPending: string,
  closed: number,
  carton: string,
  bolsa: string,
}
