import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-inventario',
  templateUrl: './inventario.component.html'
})
export class InventarioComponent implements OnInit {

  inventarioItems:InventarioItem[]=[];
  wmsErpInventories:WmsErpInventory[]=[];
  wmsInventories:WmsInventory[]=[];
  inventoryTops:InventoryTop[]=[];
  detallesErpWms:DetalleErpWms[]=[];

  constructor(private http: HttpClient){
      this.http.get("http://192.168.84.108:8080/servicios/inventario_wmserp")
         .subscribe((data: any) => {
          console.log(data);
          this.wmsErpInventories=data;
         });
      this.http.get("http://192.168.84.108:8080/servicios/inventario_items")
         .subscribe((data: any) => {
          console.log(data);
          this.inventarioItems=data;
         });
      this.http.get("http://192.168.84.108:8080/servicios/inventario_wms")
         .subscribe((data: any) => {
          console.log(data);
          this.wmsInventories=data;
         });
      this.http.get("http://192.168.84.108:8080/servicios/top_one_hundred")
         .subscribe((data: any) => {
          console.log(data);
          this.inventoryTops=data;
         });
  }

  buscarItem(item: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/inventario_detalle_wmserp/"+item)
         .subscribe((data: any) => {
          console.log(data);
          this.detallesErpWms=data;
         });
  }

  actualizarInventario()
  {
    this.inventarioItems=[];
    this.wmsErpInventories=[];
    this.wmsInventories=[];
    this.inventoryTops=[];

    this.http.get("http://192.168.84.108:8080/servicios/execute_inventario/").subscribe((data: any) => 
    {
      this.http.get("http://192.168.84.108:8080/servicios/inventario_wmserp").subscribe((data: any) => 
      {
        this.wmsErpInventories=data;
      });
      this.http.get("http://192.168.84.108:8080/servicios/inventario_items").subscribe((data: any) => 
      {
        this.inventarioItems=data;
      });
      this.http.get("http://192.168.84.108:8080/servicios/inventario_wms").subscribe((data: any) => 
      {
        this.wmsInventories=data;
      });
      this.http.get("http://192.168.84.108:8080/servicios/top_one_hundred").subscribe((data: any) => 
      {
        console.log(data);
        this.inventoryTops=data;
      });
    });
  }

  ngOnInit(): void {
  }

}

interface InventarioItem{
  warehouse: string,
  wmsOnHand: string,
  erpOnHand: string,
  numItems: string,
}

interface WmsErpInventory{
  warehouse: string,
  wmsOnHand: string,
  erpOnHand: string,
  diferencia: string,
  diferenciaAbsoluta: string,
  wmsInTransit: string,
  numItemsWms: string,
  numItemsErp: string,
  numItemsDif: string,
}

interface WmsInventory{
  warehouseCode: string,
  solicitado: string,
  onHand: string,
  comprometido: string,
  disponible: string,
  skuSolicitado: string,
  skuOnHand: string,
  skuComprometido: string,
  fechaActualizacion: string,
}

interface DetalleErpWms{
  fecha: string,
  item: string,
  warehouse: string,
  wmsComprometido: string,
  wmsTransito: string,
  wmsOnHand: string,
  erpOnHand: string,
  diferenciaOnHand: string,
  diferenciaOnHandAbsoluta: string,
}

interface InventoryTop{
  fecha: string,
  item: string,
  warehouse: string,
  wmsComprometido: string,
  wmsTransito: string,
  wmsOnHand: string,
  erpOnHand: string,
  difOnHand: string,
  difOnHandAbsolute: string,
}

