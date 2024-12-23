import { HttpClient, HttpHeaders, HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-container-type-up',
  templateUrl: './container-type-up.component.html'
})
export class ContainerTypeUp implements OnInit {
  resultMessage: string = '';

  constructor(private http: HttpClient) { }

  ngOnInit(): void { }

  onFileChange(action: 'add' | 'delete') {
    const fileInput = document.getElementById(action === 'add' ? 'fileInputAdd' : 'fileInputDelete') as HTMLInputElement;
    if (!fileInput.files?.length) {
        alert('Por favor, selecciona un archivo.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const headers = new HttpHeaders();
    const url = action === 'add' ? 'http://192.168.84.108:8080/servicios/registrar_contenedores_mx/' : 'http://192.168.84.108:8080/servicios/eliminar_contenedores_mx/';

    this.http.post(url, formData, {
        headers,
        responseType: 'blob',
        observe: 'response'
    }).subscribe({
        next: (response: HttpResponse<Blob>) => {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')) {
                const contentDisposition = response.headers.get('content-disposition');
                const fileName = contentDisposition ? contentDisposition.split('filename=')[1] : (action === 'add' ? 'resultado_inserciones.xlsx' : 'resultado_eliminaciones.xlsx');

                const blob = new Blob([response.body!], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = fileName;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                document.body.removeChild(a);

                this.resultMessage = action === 'add' ? 'Registro completado con éxito.' : 'Eliminación completada con éxito.';
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