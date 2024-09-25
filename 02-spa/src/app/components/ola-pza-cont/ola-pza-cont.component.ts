import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-ola-pza-cont',
  templateUrl: './ola-pza-cont.component.html'
})

export class OlaPzaContComponent implements OnInit
{

  olasPzaCont:OlaPzaCont[]=[];

  constructor(private http: HttpClient)
  {
    this.http.get("http://192.168.84.108:8080/servicios/ola_pza_cont")
       .subscribe((data: any) => {
        console.log(data);
        this.olasPzaCont=data;
       });
  }

  ngOnInit(): void {
  }

}

interface OlaPzaCont{
  ola: string,
  numPiezas: string,
  numContenedores: string
}
