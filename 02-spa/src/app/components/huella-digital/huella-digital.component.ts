import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-huella-digital',
  templateUrl: './huella-digital.component.html'
})
export class ConsultHuella implements OnInit {

  huellas:HuellaDigital[]=[];

  constructor(private http: HttpClient){
      this.http.get("http://192.168.84.108:8080/servicios/huella_digital/")
         .subscribe((data: any) => {
          console.log(data);
          this.huellas=data;
         });
  }

  ngOnInit(): void {
  }

}

interface HuellaDigital{
  frozenFor: string,
  itemCode: string,
  itemName: string,
  familia: string,
  bcdCode: string,
  u_sys_alto: string,
  u_sys_anch: string,
  u_sys_long: string,
  u_sys_peso: string,
  u_sys_volu: string
}
