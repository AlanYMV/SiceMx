import logging
import pyodbc
from sevicios_app.vo.detallePedidoTienda import DetallePedidoTienda
from sevicios_app.vo.pedidoTienda import PedidoTienda
from sevicios_app.vo.solicitudTraslado import SolicitudTraslado
from sevicios_app.vo.tiendaPendiente import TiendaPendiente
from sevicios_app.vo.tablaTiendaPendiente import TablaTiendaPendiente
from sevicios_app.vo.tiendaPendienteFecha import TiendaPendienteFecha
from sevicios_app.vo.pedidoPorCerrar import PedidoPorCerrar
from sevicios_app.vo.reciboTienda import ReciboTienda
from sevicios_app.vo.tiendaCorreo import TiendaCorreo

logger = logging.getLogger('')

class RecepcionTiendaDao():

    def getConexion(self):
        try:
            direccion_servidor = '192.168.84.23'
            nombre_bd = 'recepciontienda'
            nombre_usuario = 'soportedb'
            password = 'T+Sab!G@(N)'
            conexion = None

            conexion = pyodbc.connect('DRIVER={SQL Server};SERVER=' + direccion_servidor+';DATABASE='+nombre_bd+';UID='+nombre_usuario+';PWD=' + password)
            return conexion
        except Exception as exception:
            logger.error(f"Se presento un error al establecer la conexion: {exception}")
            raise exception

    def closeConexion(self, conexion):
        try:
            conexion.close()
        except Exception as exception:
            logger.error(f"Se presento una incidencia al cerrar la conexion: {exception}")
            raise exception
        
    def executeActualizarTablasTiendas(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cursor.execute("EXEC SP_REPORTE_TIENDAS_DETALLE_PEDIDO")
            conexion.commit()
            cursor.execute("EXEC SP_REPORTE_TIENDAS_STATUS_PEDIDO")
            conexion.commit()
            cursor.execute("EXEC SP_REPORTE_TIENDAS_TRASLADO")
            conexion.commit()
            cursor.execute("EXEC SP_REPORTE_TIENDAS_PENDIENTES")
            conexion.commit()
            return True
        except Exception as exception:
            logger.error(f"Se presento una incidencia al ejecutar el proceso de reporte de tiendas: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getDetallePedido(self, tienda, carga, pedido, contenedor, articulo, estatusContenedor):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            detallePedidoList=[]
            numParametros=0
            consulta="SELECT STS_SOL_NAME, ALMACENNOMBRE, SOLICITUDNOTRANSPORTE, SOLICITUDID, CONTENEDORID, ARTICULOCVE, ARTICULODESC, STS_CONT_NAME, ARTICULOQTY, QC, USUARIO_PICKING, FECHA_PICKING, USUARIO_QC, FECHA_QC from DetallePedidos where"
            if tienda != '':
                consulta=consulta+ " ALMACENNOMBRE LIKE '%"+tienda+"%'"
                numParametros +=1
            if carga != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " SOLICITUDNOTRANSPORTE LIKE '%"+carga+"%'"
                numParametros +=1
            if pedido != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " SOLICITUDID LIKE '%"+pedido+"%'"
                numParametros +=1
            if contenedor != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " CONTENEDORID LIKE '%"+contenedor+"%'"
                numParametros +=1
            if articulo != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " ARTICULOCVE LIKE '%"+articulo+"%'"
            if estatusContenedor != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " STS_CONT_NAME = '"+estatusContenedor+"'"
            print(consulta)                              
            cursor.execute(consulta)
            registros=cursor.fetchall()
            for registro in registros:
                detallePedidoTienda=DetallePedidoTienda(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13])
                detallePedidoList.append(detallePedidoTienda)
            return detallePedidoList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getPedido(self, tienda, carga, pedido):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            pedidoList=[]
            numParametros=0
            consulta="SELECT ANIO, ESTATUS, MES, FECHA_CEDIS, ID_CARGA, TIENDA, PEDIDO, TIPO_PEDIDO, SOLICITUD_TRASLADO, CONTENEDORES_PENDIENTES, CONTENEDORES_RECIBIDOS, ITEMS_PENDIENTES, PIEZAS_PENDIENTES, ITEMS_RECIBIDOS, PIEZAS_RECIBIDAS FROM STATUS_PEDIDO WHERE"
            if tienda != '':
                consulta=consulta+ " TIENDA LIKE '%"+tienda+"%'"
                numParametros +=1
            if carga != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " ID_CARGA LIKE '%"+carga+"%'"
                numParametros +=1
            if pedido != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " PEDIDO LIKE '%"+pedido+"%'"
            logger.error(consulta)    
            cursor.execute(consulta)
            registros=cursor.fetchall()
            for registro in registros:
                pedidoTienda=PedidoTienda(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14])
                pedidoList.append(pedidoTienda)
            return pedidoList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getSolicitudTraslado(self, documento, origenSolicitud, destinoSolicitud, origenTraslado, destinoTraslado):
        try:
            logger.error("acceso dao")
            conexion=self.getConexion()
            cursor=conexion.cursor()
            solicitudTrasladoList=[]
            numParametros=0
            consulta="SELECT DOCUMENTO_SOLICITUD, STATUS, ORIGEN_SOLICITUD, DESTINO_SOLICITUD, ARTICULOS_SOLICITUD, CANTIDAD_SOLICITUD, COMENTARIOS, FECHA_SOLICITUD, FECHA_VENCIMIENTO, ORIGEN_TRASLADO, DESTINO_TRASLADO, ARTICULOS_TRASLADO, CANTIDAD_TRASLADO FROM TRASLADO_SAP WHERE"
            if documento != '':
                consulta=consulta+ " DOCUMENTO_SOLICITUD LIKE '%"+documento+"%'"
                numParametros +=1
            if origenSolicitud != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " ORIGEN_SOLICITUD LIKE '%"+origenSolicitud+"%'"
                numParametros +=1
            if destinoSolicitud != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " DESTINO_SOLICITUD LIKE '%"+destinoSolicitud+"%'"
                numParametros +=1
            if origenTraslado != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " ORIGEN_TRASLADO LIKE '%"+origenTraslado+"%'"
                numParametros +=1
            if destinoTraslado != '':
                if numParametros>0:
                    consulta=consulta+ " AND"
                consulta=consulta+ " DESTINO_TRASLADO LIKE '%"+destinoTraslado+"%'"
            cursor.execute(consulta)
            registros=cursor.fetchall()
            for registro in registros:
                solicitudTraslado=SolicitudTraslado(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12])
                solicitudTrasladoList.append(solicitudTraslado)
            return solicitudTrasladoList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getTiendasPendientes(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tiendaPendienteList=[]
            numParamteros=0
            cursor.execute("SELECT TIPE.SOLICITUD_ESTATUS, TIPE.CARGA, TIPE.PEDIDO, TIPE.NOMBRE_ALMACEN, TIPE.FECHA_EMBARQUE, TIPE.FECHA_PLANEADA, TIPE.TRANSITO, TIPE.CROSS_DOCK, TIPE.FECHA_ENTREGA "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA from TIENDA_PENDIENTE TP) TIPE "+
                           "WHERE TIPE.SOLICITUD_ESTATUS='EN TRANSITO' AND TIPE.FECHA_ENTREGA<=GETDATE() "+
                           "ORDER BY TIPE.FECHA_ENTREGA")
            registros=cursor.fetchall()
            for registro in registros:
                tiendaPendiente=TiendaPendiente(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8])
                tiendaPendienteList.append(tiendaPendiente)
            return tiendaPendienteList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def executeEnvioCorreos(self, tienda):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cursor.execute("EXEC SP_ENVIO_CORREO_TIENDA @Tienda = ?", (tienda))
            conexion.commit()
            return True
        except Exception as exception:
            logger.error(f"Se presento una incidencia al ejecutar el proceso de envio de correos a tiendas tiendas: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getTablaTiendasPendientes(self, fecha):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tablastiendaPendienteList=[]
            numParamteros=0
            cursor.execute("SELECT TIPE.NOMBRE_ALMACEN, MIN(TIPE.FECHA_ENTREGA) FECHA_ENTREGA,  COUNT(TIPE.PEDIDO) NUM_PEDIDOS, SUM(TIPE.TRANSITO+TIPE.CROSS_DOCK) PIEZAS, SUM(TIPE.SolicitudTotalContenedores) CONTENEDORES "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA, SO.SolicitudTotalContenedores "+
                           "from TIENDA_PENDIENTE TP "+
                           "inner join Solicitud SO ON SO.SolicitudNoTransporte=TP.CARGA AND SO.SolicitudID=TP.PEDIDO) TIPE "+ 
                           "WHERE TIPE.SOLICITUD_ESTATUS='EN TRANSITO' AND format(TIPE.FECHA_ENTREGA, 'yyyy-MM-dd')<= ? "+
                           "GROUP BY TIPE.NOMBRE_ALMACEN ORDER BY FECHA_ENTREGA", (fecha))
            registros=cursor.fetchall()
            for registro in registros:
                tablaTiendaPendiente=TablaTiendaPendiente(registro[0], registro[1], registro[2], registro[3], registro[4])
                tablastiendaPendienteList.append(tablaTiendaPendiente)
            return tablastiendaPendienteList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getTiendasPendientesFecha(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tiendasPendientesFechaList=[]
            cursor.execute("SELECT TIPE.CARGA, TIPE.PEDIDO, TIPE.NOMBRE_ALMACEN, TIPE.FECHA_EMBARQUE, TIPE.FECHA_ENTREGA "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA from TIENDA_PENDIENTE TP) TIPE "+
                           "LEFT JOIN FECHA_TRAFICO FTR ON FTR.CARGA=TIPE.CARGA AND FTR.PEDIDO=TIPE.PEDIDO "+
                           "WHERE TIPE.SOLICITUD_ESTATUS='EN TRANSITO' AND FORMAT(TIPE.FECHA_ENTREGA, 'yyyy-MM-dd')<format(GETDATE(), 'yyyy-MM-dd') "+
                           "AND (FORMAT(FTR.FECHA_REGISTRO, 'yyyy-MM-dd')!=FORMAT(GETDATE(), 'yyyy-MM-dd') OR FTR.FECHA_REGISTRO IS NULL) "+
                           "ORDER BY TIPE.FECHA_ENTREGA, TIPE.NOMBRE_ALMACEN, TIPE.PEDIDO")
            registros=cursor.fetchall()
            for registro in registros:
                tiendaPendienteFecha=TiendaPendienteFecha(registro[0], registro[1], registro[2], registro[3], registro[4])
                tiendasPendientesFechaList.append(tiendaPendienteFecha)
            return tiendasPendientesFechaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def insertFechaTrafico(self, fecha, carga, pedido):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cursor.execute("DELETE FECHA_TRAFICO WHERE CARGA=? AND PEDIDO=?", (carga, pedido))
            cursor.execute("INSERT INTO FECHA_TRAFICO (CARGA, PEDIDO, FECHA_REAL, FECHA_REGISTRO) VALUES(?, ?, ?, GETDATE())", (carga, pedido, fecha))
            conexion.commit()
            return True
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getPedidosPorCerrar(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            pedidopPorCerrarList=[]
            cursor.execute("SELECT SP.PEDIDO, SP.ESTATUS, SP.TIENDA, SP.ID_CARGA, TS.DOCUMENTO_SOLICITUD, TS.STATUS "+
                           "FROM STATUS_PEDIDO SP INNER JOIN TRASLADO_SAP TS ON TS.DOCUMENTO_SOLICITUD=SP.SOLICITUD_TRASLADO "+
                           "WHERE TS.STATUS='C' AND SP.ESTATUS!='CERRADA'")
            registros=cursor.fetchall()
            for registro in registros:
                pedidoPorCerrar=PedidoPorCerrar(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
                pedidopPorCerrarList.append(pedidoPorCerrar)
            return pedidopPorCerrarList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def cerrarPedidoPendientes(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cursor.execute("UPDATE Solicitud SET SolicitudStatus = 4 WHERE CONCAT(SolicitudNoTransporte,'-',SolicitudID) IN (SELECT CONCAT(ID_CARGA,'-',PEDIDO) "+
                           "FROM STATUS_PEDIDO SP INNER JOIN TRASLADO_SAP TS ON TS.DOCUMENTO_SOLICITUD=SP.SOLICITUD_TRASLADO "+
                           "WHERE TS.STATUS='C' AND SP.ESTATUS!='CERRADA')")

            cursor.execute("UPDATE SolicitudContenedor SET ContenedorStatus = 4 WHERE CONCAT(SolicitudNoTransporte,'-',SolicitudID) IN (SELECT CONCAT(ID_CARGA,'-',PEDIDO) "+
                           "FROM STATUS_PEDIDO SP INNER JOIN TRASLADO_SAP TS ON TS.DOCUMENTO_SOLICITUD=SP.SOLICITUD_TRASLADO "+
                           "WHERE TS.STATUS='C' AND SP.ESTATUS!='CERRADA')")

            cursor.execute("UPDATE SolicitudRutas SET status = 4 WHERE CONCAT(SolicitudNoTransporte,'-',SolicitudID) IN (SELECT CONCAT(ID_CARGA,'-',PEDIDO) "+
                           "FROM STATUS_PEDIDO SP INNER JOIN TRASLADO_SAP TS ON TS.DOCUMENTO_SOLICITUD=SP.SOLICITUD_TRASLADO "+
                           "WHERE TS.STATUS='C' AND SP.ESTATUS!='CERRADA')")
            conexion.commit()
            return True
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
    
    def getPedidosSinTr(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            pedidosSinTrList=[]
            numero=0
            cursor.execute("SELECT PEDIDO FROM STATUS_PEDIDO WHERE SOLICITUD_TRASLADO='' and ESTATUS!='CERRADA'")
            registros=cursor.fetchall()
            for registro in registros:
                logger.error(registro[0])
                pedidosSinTrList.append(registro[0])
            return pedidosSinTrList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getTiendasPendientesAll(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tiendaPendienteList=[]
            numParamteros=0
            cursor.execute("SELECT TIPE.SOLICITUD_ESTATUS, TIPE.CARGA, TIPE.PEDIDO, TIPE.NOMBRE_ALMACEN, TIPE.FECHA_EMBARQUE, TIPE.FECHA_PLANEADA, TIPE.TRANSITO, TIPE.CROSS_DOCK, TIPE.FECHA_ENTREGA "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA from TIENDA_PENDIENTE TP) TIPE "+
                           "ORDER BY TIPE.FECHA_ENTREGA")
            registros=cursor.fetchall()
            for registro in registros:
                tiendaPendiente=TiendaPendiente(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8])
                tiendaPendienteList.append(tiendaPendiente)
            return tiendaPendienteList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getTiendasPendientesCorreo(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tiendaPendienteList=[]
            numParamteros=0
            cursor.execute("SELECT TIPE.SOLICITUD_ESTATUS, TIPE.CARGA, TIPE.PEDIDO, TIPE.NOMBRE_ALMACEN, TIPE.FECHA_EMBARQUE, TIPE.FECHA_PLANEADA, TIPE.TRANSITO, TIPE.CROSS_DOCK, TIPE.FECHA_ENTREGA "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA from TIENDA_PENDIENTE TP) TIPE "+
                           "where TIPE.SOLICITUD_ESTATUS IN ('EN TRANSITO', 'REC PARCIAL') "+
                           "AND FORMAT(TIPE.FECHA_ENTREGA, 'yyyy-MM-dd')<FORMAT(GETDATE(), 'yyyy-MM-dd') "+
                           "ORDER BY TIPE.SOLICITUD_ESTATUS DESC, TIPE.FECHA_ENTREGA")
            registros=cursor.fetchall()
            for registro in registros:
                tiendaPendiente=TiendaPendiente(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8])
                tiendaPendienteList.append(tiendaPendiente)
            return tiendaPendienteList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getRecibosTienda(self, fechaInicio, fechaFin):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            recibosTiendaList=[]
            numParamteros=0
            cursor.execute("select SolicitudNoTransporte 'CARGA', SolicitudID 'PEDIDO', TransportistaFHLlegada 'LLEGADA DEL TRANSPORTISTA:', TransportistaHoraIni 'INICIO DE ESCANEO', TransportistaHoraFin 'FIN DE ESCANEO', TransportistaFHFin  'CIERRE DE CAMION' "+
                           "from SolicitudTransportista "+
                           "where TransportistaOrigen = 'TIENDA' "+
                           "AND CONVERT(DATE, TransportistaFHLlegada ,103) between '"+fechaInicio+"' and '"+fechaFin+"' "+
                           "order by TransportistaFHLlegada DESC, SolicitudID, SolicitudNoTransporte")
            registros=cursor.fetchall()
            for registro in registros:
                reciboTienda=ReciboTienda(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
                recibosTiendaList.append(reciboTienda)
            return recibosTiendaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getCorreoTiendaPendiente(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tiendaCorreoList=[]
            cursor.execute("SELECT distinct TIPE.NOMBRE_ALMACEN "+
                           "FROM(select TP.SOLICITUD_ESTATUS, TP.CARGA, TP.PEDIDO, TP.NOMBRE_ALMACEN, TP.FECHA_EMBARQUE, TP.FECHA_PLANEADA, TP.TRANSITO, TP.CROSS_DOCK, ISNULL((SELECT FECHA_REAL FROM FECHA_TRAFICO FT WHERE FT.CARGA=TP.CARGA AND FT.PEDIDO=TP.PEDIDO), TP.FECHA_PLANEADA) FECHA_ENTREGA from TIENDA_PENDIENTE TP) TIPE "+
                           "WHERE TIPE.SOLICITUD_ESTATUS='EN TRANSITO' AND "+
                           "format(TIPE.FECHA_ENTREGA, 'yyyy-MM-dd')<format(GETDATE(), 'yyyy-MM-dd') and "+
                           "TIPE.NOMBRE_ALMACEN like 'T%' "+
                           "and substring(TIPE.NOMBRE_ALMACEN, 1, 5) not in (SELECT substring(subject, 22, 5) FROM [msdb].[dbo].[sysmail_sentitems] "+
                           "where subject like 'PEDIDOS PENDIENTES -%' and format(sent_date, 'yyyy-MM-dd')=format(GETDATE(),'yyyy-MM-dd'))")
            registros=cursor.fetchall()
            for registro in registros:
                tiendaCorreo=TiendaCorreo(registro[0])
                tiendaCorreoList.append(tiendaCorreo)
            return tiendaCorreoList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
