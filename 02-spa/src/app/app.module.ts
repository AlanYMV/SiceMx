import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

/*Rutas*/
import { APP_ROUTING } from './app.routes';

import { HttpClientModule } from '@angular/common/http';

/** Servicios */
import { HeroesService } from './servicios/heroes.service';

/*Componentes*/
import { AppComponent } from './app.component';
import { NavbarComponent } from './components/shared/navbar/navbar.component';
import { HomeComponent } from './components/home/home.component';
import { AboutComponent } from './components/about/about.component';
import { HeroesComponent } from './components/heroes/heroes.component';
import { ArticulosComponent } from './components/articulos/articulos.component';
import { PedidosComponent } from './components/pedidos/pedidos.component';
import { CargasComponent } from './components/cargas/cargas.component';
import { StorageComponent } from './components/storage/storage.component';
import { PreciosComponent } from './components/precios/precios.component';
import { InventarioComponent } from './components/inventario/inventario.component';
import { RecibosComponent } from './components/recibos/recibos.component';
import { SplitComponent } from './components/split/split.component';
import { ReporteTiendasComponent } from './components/reporte-tiendas/reporte-tiendas.component';
import { CuadrajeComponent } from './components/cuadraje/cuadraje.component';
import { ConetendorEpqComponent } from './components/conetendor-epq/conetendor-epq.component';
import { ReciboTiendaComponent } from './components/recibo-tienda/recibo-tienda.component';
import { PedidoPlaneacionComponent } from './components/pedido-planeacion/pedido-planeacion.component';
import { UbicacionesVaciasComponent } from './components/ubicaciones-vacias/ubicaciones-vacias.component';
import { EstatusOlaComponent } from './components/estatus-ola/estatus-ola.component';
import { OlaPzaContComponent } from './components/ola-pza-cont/ola-pza-cont.component';
import { DetalleOlaComponent } from './components/detalle-ola/detalle-ola.component';
import { LineasOlaComponent } from './components/lineas-ola/lineas-ola.component';
import { DownloadsComponent } from './components/downloads/downloads.component';
import { DownloadsAlmacenComponent } from './components/downloads-almacen/downloads-almacen.component';
import { PorcentajeComponent } from './components/porcentaje/porcentaje.component';
import { DownloadInventarioComponent } from './components/download-inventario/download-inventario.component';
import { WaveAnalysisComponent } from './components/wave-analysis/wave-analysis.component';
import { PedimentoComponent } from './components/pedimento/pedimento.component';
import { PesoContenedorComponent } from './components/peso-contenedor/peso-contenedor.component';
import { ConfirmPending } from './components/confirmacion-pendientes/confirmacion-pendientes.component';
import { ColsultKardex } from './components/kardex/consult-kardex.component';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    AboutComponent,
    HeroesComponent,
    ArticulosComponent,
    PedidosComponent,
    CargasComponent,
    StorageComponent,
    PreciosComponent,
    InventarioComponent,
    RecibosComponent,
    SplitComponent,
    ReporteTiendasComponent,
    CuadrajeComponent,
    ConetendorEpqComponent,
    ReciboTiendaComponent,
    PedidoPlaneacionComponent,
    UbicacionesVaciasComponent,
    EstatusOlaComponent,
    OlaPzaContComponent,
    DetalleOlaComponent,
    LineasOlaComponent,
    DownloadsComponent,
    DownloadsAlmacenComponent,
    PorcentajeComponent,
    DownloadInventarioComponent,
    WaveAnalysisComponent,
    PedimentoComponent,
    PesoContenedorComponent,
    ConfirmPending,
    ColsultKardex
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    APP_ROUTING
  ],
  providers: [HeroesService],
  bootstrap: [AppComponent]
})
export class AppModule { }
