import { HttpClient } from '@angular/common/http';
import { Injectable } from "@angular/core";

@Injectable()
export class ArticulosService {

    private articulos: Articulo[] = [];

    constructor(private http: HttpClient){
        this.http.get("http://192.168.84.108:8080/servicios/articles")
             .subscribe(articulosJson => {
              console.log(articulosJson);
             });
    }

    getArticulos(): Articulo[] {
        return this.articulos;
    }
}

export interface Articulo{
    sku: string,
    descripcionSku: string,
    codigoSat: string,
    codigoProveedor: string,
    proveedor: string,
    unidadMedidaCompra: string,
    claveUnidad: string,
    pesoArticulo: string,
    itemsUnidadCompra: string,
    cantidadPaquete: string
}
