import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-consult-kardex',
  templateUrl: './consult-kardex.component.html'
})
export class ColsultKardex implements OnInit {

  kardexs:Kardex[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
    this.http.get("http://127.0.0.1:8000/servicios/consult_kardex/")
    .subscribe((data: any) => {
     this.kardexs=data;
    });
  }

  buscarKardex(tienda:string, fechaInicio:string, fechaFin:string){
    this.http.get("http://127.0.0.1:8000/servicios/consult_kardex/")
    .subscribe((data: any) => {
     this.kardexs=data;
    });
  }

}

interface Kardex{
  item: string,
  location : string,
  date_stamp: string,
  user_tamp: string,
  quantity: string,
  before_on_hand_qty: string,
  after_on_hand_qty: string,
  before_in_transit_qty: string,
  after_in_transit_qty: string,
  before_alloc_qty: string,
  after_alloc_qty: string
}
