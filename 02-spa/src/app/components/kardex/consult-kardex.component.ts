import { HttpClient } from '@angular/common/http';
import { Component, OnInit ,ViewChild} from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';

@Component({
  selector: 'app-consult-kardex',
  templateUrl: './consult-kardex.component.html'
})
export class ColsultKardex implements OnInit {

  transactions: Transaction[]=[];
  kardexs:Kardex[]=[];
  formulario: FormGroup;
  selectedTransaction: string | null = null;

  constructor(private http: HttpClient) { 
    this.formulario = new FormGroup({
      transactions: new FormControl('')
    });}

  ngOnInit(): void {
      this.http.get("http://192.168.84.108:8080/servicios/descripcion_transacciones/")
      .subscribe((data: any) => {
          this.transactions = data;
          console.log('Tiendas:', this.transactions);
    });
  }
  
    onTransactionChange(event: Event): void {
      const target = event.target as HTMLSelectElement;
      const value = target?.value;
      if (value !== null && value !== undefined && value !== " " && value !== "Tipo de transaccion") {
        this.selectedTransaction = value;
      } else {
        this.selectedTransaction = null;
      }
    }
    
    buscarKardex(item: string, container_id?: string, location?: string, user_stamp?: string, work_type?: string, fechaInicio?: string, fechaFin?: string) {
        let url = `http://192.168.84.108:8080/servicios/consult_kardex/`;

        url += `${item || ''}/`;
        url += `${container_id || ''}/`;
        url += `${location || ''}/`;
        url += `${user_stamp || ''}/`;
        url += `${work_type || ''}/`;
        url += `${fechaInicio || ''}/`;
        url += `${fechaFin || ''}/`;
        console.log(this.selectedTransaction)
        console.log(url)
        url += `${this.selectedTransaction || ''}/`;

        this.http.get(url)
            .subscribe((data: any) => {
                this.kardexs = data;
            });
      
    }



      messageDiv = document.getElementById('message') as HTMLDivElement;

      downloadKardex(item: string, container_id?: string, location?: string, user_stamp?: string, work_type?: string, fechaInicio?: string, fechaFin?: string) {
        let url = `http://192.168.84.108:8080/servicios/download_kardex/`;
        
        console.log(this.selectedTransaction)
        console.log(url)

        url += `${item || ''}/`;
        url += `${container_id || ''}/`;
        url += `${location || ''}/`;
        url += `${user_stamp || ''}/`;
        url += `${work_type || ''}/`;
        url += `${fechaInicio || ''}/`;
        url += `${fechaFin || ''}/`;
        url += `${this.selectedTransaction || ''}/`;
        

        return url;
      };

      async fetchKardexDownload(url: string) {
        try {
          const response = await fetch(url, { method: 'GET' });
    
          if (!response.ok) {
            throw new Error("Error");
          }
    
          const contentType = response.headers.get("content-type");
          if (contentType && contentType.includes("application/json")) {
            const jsonResponse = await response.json();
            alert("No se cumple con las condiciones \nSi son mas de 10,000 registros intente despues de las 10 de la noche \nPara no comprometer al servidor y a los demas usuarios")
            return;
          }
    
          const blob = await response.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.style.display = 'none';
          a.href = downloadUrl;
          a.download = 'Kardex.xlsx';
          document.body.appendChild(a);
          a.click();
          window.URL.revokeObjectURL(downloadUrl);
        } catch (error) {
          alert("Error al tratar de descargar")
        }
      }
    
      onDownloadClick(item: string, container_id: string, location: string, user_stamp: string, work_type: string, fechaInicio: string, fechaFin: string) {
        const url = this.downloadKardex(item, container_id, location, user_stamp, work_type, fechaInicio, fechaFin);
        this.fetchKardexDownload(url);
      }
  }

  

interface Kardex{
  item: string,
  location : string,
  date_stamp: string,
  user_tamp: string,
  quantity: string,
  before_on_hand_qty: string,
  after_on_hand_qty: string,
  before_in_transit_qty: string,
  after_in_transit_qty: string,
  before_alloc_qty: string,
  after_alloc_qty: string
}

interface Transaction{
  identifier: string,
  description: string
}