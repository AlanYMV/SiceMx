import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-shorpack',
  templateUrl: './shorpack.component.html'
})
export class ShorpackDay implements OnInit {

  shorpacks:Shorpack[]=[];
  Dt = '';

  constructor(private http: HttpClient) {
    this.Dt = this.dateToday()
    this.http.get('http://192.168.84.108:8080/servicios/shorpack/'+this.Dt).subscribe((data: any) => {
      console.log(data);
      this.shorpacks = data;
    });}

  ngOnInit(): void {
  }
  dateToday(): string {
    var today = new Date();
    var dd = String(today.getDate()).padStart(2, '0');
    var mm = String(today.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = today.getFullYear();
    var todayDate = '';

    todayDate = ''+ dd + '-' + mm + '-' + yyyy+'';
    console.log(todayDate);
    return todayDate
  }
  searchShorpacks(fecha:string){
    // console.log(fecha)
    if (fecha){
      this.http.get('http://192.168.84.108:8080/servicios/shorpack/'+fecha).subscribe((data: any) => {
        console.log(data);
        this.shorpacks = data;
      });
    }
    else{
      alert("Ingrese la fecha que desea buscar")
    }
  }
  downloadShorpacks(fecha:string){
    console.log(fecha)
    if (fecha){
      const url: string = "http://192.168.84.108:8080/servicios/descargar_shorpack/"+fecha;
      console.info(url);
      window.location.href = url;
    }
    else{
      alert("Ingrese la fecha que desea descargar")
    }
  }

}

interface Shorpack{
  pickWaveCode:string,
  clientCode:string,
  productCode:string,
  documentCode:string,
  request_qty:string,
  total_qty:string,
  rechazadas:string,
  pzasFaltantes:string,
  fecha:string
}
