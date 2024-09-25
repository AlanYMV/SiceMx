import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-recibos',
  templateUrl: './recibos.component.html'
})
export class RecibosComponent implements OnInit {

  recibosPendientes:ReciboPendiente[]=[];

  constructor(private http: HttpClient){
      this.http.get("http://192.168.84.108:8080/servicios/recibos_pendientes")
         .subscribe((data: any) => {
          console.log(data);
          this.recibosPendientes=data;
         });
  }

  ngOnInit(): void {
  }

}

interface ReciboPendiente{
  receiptId: string,
  item: string,
  itemDesc: string,
  totalQty: string,
  openQty: string,
}
