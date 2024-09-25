import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-ubicaciones-vacias',
  templateUrl: './ubicaciones-vacias.component.html'
})
export class UbicacionesVaciasComponent implements OnInit
{
  ubicacionesVacias:UbicacionVacia[]=[];

  constructor(private http: HttpClient)
  {
    this.http.get("http://192.168.84.108:8080/servicios/ubicaciones_vacias")
       .subscribe((data: any) => {
        console.log(data);
        this.ubicacionesVacias=data;
       });
  }


  ngOnInit(): void {
  }

}

interface UbicacionVacia{
  ubicacion: string,
  status: string,
  active: string,
}
