import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-storage',
  templateUrl: './storage.component.html'
})
export class StorageComponent implements OnInit {

  storages:Storage[]=[];


  constructor(private http: HttpClient){
      this.http.get("http://192.168.84.108:8080/servicios/storage_template")
         .subscribe((data: any) => {
          console.log(data);
          this.storages=data;
          console.log(this.storages[0]);
         });
  }
  
  ngOnInit(): void {
  }
}

interface Storage{
  itemCode: string,
  storageTemplate: string,
  salUnitMsr: string,
  familia: string,
  subFamilia: string,
  subSubFamilia: string,
  uSysCat4: string,
  uSysCat5: string,
  uSysCat6: string,
  uSysCat7: string,
  uSysCat8: string,
  height: string,
  width: string,
  length: string,
  volume: string,
  weight: string,
}
