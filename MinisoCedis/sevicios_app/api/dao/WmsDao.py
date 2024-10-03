import logging
import pyodbc
from sevicios_app.vo.pedido import Pedido
from sevicios_app.vo.carga import Carga
from sevicios_app.vo.detalleCarga import DetalleCarga
from sevicios_app.vo.reciboPendiente import ReciboPendiente
from sevicios_app.vo.split import Split
from sevicios_app.vo.contenedorEpq import ContenedorEpq
from sevicios_app.vo.ubicacionVacia import UbiacionVacia
from sevicios_app.vo.contenedorOla import ContenedorOla
from sevicios_app.vo.olaPiezaCont import OlaPiezaCont
from sevicios_app.vo.detalleContenedorOla import DetalleContenedorOla
from sevicios_app.vo.lineaOla import LineaOla
from sevicios_app.vo.tareaReaSurtAbierta import TareaReaSurtAbierta
from sevicios_app.vo.contenedor import Contenedor
from sevicios_app.vo.inventario import Inventario
from sevicios_app.vo.cantidad import Cantidad
from sevicios_app.vo.porcentaje import Porcentaje
from sevicios_app.vo.wave import Wave
from sevicios_app.vo.pesoContenedor import PesoContenedor
from sevicios_app.vo.shorpick import Shorpick
from sevicios_app.vo.unlock import Unlock
from sevicios_app.vo.contenedorQc import ContenedorQc
from sevicios_app.vo.itemcontenedorqc import ItemContenedorQc

logger = logging.getLogger('')

class WMSDao():

    def getConexion(self):
        try:
            direccion_servidor = '192.168.84.103'
            nombre_bd = 'ILS'
            nombre_usuario = 'manh'
            password = 'Pa$$w0rdLDM'
            conexion = None

