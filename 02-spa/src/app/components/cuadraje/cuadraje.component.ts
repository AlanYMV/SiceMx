import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-cuadraje',
  templateUrl: './cuadraje.component.html',
})
export class CuadrajeComponent implements OnInit {

  diferenciasReciboSap:ReciboSap[]=[];
  diferenciasPedidoSap:PedidoSap[]=[];
  recibosSap:ReciboSap[]=[];
  pedidosSap:PedidoSap[]=[];
  recibosSapAjustes:ReciboSap[]=[];
  pedidosSapAjustes:PedidoSap[]=[];
  cuadrajes:Cuadraje[]=[];
  tiendasPendientes:TiendaPendiente[]=[];
  pedidosAbiertos:string='';
  pedidosAbiertosNum:string='';
  recibosTotal:string='';
  pedidosTotal:string='';
  recibosOk:string='';
  pedidosOk:string='';
  recibosQty:string='';
  pedidosQty:string='';
  recibosCloseErp:string='';
  pedidosCloseErp:string='';
  recibosRev:string='';
  pedidosRev:string='';

  constructor(private http: HttpClient) 
  { 
    this.http.get("http://192.168.84.108:8080/servicios/cuadraje/")
    .subscribe((data: any) => {
      this.cuadrajes=data;
      if(this.cuadrajes.length>0)
      {
        this.pedidosAbiertos=this.cuadrajes[0].pedidosAbiertos;
        this.pedidosAbiertosNum=this.cuadrajes[0].pedidosAbiertosNum;
        this.recibosTotal =this.cuadrajes[0].recibosTotal;
        this.pedidosTotal =this.cuadrajes[0].pedidosTotal;
        this.recibosOk =this.cuadrajes[0].recibosOk;
        this.pedidosOk =this.cuadrajes[0].pedidosOk;
        this.recibosQty =this.cuadrajes[0].recibosQty;
        this.pedidosQty =this.cuadrajes[0].pedidosQty;
        this.recibosCloseErp =this.cuadrajes[0].recibosCloseErp;
        this.pedidosCloseErp =this.cuadrajes[0].pedidosCloseErp;
        this.recibosRev =this.cuadrajes[0].recibosRev;
        this.pedidosRev =this.cuadrajes[0].pedidosRev;
      }
    });
    this.http.get("http://192.168.84.108:8080/servicios/pendiente_semana/")
    .subscribe((data: any) => {
      this.tiendasPendientes=data;
    });
  }

  actualizarCuadraje()
  {
    this.pedidosAbiertos='';
    this.pedidosAbiertosNum='';
    this.recibosTotal ='';
    this.pedidosTotal ='';
    this.recibosOk ='';
    this.pedidosOk ='';
    this.recibosQty ='';
    this.pedidosQty ='';
    this.recibosCloseErp ='';
    this.pedidosCloseErp ='';
    this.recibosRev ='';
    this.pedidosRev ='';
    this.tiendasPendientes=[];
    this.diferenciasReciboSap=[];
    this.diferenciasPedidoSap=[];
    this.recibosSap=[];
    this.pedidosSap=[];
    this.recibosSapAjustes=[];
    this.pedidosSapAjustes=[];
  

    this.http.get("http://192.168.84.108:8080/servicios/execute_cuadraje/")
    .subscribe((data: any) => 
    {
      this.http.get("http://192.168.84.108:8080/servicios/cuadraje/")
      .subscribe((data: any) => {
        this.cuadrajes=data;
        if(this.cuadrajes.length>0)
          {
            this.pedidosAbiertos=this.cuadrajes[0].pedidosAbiertos;
            this.pedidosAbiertosNum=this.cuadrajes[0].pedidosAbiertosNum;
            this.recibosTotal =this.cuadrajes[0].recibosTotal;
            this.pedidosTotal =this.cuadrajes[0].pedidosTotal;
            this.recibosOk =this.cuadrajes[0].recibosOk;
            this.pedidosOk =this.cuadrajes[0].pedidosOk;
            this.recibosQty =this.cuadrajes[0].recibosQty;
            this.pedidosQty =this.cuadrajes[0].pedidosQty;
            this.recibosCloseErp =this.cuadrajes[0].recibosCloseErp;
            this.pedidosCloseErp =this.cuadrajes[0].pedidosCloseErp;
            this.recibosRev =this.cuadrajes[0].recibosRev;
            this.pedidosRev =this.cuadrajes[0].pedidosRev;
          }
          
      });
      this.http.get("http://192.168.84.108:8080/servicios/pendiente_semana/")
      .subscribe((data: any) => {
        this.tiendasPendientes=data;
      });
    });
  }

