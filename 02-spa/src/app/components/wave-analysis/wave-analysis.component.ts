import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-wave-analysis',
  templateUrl: './wave-analysis.component.html'
})
export class WaveAnalysisComponent implements OnInit {

  waveNum:string='';

  waves:Wave[]=[];

  constructor(private http: HttpClient) { }

  ngOnInit(): void {
  }

  buscarOla(waveNum:string){
    this.http.get("http://192.168.84.108:8080/servicios/wave_analysis/"+waveNum)
    .subscribe((data: any) => {
     this.waves=data;
     if(this.waves.length>0)
     {
       this.waveNum=waveNum;
     }
     else
     {
       this.waveNum='';
     }
    });
  }
}

interface Wave
{
  item: string,
  description: string,
  storageTemplate: string,
  shipmentId: string,
  launchNum: string,
  status: string,
  requestedQty: string,
  allocatedQty: string,
  av: string,
  oh: string,
  al: string,
  it: string,
  su: string,
  customer: string,
  itemCategory: string,
  creationDateTimeStamp: string,
  scheduledShipDate: string,
  division: string,
  conv: string,
}
