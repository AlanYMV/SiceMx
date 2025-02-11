import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-inventory-available',
  templateUrl: './inventory-available.component.html'
})
export class InventoryAvailable implements OnInit {

  inventory:Inventory[]=[];
  Dt = '';

  constructor(private http: HttpClient) {
    this.Dt = this.dateToday()
    this.http.get('http://192.168.84.108:8080/servicios/inventario_disponible/'+this.Dt).subscribe((data: any) => {
      console.log(data);
      this.inventory = data;
    });}

  ngOnInit(): void {
  }
  dateToday(): string {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); 
    var yyyy = today.getFullYear();
    var todayDate = '';

    todayDate = ''+ yyyy+ '-' + mm + '-'+ dd + '';
    console.log(todayDate);
    return todayDate
  }
  searchInventory(fecha:string){
    // console.log(fecha)
    if (fecha){
      this.http.get('http://192.168.84.108:8080/servicios/inventario_disponible/'+fecha).subscribe((data: any) => {
        console.log(data);
        this.inventory = data;
      });
    }
    else{
      alert("Ingrese la fecha que desea buscar")
    }
  }
  download(fecha:string){
    console.log(fecha)
    if (fecha){
      const url: string = "http://192.168.84.108:8080/servicios/descargar_inventario_disponible/"+fecha;
      console.info(url);
      window.location.href = url;
    }
    else{
      alert("Ingrese la fecha que desea descargar")
    }
  }

}

interface Inventory{
  item:string,
  on_hand:string,
  in_transit:string,
  allocated:string,
  suspense:string,
  requested:string,
  quantity:string,
  date_time:string
}
