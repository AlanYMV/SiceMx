import { HttpClient } from '@angular/common/http';
import { Component, OnInit, ElementRef } from '@angular/core';

@Component({
  selector: 'app-item-location',
  templateUrl: './item-location.component.html',
})
export class ItemLocation implements OnInit {

  itemLs: ItemL[] = [];

  constructor(private http: HttpClient, private el: ElementRef) {
    this.http.get('http://192.168.84.108:8080/servicios/articulos_ubicacion').subscribe((data: any) => {
      console.log(data);
      this.itemLs = data;
      console.log(this.itemLs[0]);
    });
  }

  ngOnInit(): void {
  }

  descargarConFecha() {
    const fechaInput: HTMLInputElement | null = this.el.nativeElement.querySelector('#fecha');
    if (!fechaInput) {
        alert('No se encontró el campo de fecha.');
        return;
    }

    const fechaValue: string = fechaInput.value.trim();

    if (!fechaValue) {
        alert('Por favor, ingrese una fecha.');
        return;
    }
    const url: string = "http://192.168.84.108:8080/servicios/descargar_articulos_ubicacion/" + fechaValue;
    console.info(url);
    window.location.href = url;
  }
}

interface ItemL {
  id: string;
  item: string;
  location: string;
  found: string;
  date: string;
}
