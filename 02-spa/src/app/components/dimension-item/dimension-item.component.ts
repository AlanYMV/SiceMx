import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-dimension-item',
  templateUrl: './dimension-item.component.html'
}) 
export class DimensionItem implements OnInit 
{
  resultMessage: string = '';

  constructor(private http: HttpClient) { }

  ngOnInit(): void { }

  onFileChange(action: 'update') {
    const fileInput = document.getElementById('fileInputUpdate') as HTMLInputElement;
    if (!fileInput.files?.length) {
        alert('Por favor, selecciona un archivo.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const headers = new HttpHeaders();
    const url = 'http://192.168.84.108:8080/servicios/actualizar_dimensiones_mx/';

    this.http.post(url, formData, {
        headers,
        responseType: 'blob', 
        observe: 'response'   
    }).subscribe({
        next: (response: HttpResponse<Blob>) => {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
                const contentDisposition = response.headers.get('content-disposition');
                const fileName = contentDisposition ? contentDisposition.split('filename=')[1] : 'resultado_actualizacion.xlsx';

                const blob = new Blob([response.body!], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                this.resultMessage = 'Actualización completada con éxito.';
                alert(this.resultMessage);  
            } else {
                const reader = new FileReader();
                reader.onload = () => {
                    this.resultMessage = reader.result as string;
                    alert(this.resultMessage);  
                };
                reader.readAsText(response.body!);
            }
        },
        error: (err: any) => {
            const reader = new FileReader();
            reader.onload = () => {
                this.resultMessage = reader.result as string;
                alert(this.resultMessage);  
            };
            reader.readAsText(err.error); 
            console.error('Error al procesar el archivo:', err);
        }
    });
  }
}