  actualizardiferencias()
  {
    this.pedidosAbiertos='';
    this.pedidosAbiertosNum='';
    this.recibosTotal ='';
    this.pedidosTotal ='';
    this.recibosOk ='';
    this.pedidosOk ='';
    this.recibosQty ='';
    this.pedidosQty ='';
    this.recibosCloseErp ='';
    this.pedidosCloseErp ='';
    this.recibosRev ='';
    this.pedidosRev ='';
    this.tiendasPendientes=[];
    this.diferenciasReciboSap=[];
    this.diferenciasPedidoSap=[];
    this.recibosSap=[];
    this.pedidosSap=[];
    this.recibosSapAjustes=[];
    this.pedidosSapAjustes=[];
  
    this.http.get("http://192.168.84.108:8080/servicios/update_diferencias/")
    .subscribe((data: any) => 
    {
      this.http.get("http://192.168.84.108:8080/servicios/cuadraje/")
      .subscribe((data: any) => {
        this.cuadrajes=data;
        if(this.cuadrajes.length>0)
          {
            this.pedidosAbiertos=this.cuadrajes[0].pedidosAbiertos;
            this.pedidosAbiertosNum=this.cuadrajes[0].pedidosAbiertosNum;
            this.recibosTotal =this.cuadrajes[0].recibosTotal;
            this.pedidosTotal =this.cuadrajes[0].pedidosTotal;
            this.recibosOk =this.cuadrajes[0].recibosOk;
            this.pedidosOk =this.cuadrajes[0].pedidosOk;
            this.recibosQty =this.cuadrajes[0].recibosQty;
            this.pedidosQty =this.cuadrajes[0].pedidosQty;
            this.recibosCloseErp =this.cuadrajes[0].recibosCloseErp;
            this.pedidosCloseErp =this.cuadrajes[0].pedidosCloseErp;
            this.recibosRev =this.cuadrajes[0].recibosRev;
            this.pedidosRev =this.cuadrajes[0].pedidosRev;
          }
          
      });
      this.http.get("http://192.168.84.108:8080/servicios/pendiente_semana/")
      .subscribe((data: any) => {
        this.tiendasPendientes=data;
      });
    });
  }

  buscarDiferenciasRecibos(tipoDiferenciaRecibo: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/recibo_sap_valor/"+tipoDiferenciaRecibo)
    .subscribe((data: any) => {
      this.diferenciasReciboSap=data;
    });
  }

  buscarDiferenciasPedidos(tipoDiferenciaPedido: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/pedido_sap_valor/"+tipoDiferenciaPedido)
    .subscribe((data: any) => {
      this.diferenciasPedidoSap=data;
    });
  }

  buscarRecibos(recibos: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/recibo_sap/"+recibos)
    .subscribe((data: any) => {
      this.recibosSap=data;
    });
  }

  buscarPedidos(pedidos: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/pedido_sap/"+pedidos)
    .subscribe((data: any) => {
      this.pedidosSap=data;
    });
  }

  buscarRecibosAjuste(recibos: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/recibo_sap/"+recibos)
    .subscribe((data: any) => {
      this.recibosSapAjustes=data;
    });
  }

  buscarPedidosAjuste(pedidos: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/pedido_sap/"+pedidos)
    .subscribe((data: any) => {
      this.pedidosSapAjustes=data;
    });
  }

  insertSapReceiptVal(idReceipt: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/insert_sapreceipt/"+idReceipt)
    .subscribe((data: any) => {
      this.pedidosSapAjustes=data;
    });
  }

  insertSapShipmentVal(idShipment: string)
  {
    this.http.get("http://192.168.84.108:8080/servicios/insert_sapshipment/"+idShipment)
    .subscribe((data: any) => {
      this.pedidosSapAjustes=data;
    });
  }

  ngOnInit(): void {
  }

}

interface ReciboSap
{
  docSDT: string,
  closeQtySdt: string,
  closeQtyTr: string,
  openQtySdt: string,
  openQtyTr: string,
  totalQtySdt: string,
  totalQtyTr: string,
  wms: string,
  dif: string,
  closeDate: string,
  stsWms: string,
  val: string,
}

interface PedidoSap
{
  docSDT: string,
  closeQtySdt: string,
  closeQtyTr: string,
  openQtySdt: string,
  openQtyTr: string,
  totalQtySdt: string,
  totalQtyTr: string,
  wmsClose: string,
  dif: string,
  shipDate: string,
  stsWms: string,
  val: string,
  openSap: string, 
}

interface Cuadraje
{
  recibosTotal: string,
  recibosOk: string,
  recibosQty: string,
  recibosCloseErp: string,
  recibosRev: string,
  recibosTotalNum: string,
  recibosOkNum: string,
  recibosQtyNum: string,
  recibosCloseErpNum: string,
  recibosRevNum: string,
  pedidosTotal: string,
  pedidosOk: string,
  pedidosQty: string,
  pedidosCloseErp: string,
  pedidosRev: string,
  pedidosTotalNum: string,
  pedidosOkNum: string,
  pedidosQtyNum: string,
  pedidosCloseErpNum: string,
  pedidosRevNum: string,
  pedidosAbiertos: string,
  pedidosAbiertosNum: string,
}

interface TiendaPendiente
{
  fecha: string,
  shipDate: string,
  numeroRegistros: string,
  piezas: string,
  reetiquetado: string, 
}