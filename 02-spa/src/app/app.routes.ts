import { RouterModule, Routes } from "@angular/router";
import { HomeComponent } from "./components/home/home.component";
import { AboutComponent } from "./components/about/about.component";
import { HeroesComponent } from "./components/heroes/heroes.component";
import { ArticulosComponent } from "./components/articulos/articulos.component";
import { PedidosComponent } from "./components/pedidos/pedidos.component";
import { CargasComponent } from "./components/cargas/cargas.component";
import { StorageComponent } from "./components/storage/storage.component";
import { PreciosComponent } from "./components/precios/precios.component";
import { InventarioComponent } from "./components/inventario/inventario.component";
import { RecibosComponent } from "./components/recibos/recibos.component";
import { SplitComponent } from "./components/split/split.component";
import { ReporteTiendasComponent } from "./components/reporte-tiendas/reporte-tiendas.component";
import { CuadrajeComponent } from "./components/cuadraje/cuadraje.component";
import { ConetendorEpqComponent } from "./components/conetendor-epq/conetendor-epq.component";
import { ReciboTiendaComponent } from "./components/recibo-tienda/recibo-tienda.component";
import { PedidoPlaneacionComponent } from "./components/pedido-planeacion/pedido-planeacion.component"
import { UbicacionesVaciasComponent } from "./components/ubicaciones-vacias/ubicaciones-vacias.component";
import { EstatusOlaComponent } from "./components/estatus-ola/estatus-ola.component"
import { OlaPzaContComponent } from "./components/ola-pza-cont/ola-pza-cont.component"
import { DetalleOlaComponent } from "./components/detalle-ola/detalle-ola.component"
import { LineasOlaComponent } from "./components/lineas-ola/lineas-ola.component";
import { DownloadsComponent } from "./components/downloads/downloads.component";
import { DownloadsAlmacenComponent } from "./components/downloads-almacen/downloads-almacen.component"
import { PorcentajeComponent } from "./components/porcentaje/porcentaje.component";
import { DownloadInventarioComponent } from "./components/download-inventario/download-inventario.component";
import { WaveAnalysisComponent } from "./components/wave-analysis/wave-analysis.component";
import { PedimentoComponent } from "./components/pedimento/pedimento.component";
import { PesoContenedorComponent } from "./components/peso-contenedor/peso-contenedor.component";
import { DownloadsContainerQc } from "./components/container-qc/container-qc.component";
import { ConfirmPending } from "./components/confirmacion-pendientes/confirmacion-pendientes.component";
import { ColsultKardex } from "./components/kardex/consult-kardex.component";

const APP_ROUTES : Routes = [
    { path:'home', component: HomeComponent},
    { path:'about', component: AboutComponent},
    { path:'heroes', component: HeroesComponent},
    { path:'articulos', component: ArticulosComponent},
    { path:'pedidos', component: PedidosComponent},
    { path:'cargas', component: CargasComponent},
    { path:'precios', component: PreciosComponent},
    { path:'storage', component: StorageComponent},
    { path:'inventario', component: InventarioComponent},
    { path:'recibos', component: RecibosComponent},
    { path:'split', component: SplitComponent},
    { path:'reporte-tiendas', component: ReporteTiendasComponent},
    { path:'cuadraje', component: CuadrajeComponent},
    { path:'contenedoresEpq', component: ConetendorEpqComponent},
    { path:'recibosTienda', component: ReciboTiendaComponent},
    { path:'pedidoPlaneacion', component: PedidoPlaneacionComponent},
    { path:'ubicacionVacia', component: UbicacionesVaciasComponent},
    { path:'estatusOla', component: EstatusOlaComponent},
    { path:'olaPzaCont', component: OlaPzaContComponent},
    { path:'detalleOla/:numOla', component: DetalleOlaComponent},
    { path:'lineasOla', component: LineasOlaComponent},
    { path:'downloads', component: DownloadsComponent},
    { path:'downloadsAlmacen', component: DownloadsAlmacenComponent},
    { path:'porcentaje', component: PorcentajeComponent},
    { path:'downloadInventario', component: DownloadInventarioComponent},
    { path:'waveAnalysis', component: WaveAnalysisComponent},
    { path:'pedimentos', component: PedimentoComponent},
    { path:'pesoContenedor', component: PesoContenedorComponent},
    { path:'containerQc',component: DownloadsContainerQc},
    { path:'confirmacion-pendientes', component: ConfirmPending},
    { path:'consult-kardex', component: ColsultKardex},
    { path:'**', pathMatch: 'full', redirectTo: 'home'}
];

export const APP_ROUTING = RouterModule.forRoot(APP_ROUTES, {useHash: true});
