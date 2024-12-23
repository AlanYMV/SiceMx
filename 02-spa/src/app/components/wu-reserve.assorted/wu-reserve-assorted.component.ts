import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-wu-reserve-assorted',
  templateUrl: './wu-reserve-assorted.component.html'
})
export class WUReserveAssorted implements OnInit {

  reserveNum:string='';

  reserveAssorteds:ReserveAssorted[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarUnidad(launch_num:string){
    this.http.get("http://192.168.84.108:8080/servicios/unidad_trabajo_surtido_reserva/"+launch_num)
    .subscribe((data: any) => {
     this.reserveAssorteds=data;
     if(this.reserveAssorteds.length>0)
     {
       this.reserveNum=launch_num;
     }
     else
     {
       this.reserveNum='';
     }
    });
  }
}

interface ReserveAssorted
{
  container_id: string,
  container_type: string,
  work_unit: string,
  from_loc: string,
  item: string,
  quantity: string
}
