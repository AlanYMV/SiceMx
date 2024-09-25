import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-split',
  templateUrl: './split.component.html',
})
export class SplitComponent implements OnInit {

  numSplits : number=1;

  splits:Split[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarSplits(fecha:string){
    console.log(fecha);
    this.http.get("http://192.168.84.108:8080/servicios/split/"+fecha)
    .subscribe((data: any) => {
     this.splits=data;
     console.log(this.splits.length);
     this.numSplits=this.splits.length;
    });
  }

}

interface Split{
  pedido: string,
  contenedor: string,
  fechaCreacion: string,
  numeroPiezas: string,
  status: string,
  usuario: string,
}
