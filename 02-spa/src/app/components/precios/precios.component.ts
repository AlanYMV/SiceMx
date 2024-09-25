import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-precios',
  templateUrl: './precios.component.html'
})
export class PreciosComponent implements OnInit {

  precios:Precio[]=[];


  constructor(private http: HttpClient){
      this.http.get("http://192.168.84.108:8080/servicios/precios")
         .subscribe((data: any) => {
          console.log(data);
          this.precios=data;
          console.log(this.precios[0]);
         });

  }
  
  ngOnInit(): void {
  }
}

interface Precio{
  itemCode: string,
  codigoBarras: string,
  categoria: string,
  subcategoria: string,
  clase: string,
  itemName: string,
  storageTemplate: string,
  licencia: string,
  height: string,
  width: string,
  length: string,
  volume: string,
  weight: string,
  fvEstandar: string,
  fvAptosCdmx: string,
  fvAptosForaneos: string,
  fvAptosFronterizos: string,
  fvOutlet: string,
  fvFrontera: string,
  proveedor: string
}

