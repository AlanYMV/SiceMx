import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-prices-promotions',
  templateUrl: './prices-promotions.component.html'
})
export class PricePromotion implements OnInit {
  private url = 'http://192.168.84.108:8080/servicios/precio_promociones/';
  selectedFile: File | null = null;

  constructor(private http: HttpClient) {}

  ngOnInit(): void {
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }

  sendExcel(): void {
    if (!this.selectedFile) {
      console.error('No file selected');
      return;
    }

    const formData: FormData = new FormData();
    formData.append('file', this.selectedFile, this.selectedFile.name);

    const headers = new HttpHeaders();
    headers.append('Accept', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet');

    this.http.post(this.url, formData, { headers: headers, responseType: 'blob' })
      .subscribe(response => {
        const contentType = response.type;
        if (contentType === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet') {
          const blob = new Blob([response], { type: contentType });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'promociones_resultados.xlsx';
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        } else {
          const reader = new FileReader();
          reader.onload = (e: any) => {
            const jsonResponse = JSON.parse(e.target.result);
            console.log(jsonResponse);
          };
          reader.readAsText(response);
        }
      }, error => {
        console.error('Error uploading file:', error);
      });
  }
}