#            direccion_servidor = '192.168.84.162'
#            nombre_bd = 'ILS'
#            nombre_usuario = 'manh'
#            password = 'Pa$$w0rdLDM'
#            conexion = None

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
        
    def getPedidos(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            pedidosList=[]
            cursor.execute("select distinct erp_order from SHIPMENT_HEADER where TRAILING_STS<900 order by erp_order")
            registros=cursor.fetchall()
            for registro in registros:
                pedido=Pedido(registro[0])
                pedidosList.append(pedido)
            return pedidosList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getCargas(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cargasList=[]
            cursor.execute("select distinct internal_load_num from shipping_load  where TRAILING_STS<900 order by internal_load_num")
            registros=cursor.fetchall()
            for registro in registros:
                carga=Carga(registro[0])
                cargasList.append(carga)
            return cargasList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getCarga(self, idsCargas, numRegistros):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            detallesCargaList=[]
            registros=''
            if numRegistros:
                registros='TOP '+numRegistros
            cursor.execute("select "+registros+" sd.REQUESTED_QTY as 'Cantidad', "+
                           "'5' as 'IdUnidadEmbalaje', "+
                           "sd.ITEM_CATEGORY3 as 'DescripcionMaterialCarga', "+
                           "sd.ITEM_WEIGHT as 'PesoArticulo',  "+
                           "'21' as 'IdUnidadPeso', "+
                           "sd.ITEM as 'ClaveProductoServicio', "+
                           "'KGM' as 'ClaveUnidadMedidaEmbalaje', "+
                           "'H87' as 'ClaveUnidad', "+
                           "'NO' as 'MaterialPeligroso', "+
                           "sd.ERP_ORDER as 'Pedido', "+
                           "sh.customer as 'Tienda',  "+
                           "sh.CUSTOMER_NAME as 'NombreTienda',  "+
                           "sh.SHIP_TO_POSTAL_CODE as 'CodigoPostal', "+
                           "'MEX' as 'Pais', "+
                           "CASE sh.SHIP_TO_STATE  "+
                           "WHEN 'MCH' THEN 'MIC' "+
                           "WHEN 'QR' THEN 'ROO' "+
                           "WHEN 'CMX' THEN 'DIF' "+
                           "WHEN 'CHS' THEN 'CHP' "+
                           "WHEN 'GTO' THEN 'GUA' "+
                           "WHEN 'CHI' THEN 'CHH' "+
                           "WHEN 'NL' THEN 'NLE' "+
                           "WHEN 'AGS' THEN 'AGU' "+
                           "WHEN 'BC' THEN 'BCN' "+
                           "WHEN 'DF' THEN 'DIF' "+
                           "ELSE sh.SHIP_TO_STATE "+
                           "END as 'Estado', "+
                           "sh.SHIP_TO_ADDRESS1 as 'Direccion',  "+
                           "sd.QUANTITY_UM as 'UnidadMedida', "+
                           "'OR000001' as 'IdOrigen', "+
                           "CONCAT('DE00', substring(sh.customer,2,4)) as 'IdDestino', "+
                           "sd.ITEM_VOLUME as 'Volumen',  "+
                           "sd.ITEM_DIMENSION_UM as 'UnidadVolumen' "+
                           "from shipping_load sl  "+
                           "inner join shipment_header sh on sh.SHIPPING_LOAD_NUM = sl.INTERNAL_LOAD_NUM  "+
                           "inner join shipment_detail sd on sd.INTERNAL_SHIPMENT_NUM = sh.INTERNAL_SHIPMENT_NUM  "+
                           "where sl.INTERNAL_LOAD_NUM in ("+idsCargas +") "
                           "order by sh.customer, sd.ERP_ORDER")
            registros=cursor.fetchall()
            for registro in registros:
                detalleCarga=DetalleCarga(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], 
                                  registro[11], registro[12], registro[13], registro[14], registro[15], registro[16], registro[17], registro[18], registro[19], registro[20])
                if detalleCarga.tienda[0:3]=='MKP':
                    detalleCarga.idDestino='DE30'+detalleCarga.tienda[3:]
                detallesCargaList.append(detalleCarga)
            return detallesCargaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
        
    def updateCodigoSat(self, codigosSatList):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            sqlUpdate = "UPDATE ITEM SET USER_DEF6 = ? WHERE ITEM = ?"
            index=0
            for codigoSat in codigosSatList:
                index+=1
                cursor.execute(sqlUpdate, (codigoSat.codigoSat, codigoSat.item))
                if index % 100 == 0:
                    print(index)
                    conexion.commit()
            conexion.commit()
            return
        except Exception as exception:
            logger.error(f"Se presento una incidencia al actualizar los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
            
    def getRecibosPendientes(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            reciboPendienteList=[]
            cursor.execute("select rh.RECEIPT_ID, rd.ITEM, rd.ITEM_DESC, rd.TOTAL_QTY, rd.OPEN_QTY from RECEIPT_HEADER rh inner join RECEIPT_DETAIL rd on rd.RECEIPT_ID=rh.RECEIPT_ID where CLOSE_DATE is null and TRAILING_STS <900 and rd.OPEN_QTY>0")
            registros=cursor.fetchall()
            for registro in registros:
                reciboPendiente=ReciboPendiente(registro[0], registro[1], registro[2], registro[3], registro[4])
                reciboPendienteList.append(reciboPendiente)
            return reciboPendienteList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getSplitsByFecha(self, fecha):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            splitList=[]
            cursor.execute("select PEDIDO, CONTENEDOR, FECHA_CREACION, NUMERO_PIEZAS, ESTATUS, USUARIO FROM MINISO_DETALLE_SPLIT WHERE FORMAT(FECHA_CREACION, 'yyyy-MM-dd')=?", (fecha))
            registros=cursor.fetchall()
            for registro in registros:
                split=Split(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
                splitList.append(split)
            return splitList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getContenedoresEpqDay(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            contenedoresEpqList=[]
            cursor.execute("SELECT top 100 CON.CONTENEDOR, FORMAT(CON.ACTIVITY_DATE_TIME, 'yyyy-MM-dd HH:mm:ss'), sh.SHIPMENT_ID PEDIDO, sh.LAUNCH_NUM OLA "+
                           "FROM (select distinct TH.CONTAINER_ID CONTENEDOR, "+
                           "(select top 1 DATEADD(HOUR, DATEDIFF(HOUR, GETUTCDATE(), GETDATE()),ACTIVITY_DATE_TIME) from transaction_history thy where thy.CONTAINER_ID=TH.CONTAINER_ID and thy.TRANSACTION_TYPE=140 and thy.LOCATION='EPQ-01') ACTIVITY_DATE_TIME "+
                           "from TRANSACTION_HISTORY TH WHERE TH.TRANSACTION_TYPE=140 AND TH.LOCATION='EPQ-01' AND TH.CONTAINER_ID IS NOT NULL "+
                           "UNION "+
                           "select distinct ContainerBarcode CONTENEDOR, (SELECT TOP 1 user_def8 FROM MINISO_CONTAINER_LINE MC WHERE MC.ContainerBarcode=MCL.ContainerBarcode) ACTIVITY_DATE_TIME "+
                           "from MINISO_CONTAINER_LINE MCL where status ='Processed') CON "+
                           "INNER JOIN SHIPPING_CONTAINER SC ON SC.CONTAINER_ID=CON.CONTENEDOR "+
                           "inner join SHIPMENT_HEADER SH on SH.INTERNAL_SHIPMENT_NUM=SC.INTERNAL_SHIPMENT_NUM "+
                           "where FORMAT(CON.ACTIVITY_DATE_TIME, 'yyyy-MM-dd')=FORMAT(GETDATE(), 'yyyy-MM-dd') "+
                           "ORDER BY CON.ACTIVITY_DATE_TIME DESC")
            registros=cursor.fetchall()
            for registro in registros:
                contenedorEpq=ContenedorEpq(registro[0], registro[1], registro[2], registro[3])
                contenedoresEpqList.append(contenedorEpq)
            return contenedoresEpqList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getContenedoresEpqAll(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            contenedoresEpqList=[]
            cursor.execute("SELECT CON.CONTENEDOR, FORMAT(CON.ACTIVITY_DATE_TIME, 'yyyy-MM-dd HH:mm:ss'), sh.SHIPMENT_ID PEDIDO, sh.LAUNCH_NUM OLA "+
                           "FROM (select distinct TH.CONTAINER_ID CONTENEDOR, "+
                           "(select top 1 DATEADD(HOUR, DATEDIFF(HOUR, GETUTCDATE(), GETDATE()),ACTIVITY_DATE_TIME) from transaction_history thy where thy.CONTAINER_ID=TH.CONTAINER_ID and thy.TRANSACTION_TYPE=140 and thy.LOCATION='EPQ-01') ACTIVITY_DATE_TIME "+
                           "from TRANSACTION_HISTORY TH WHERE TH.TRANSACTION_TYPE=140 AND TH.LOCATION='EPQ-01' AND TH.CONTAINER_ID IS NOT NULL "+
                           "UNION "+
                           "select distinct ContainerBarcode CONTENEDOR, (SELECT TOP 1 user_def8 FROM MINISO_CONTAINER_LINE MC WHERE MC.ContainerBarcode=MCL.ContainerBarcode) ACTIVITY_DATE_TIME "+
                           "from MINISO_CONTAINER_LINE MCL where status ='Processed') CON "+
                           "INNER JOIN SHIPPING_CONTAINER SC ON SC.CONTAINER_ID=CON.CONTENEDOR "+
                           "inner join SHIPMENT_HEADER SH on SH.INTERNAL_SHIPMENT_NUM=SC.INTERNAL_SHIPMENT_NUM "+
                           "ORDER BY CON.ACTIVITY_DATE_TIME DESC")
            registros=cursor.fetchall()
            for registro in registros:
                contenedorEpq=ContenedorEpq(registro[0], registro[1], registro[2], registro[3])
                contenedoresEpqList.append(contenedorEpq)
            return contenedoresEpqList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getUbicacionesVaciasReservaTop(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            ubicacionesVaciasList=[]
            cursor.execute("select top 100 location, LOCATION_STS, ACTIVE "+
                           "from location "+
                           "where LOCATION_STS='Empty' "+
                           "AND  ACTIVE='Y' "+
                           "and location_type='RESERVA'")
            registros=cursor.fetchall()
            for registro in registros:
                ubiacionVacia=UbiacionVacia(registro[0], registro[1], registro[2])
                ubicacionesVaciasList.append(ubiacionVacia)
            return ubicacionesVaciasList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
    
    def getUbicacionesVaciasAll(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            ubicacionesVaciasList=[]
            cursor.execute("select location, LOCATION_STS, ACTIVE "+
                           "from location "+
                           "where LOCATION_STS='Empty' "+
                           "AND  ACTIVE='Y' "+
                           "and location_type='RESERVA'")
            registros=cursor.fetchall()
            for registro in registros:
                ubiacionVacia=UbiacionVacia(registro[0], registro[1], registro[2])
                ubicacionesVaciasList.append(ubiacionVacia)
            return ubicacionesVaciasList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getEstatusContenedores(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            contenedorOlaList=[]
            cursor.execute("SELECT INF.LAUNCH_NUM, 'SEM'+CAST((SELECT DATEPART(ISO_WEEK, LS.LAUNCH_DATE_TIME_STARTED)from LAUNCH_STATISTICS LS where LS.INTERNAL_LAUNCH_NUM =INF.LAUNCH_NUM) AS VARCHAR) SEMANA, "+
                           "INF.PEDIDOS, INF.CONTENEDORES, INF.[PICKING PENDING], INF.[IN PICKING], INF.[PACKING PENDING], INF.[IN PACKING], "+
                           "INF.[STAGING PENDING], INF.[LOADING PENDING], INF.[SHIP CONFIRM PENDING], INF.[LOAD CONFIRM PENDING], INF.CLOSED, "+
                           "INF.Carton, INF.Bolsa "+
                           "FROM (select SH.LAUNCH_NUM, COUNT(DISTINCT SH.SHIPMENT_ID) PEDIDOS, "+
                           "COUNT(SC.CONTAINER_ID) CONTENEDORES, "+
                           "count(case when SC.status=300 then 1 end) 'PICKING PENDING', "+
                           "count(case when SC.status=301 then 1 end) 'IN PICKING', "+
                           "count(case when SC.status=400 then 1 end) 'PACKING PENDING', "+
                           "count(case when SC.status=401 then 1 end) 'IN PACKING', "+
                           "count(case when SC.status=600 then 1 end) 'STAGING PENDING', "+
                           "count(case when SC.status=650 then 1 end) 'LOADING PENDING', "+
                           "count(case when SC.status=700 then 1 end) 'SHIP CONFIRM PENDING', "+
                           "count(case when SC.status=800 then 1 end) 'LOAD CONFIRM PENDING', "+
                           "count(case when SC.status=900 then 1 end) 'CLOSED', "+
                           "count(case when SC.CONTAINER_CLASS='Carton' then 1 end) 'Carton', "+
                           "count(case when SC.CONTAINER_CLASS='Bolsa' then 1 end) 'Bolsa' "+
                           "from SHIPMENT_HEADER SH "+
                           "INNER JOIN (select CONTAINER_ID, STATUS, CONTAINER_CLASS, INTERNAL_SHIPMENT_NUM, CONTAINER_TYPE, ISNULL(USER_DEF3, 'NULL') USER_DEF3 from SHIPPING_CONTAINER WHERE CONTAINER_ID IS NOT NULL) SC "+
                           "ON SC.INTERNAL_SHIPMENT_NUM=SH.INTERNAL_SHIPMENT_NUM AND SC.USER_DEF3!='ELIMINAR CONT' AND SC.CONTAINER_TYPE!='ERROR' "+
                           "GROUP BY SH.LAUNCH_NUM) INF "+
                           "ORDER BY SEMANA, INF.LAUNCH_NUM")
            registros=cursor.fetchall()
            for registro in registros:
                contenedorOla=ContenedorOla(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14])
                contenedorOlaList.append(contenedorOla)
            return contenedorOlaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getDetalleEstatusContenedores(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            detalleContenedorOlaList=[]
            cursor.execute("select SH.LAUNCH_NUM, SH.SHIPMENT_ID, SC.CONTAINER_ID, SC.status, "+
                           "CASE "+
                           "WHEN SC.status=300 THEN 'PICKING PENDING' "+
                           "WHEN SC.status=301 THEN 'IN PICKING' "+
                           "WHEN SC.status=400 THEN 'PACKING PENDING' "+
                           "WHEN SC.status=401 THEN 'IN PACKING' "+
                           "WHEN SC.status=600 THEN 'STAGING PENDING' "+
                           "WHEN SC.status=650 THEN 'LOADING PENDING' "+
                           "WHEN SC.status=700 THEN 'SHIP CONFIRM PENDING' "+
                           "WHEN SC.status=800 THEN 'LOAD CONFIRM PENDING' "+ 
                           "WHEN SC.status=900 THEN 'CLOSED' "+
                           "END AS ESTATUS, "+
                           "CASE "+ 
                           "WHEN SC.CONTAINER_CLASS='Carton' THEN 'CARTON' "+
                           "WHEN SC.CONTAINER_CLASS='Bolsa' THEN 'BOLSA' "+ 
                           "END AS TIPO "+
                           "from SHIPMENT_HEADER SH "+
                           "INNER JOIN (SELECT CONTAINER_ID, CONTAINER_CLASS, status, INTERNAL_SHIPMENT_NUM, ISNULL(USER_DEF3, 'NULL') USER_DEF3, CONTAINER_TYPE FROM SHIPPING_CONTAINER WHERE CONTAINER_ID IS NOT NULL) SC ON SC.INTERNAL_SHIPMENT_NUM=SH.INTERNAL_SHIPMENT_NUM "+
                           "AND SC.USER_DEF3!='ELIMINAR CONT' AND SC.CONTAINER_TYPE!='ERROR' "+
                           "ORDER BY SC.status, SH.SHIPMENT_ID, TIPO, SC.CONTAINER_ID")
            registros=cursor.fetchall()
            for registro in registros:
                detalleContenedorOla=DetalleContenedorOla(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
                detalleContenedorOlaList.append(detalleContenedorOla)
            return detalleContenedorOlaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getOlaPiezasContenedores(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            olaPiezaContList=[]
            cursor.execute("SELECT QTY.LAUNCH_NUM, QTY.TOTAL_QUANTITY, isnull(CONT.CONTENEDORES, 0) CONTENEDORES "+
                           "FROM "+
                           "(select SH.LAUNCH_NUM, "+
                           "sum(SD.TOTAL_QTY) TOTAL_QUANTITY "+
                           "from SHIPMENT_HEADER SH "+
                           "INNER JOIN SHIPMENT_DETAIL SD ON SD.INTERNAL_SHIPMENT_NUM= SH.INTERNAL_SHIPMENT_NUM "+
                           "GROUP BY SH.LAUNCH_NUM) QTY "+
                           "LEFT JOIN "+
                           "(select SH.LAUNCH_NUM, "+
                           "COUNT(SC.CONTAINER_ID) CONTENEDORES "+
                           "from SHIPMENT_HEADER SH "+
                           "INNER JOIN SHIPPING_CONTAINER SC ON SC.INTERNAL_SHIPMENT_NUM=SH.INTERNAL_SHIPMENT_NUM AND SC.CONTAINER_ID IS NOT NULL AND SC.USER_DEF3!='ELIMINAR CONT' AND SC.CONTAINER_TYPE!='ERROR' "+
                           "GROUP BY SH.LAUNCH_NUM) CONT ON CONT.LAUNCH_NUM=QTY.LAUNCH_NUM "+
                           "order by QTY.LAUNCH_NUM")
            registros=cursor.fetchall()
            for registro in registros:
                olaPiezaCont=OlaPiezaCont(registro[0], registro[1], registro[2])
                olaPiezaContList.append(olaPiezaCont)
            return olaPiezaContList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getLineasOla(self, oneHundred, ola):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            lineaOlaList=[]
            top=""
            if oneHundred:
                  top="top 100 "
            cursor.execute("select "+top+"LAUNCH_NUM, SHIPMENT_ID, ITEM, ITEM_DESC, TOTAL_QTY, STATUS1 "+
                           "from SHIPMENT_DETAIL where LAUNCH_NUM='"+ola+"' "+
                           "and STATUS1 <> 900 and total_qty != 0 and STATUS1 >= 300")
            registros=cursor.fetchall()
            for registro in registros:
                lineaOla=LineaOla(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5])
                lineaOlaList.append(lineaOla)
            return lineaOlaList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)


    def getTareasReaSurtAbiertas(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            tareasList=[]
            cursor.execute("SELECT WI.WORK_UNIT, WI.INSTRUCTION_TYPE, WI.WORK_TYPE, WI.USER_DEF1, WI.USER_DEF6, WI.CONDITION, WI.ITEM, WI.ITEM_DESC, WI.REFERENCE_ID, WI.FROM_LOC, WI.FROM_QTY, "+
                           "WI.TO_LOC, WI.TO_QTY, WI.LAUNCH_NUM, WI.INTERNAL_INSTRUCTION_NUM, WI.CONVERTED_QTY, WI.CONTAINER_ID, CT.CONTAINER_TYPE, FORMAT(WI.AGING_DATE_TIME, 'dd/MM/yyyy hh:mm:ss'), "+
                           "FORMAT(WI.START_DATE_TIME, 'dd/MM/yyyy hh:mm:ss') "+  
                           "FROM WORK_INSTRUCTION WI LEFT JOIN (SELECT * FROM SHIPPING_CONTAINER WHERE CONTAINER_TYPE <> '-' AND CONTAINER_ID IS NOT NULL) CT ON WI.CONTAINER_ID = CT.CONTAINER_ID "+ 
                           "WHERE (WORK_TYPE = 'Reab de Reserva a Picking' or WORK_TYPE LIKE 'Surt%') AND INSTRUCTION_TYPE = 'Detail' AND CONDITION ='OPEN'")
            registros=cursor.fetchall()
            for registro in registros:
                tareaReaSurtAbierta=TareaReaSurtAbierta(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14], registro[15], registro[16], registro[17], registro[18], registro[19])
                tareasList.append(tareaReaSurtAbierta)
            return tareasList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getContenedores(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            contenedoresList=[]
            cursor.execute("SELECT SCH.CONTAINER_ID, SH.SHIPMENT_ID, SCH.CONTAINER_TYPE, SH.LEADING_STS, SC.ITEM, SC.QUANTITY, SH.CUSTOMER, SC.LAUNCH_NUM, format(dateadd(HOUR, -6,sc.DATE_TIME_STAMP), 'yyyy-MM-dd') "+
                           "FROM SHIPPING_CONTAINER SC "+ 
                           "INNER JOIN SHIPMENT_HEADER SH ON SH.INTERNAL_SHIPMENT_NUM=SC.INTERNAL_SHIPMENT_NUM "+
                           "INNER JOIN (SELECT CONTAINER_ID, CONTAINER_TYPE FROM SHIPPING_CONTAINER WHERE CONTAINER_ID IS NOT NULL) SCH ON SCH.CONTAINER_ID=SC.PARENT_CONTAINER_ID "+
                           "WHERE SC.QUANTITY>0 AND SH.LEADING_STS<999")
            registros=cursor.fetchall()
            for registro in registros:
                contenedor=Contenedor(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8])
                contenedoresList.append(contenedor)
            return contenedoresList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getInventario(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            inventarioList=[]
            cursor.execute("select li.LOCATION, li.PERMANENT, lo.ACTIVE, lo.LOCATING_ZONE, li.ITEM, li.ITEM_DESC, li.INVENTORY_STS, (li.ON_HAND_QTY+li.IN_TRANSIT_QTY-li.ALLOCATED_QTY-li.SUSPENSE_QTY), li.ON_HAND_QTY, li.IN_TRANSIT_QTY, li.ALLOCATED_QTY, li.SUSPENSE_QTY, it.ITEM_CATEGORY1, it.ITEM_CATEGORY2, it.ITEM_CATEGORY3 "+
                           "from LOCATION_INVENTORY li "+
                           "inner join location lo on lo.LOCATION=li.LOCATION "+
                           "inner join item it on it.ITEM=li.ITEM "+
                           "where li.LOCATION like 'R-%' "+
                           "OR (li.LOCATION LIKE 'P-%' AND LOCATION_TYPE = 'PICKING TEPOZ PICHONERA') " + #new
                           "order by li.LOCATION")
            registros=cursor.fetchall()
            for registro in registros:
                inventario=Inventario(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14])
                inventarioList.append(inventario)
            return inventarioList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def calcular_cantidad_en_caja(dim_caja, dim_producto, peso_producto, peso_limite):
        cantidad_longitud = dim_caja[0] // dim_producto[0]
        cantidad_ancho = dim_caja[1] // dim_producto[1]
        cantidad_altura = dim_caja[2] // dim_producto[2]
        
        cantidad_total = cantidad_longitud * cantidad_ancho * cantidad_altura
        
        peso_total = cantidad_total * peso_producto
        
        if peso_total <= peso_limite:
            return cantidad_total
        else:
            cantidad_limite_peso = peso_limite // peso_producto
            return cantidad_limite_peso

    def getCantidadCajas(self, item):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cantidadCajas=0
            cantidadlist=[]
            cursor.execute("SELECT 120 AS dimensiones_caja_largo, 100 AS dimensiones_caja_ancho, 125 AS dimensiones_caja_altura, "+
                           "LENGTH AS dimensiones_producto_largo, WIDTH AS dimensiones_producto_ancho, HEIGHT AS dimensiones_producto_altura, "+
                           "WEIGHT AS peso_producto, 300 AS peso_limite_caja FROM ITEM_UNIT_OF_MEASURE WHERE QUANTITY_UM = 'CJA' AND ITEM = '"+item+"'")
            fila = cursor.fetchone()
            if fila:
                dimensiones_caja = (fila.dimensiones_caja_largo, fila.dimensiones_caja_ancho, fila.dimensiones_caja_altura)
                dimensiones_producto = (fila.dimensiones_producto_largo, fila.dimensiones_producto_ancho, fila.dimensiones_producto_altura)
                peso_producto = fila.peso_producto
                peso_limite_caja = fila.peso_limite_caja
                cantidad_longitud = dimensiones_caja[0] // dimensiones_producto[0]
                cantidad_ancho = dimensiones_caja[1] // dimensiones_producto[1]
                cantidad_altura = dimensiones_caja[2] // dimensiones_producto[2]
        
                cantidad_total = cantidad_longitud * cantidad_ancho * cantidad_altura
        
                peso_total = cantidad_total * peso_producto
                
                if peso_total <= peso_limite_caja:
                    cantidadCajas= cantidad_total
                else:
                    cantidadCajas = peso_limite_caja // peso_producto

            cantidad=Cantidad(item, cantidadCajas)    
            return cantidad
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
    
    def getPorcentajeSKUsPrioritarios(self, container):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            cursor.execute("select sc.PARENT_CONTAINER_ID container, isnull(sum(case when sp.item is not null then sc.QUANTITY end), 0)/sum(sc.QUANTITY)*100 porcentaje "+
                           "from shipping_container sc "+
                           "left join  (select skuprioritarioitem COLLATE Latin1_General_CI_AS item from [192.168.84.23].recepciontienda.dbo.SKUPrioritario) sp on sp.item=sc.ITEM "+
                           "where sc.PARENT_CONTAINER_ID=? group by sc.PARENT_CONTAINER_ID", (container))
            fila = cursor.fetchone()
            if fila:
                return Porcentaje(fila.container, fila.porcentaje)
            return Porcentaje(None, None)
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getWaveAnalysis(self, oneHundred, wave):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            waveList=[]
            top=""
            if oneHundred:
                top="top 100 "
            cursor.execute("SELECT "+top+"sh.ITEM, it.description, it.STORAGE_TEMPLATE, sh.SHIPMENT_ID, sh.LAUNCH_NUM "+
                           ", (SELECT SF.STATUS_NAME FROM FUNCTIONAL_AREA_STATUS_FLOW SF (NOLOCK) "+ 
                           "WHERE SF.status = sh.STATUS1 AND SF.FUNCTIONAL_AREA = 'Outbound' ) STATUS "+
                           ", sh.REQUESTED_QTY "+
                           ", (SELECT SUM(SAR.ALLOCATED_QTY) FROM SHIPMENT_ALLOC_REQUEST SAR (NOLOCK) "+ 
                           "WHERE SAR.SHIPMENT_ID = sh.SHIPMENT_ID AND SAR.ITEM = sh.ITEM)ALLOCATED_QTY "+
                           ",SUM(mt.ON_HAND_QTY) - SUM(mt.ALLOCATED_QTY) - SUM(mt.SUSPENSE_QTY) AS AV "+
                           ",SUM(mt.ON_HAND_QTY) OH, SUM(mt.ALLOCATED_QTY) AL, SUM(mt.IN_TRANSIT_QTY) IT, SUM(mt.SUSPENSE_QTY) SU "+
                           ", sh.CUSTOMER, sh.ITEM_CATEGORY1, DATEADD(HH,-6, HE.CREATION_DATE_TIME_STAMP) CREATION_DATE_TIME_STAMP, HE.SCHEDULED_SHIP_DATE "+
                           ", it.DIVISION "+
                           ", 'CONV' = CASE "+ 
                           "WHEN it.STORAGE_TEMPLATE = 'PZA-INR-CJA' THEN "+ 
                           "(SELECT un.CONVERSION_QTY FROM ITEM_UNIT_OF_MEASURE un (NOLOCK) WHERE un.ITEM = it.ITEM and un.QUANTITY_UM = 'INR') "+
                           "ELSE 1 END "+
                           "FROM "+ 
                           "SHIPMENT_DETAIL sh (NOLOCK) "+
                           "inner join SHIPMENT_HEADER HE (NOLOCK) on sh.SHIPMENT_ID = HE.SHIPMENT_ID "+ 
                           "left outer join METADATA_INSIGHT_INVENTORY_VIEW MT (NOLOCK) on sh.ITEM = MT.ITEM "+ 
                           "and MT.ACTIVE = 'Y' and MT.INVENTORY_STS = 'Disponible' "+
                           "left join ITEM it (NOLOCK) on sh.ITEM = it.ITEM "+
                           "WHERE "+ 
                           "HE.LEADING_STS <= 300 "+
                           "and HE.LAUNCH_NUM=? "+
                           "GROUP BY sh.ITEM, it.STORAGE_TEMPLATE, sh.SHIPMENT_ID,	sh.LAUNCH_NUM, sh.REQUESTED_QTY, sh.ERP_ORDER_LINE_NUM "+
                           ", sh.CUSTOMER, sh.ITEM_CATEGORY1, HE.CREATION_DATE_TIME_STAMP, HE.SCHEDULED_SHIP_DATE, it.DIVISION "+
                           ", sh.STATUS1 "+
                           ", it.description, it.ITEM "+
                           "ORDER BY sh.SHIPMENT_ID, sh.ERP_ORDER_LINE_NUM", (wave))
            registros=cursor.fetchall()
            for registro in registros:
                wave=Wave(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14], registro[15], registro[16], registro[17], registro[18])
                waveList.append(wave)
            return waveList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)
                
    def getPesoContenedor(self, contenedor):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            item=''
            cantidad=0
            peso=0
            tolerancia=0.0
            tipoContenedor=''
            pesoCja=0.0
            cursor.execute("SELECT CT.EMPTY_WEIGHT, CT.WEIGHT_TOLERANCE, SC.CONTAINER_TYPE FROM SHIPPING_CONTAINER SC INNER JOIN CONTAINER_TYPE CT ON CT.CONTAINER_TYPE=SC.CONTAINER_TYPE WHERE SC.CONTAINER_ID=?", (contenedor))
            datosCja=cursor.fetchall()
            if len(datosCja) ==0:
                return PesoContenedor(-1, tolerancia, tipoContenedor)
            else:
                pesoCja=float(datosCja[0][0])
                tolerancia=float(datosCja[0][1])
                tipoContenedor=datosCja[0][2]
            cursor.execute("SELECT ITEM, QUANTITY FROM SHIPPING_CONTAINER WHERE (CONTAINER_ID=? OR PARENT_CONTAINER_ID=?) AND ITEM IS NOT NULL", (contenedor, contenedor))
            itemsCaja=cursor.fetchall()
            print(len(itemsCaja))
            if len(itemsCaja)==1:
                item=itemsCaja[0][0]
                cantidad=int(itemsCaja[0][1])
                print(f"Item: {item}, cantidad: {cantidad}")
                cursor.execute("SELECT CONVERSION_QTY, WEIGHT FROM ITEM_UNIT_OF_MEASURE WHERE ITEM=? AND QUANTITY_UM='CJA'", (item))
                datosCaja=cursor.fetchall()
                if len(datosCaja)==1:
                    pzas=int(datosCaja[0][0])
                    if cantidad%pzas==0 and cantidad/pzas==1:
                        return PesoContenedor(float(datosCaja[0][1]), tolerancia, tipoContenedor)
                cursor.execute("SELECT CONVERSION_QTY, WEIGHT FROM ITEM_UNIT_OF_MEASURE WHERE ITEM=? AND QUANTITY_UM='INR'", (item))
                datosInner=cursor.fetchall()
                if len(datosInner)==1:
                    pzas=int(datosInner[0][0])
                    if cantidad%pzas==0 and cantidad%pzas==1:
                        return PesoContenedor(float(datosInner[0][1]), tolerancia, tipoContenedor)
            for itm in itemsCaja:
                item=itm[0]
                cantidad=int(itm[1])
                cursor.execute("SELECT CONVERSION_QTY, WEIGHT FROM ITEM_UNIT_OF_MEASURE WHERE ITEM=? AND QUANTITY_UM='INR'", (item))
                datosInner=cursor.fetchall()
                if len(datosInner)==1:
                    pzas=int(datosInner[0][0])
                    weight=float(datosInner[0][1])
                    if cantidad%pzas==0:
                        pe=(cantidad/pzas*weight)
                        peso=peso+(cantidad/pzas*weight)
                    else:
                        cursor.execute("SELECT CONVERSION_QTY, WEIGHT FROM ITEM_UNIT_OF_MEASURE WHERE ITEM=? AND QUANTITY_UM='PZA'", (item))
                        datosPza=cursor.fetchone()
                        weight=float(datosPza[1])
                        pe=cantidad*weight
                        peso=peso+(cantidad*weight)
                else:
                    cursor.execute("SELECT CONVERSION_QTY, WEIGHT FROM ITEM_UNIT_OF_MEASURE WHERE ITEM=? AND QUANTITY_UM='PZA'", (item))
                    datosPza=cursor.fetchone()
                    weight=float(datosPza[1])
                    pe=cantidad*weight
                    peso=peso+(cantidad*weight)
            peso = peso + pesoCja
            return PesoContenedor(peso, tolerancia, tipoContenedor)
            
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

#New =>

    def getShorpick(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            shorpickList=[]
            
            cursor.execute("SELECT  DATEPART(WEEK,DATE_TIME_STAMP),INTERNAL_ID, REFERENCE_ID, DATE_TIME_STAMP, TRANSACTION_TYPE, LOCATION,ITEM,COMPANY,LOT,CAST(QUANTITY as int) AS QUANTITY,QUANTITY_UM,DIRECTION,WORK_TYPE,WORK_TEAM,INTERNAL_KEY_ID, WORK_UNIT,USER_NAME,USER_DEF1,EQUIPMENT_TYPE, warehouse " +
                            "FROM TRANSACTION_HISTORY_INVENTORY_ATTRIBUTE_VIEW " +
                            "where location != 'EPQ-01' AND " +
                            "TRANSACTION_TYPE = '240' " +
                            "ORDER BY INTERNAL_ID")
            registros=cursor.fetchall()
            for registro in registros:
                shorpick=Shorpick(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14],registro[15], registro[16], registro[17], registro[18], registro[19])
                shorpickList.append(shorpick)
            return shorpickList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getUnlock(self):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            unlockList=[]
            cursor.execute("SELECT INTERNAL_ID, REFERENCE_ID,DATE_TIME_STAMP, TRANSACTION_TYPE, LOCATION, ITEM, COMPANY, LOT,CAST(QUANTITY as int) AS QUANTITY,QUANTITY_UM,USER_DEF1,WORK_TYPE,CONTAINER_ID,INTERNAL_KEY_ID, WORK_UNIT,USER_NAME, WORK_TEAM, EQUIPMENT_TYPE, warehouse,CAST(ABS(QUANTITY)AS INT) AS QUANTITY_Positive " +
                            "FROM TRANSACTION_HISTORY_INVENTORY_ATTRIBUTE_VIEW " +
                            "where TRANSACTION_TYPE = '270' " +
                            "GROUP BY INTERNAL_ID, REFERENCE_ID, DATE_TIME_STAMP, TRANSACTION_TYPE, LOCATION,warehouse, WORK_TYPE, USER_NAME, WORK_TEAM, EQUIPMENT_TYPE, ITEM, COMPANY, LOT, QUANTITY, QUANTITY_UM, INTERNAL_KEY_ID, WORK_UNIT, USER_DEF1, CONTAINER_ID " +
                            "order by DATE_TIME_STAMP")
            registros=cursor.fetchall()
            for registro in registros:
                unlock=Unlock(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], registro[11], registro[12], registro[13], registro[14],registro[15], registro[16], registro[17], registro[18], registro[19])
                unlockList.append(unlock)
            return unlockList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getContainerQc(self): #ContenedorQc
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            containerList=[]
            cursor.execute("select CONTAINER_ID, WEIGHT, USER_DEF1, TOTAL_FREIGHT_CHARGE, BASE_FREIGHT_CHARGE, FREIGHT_DISCOUNT, ACCESSORIAL_CHARGE, QC_ASSIGNMENT_ID, QC_STATUS, (select activity_date_time from TRANSACTION_HISTORY th where th.CONTAINER_ID =SC.CONTAINER_ID and TRANSACTION_TYPE=210) fecha "+
                            "from SHIPPING_CONTAINER SC " +
                            "where SC.FREIGHT_DISCOUNT>0 and SC.CONTAINER_ID is not null and SC.QC_ASSIGNMENT_ID is not null")
            registros=cursor.fetchall()
            for registro in registros:
                container=ContenedorQc(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8],registro[9])
                containerList.append(container)
            return containerList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getItemContainerQc(self): #ItemContenedoresQc
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            itemContenedorQcList=[]
            cursor.execute("select sc.ITEM, count(*) NumOcur, (select count(*) from shipping_container sct where sct.ITEM=sc.ITEM and sct.status>=650 ) TotalCont " +
                            "from SHIPPING_CONTAINER sc " +
                            "inner join SHIPPING_CONTAINER scq on scq.CONTAINER_ID=sc.PARENT_CONTAINER_ID and scq.QC_ASSIGNMENT_ID is not null " +
                            "where sc.status>=650 "+
                            "group by sc.ITEM order by NumOcur desc")
            registros=cursor.fetchall()
            for registro in registros:
                itemContenedorQc=ItemContenedorQc(registro[0], registro[1], registro[2])
                itemContenedorQcList.append(itemContenedorQc)
            return itemContenedorQcList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los reistros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)