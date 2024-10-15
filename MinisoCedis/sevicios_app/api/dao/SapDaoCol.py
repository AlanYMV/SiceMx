import logging
from hdbcli import dbapi
from sevicios_app.vo.articulo import Articulo
from sevicios_app.vo.detallePedido import DetallePedido
from sevicios_app.vo.codigoSat import CodigoSat
from sevicios_app.vo.storageTemplate import StorageTemplate
from sevicios_app.vo.precioCol import PrecioCol
from sevicios_app.vo.infoPedidoSinTr import InfoPedidoSinTr
from sevicios_app.vo.pedidoSapPlaneacion import PedidoSapPlaneacion

logger = logging.getLogger('')

class SapDaoCol():

    def getConexion(self):
        try:
            conexion=dbapi.connect(address="192.168.84.182", port=30015, user="SYSTEM", password="Sy573Mmnso!!")
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
        
    def getStorageTemplatesCol(self, numRegistros):
        try:
            conexion=self.getConexion()
            cursor=conexion.cursor()
            storagesTemplatesList=[]
            registros=''
            if numRegistros:
                registros='TOP '+numRegistros
            cursor.execute('SELECT '+registros+' T0."ItemCode", '+
                            'T1."UgpCode"  as "StorageTemplate", '+
                            'T0."U_SYS_GUML"  as "GrupoLogistico", '+
                            'T0."SalUnitMsr", '+
                            'T2."ItmsGrpNam" as "Familia", '+
                            'T0."U_SUBFAMILIA" as "SubFamilia", '+
                            'T0."U_SUBSUBFAMILIA" as "SubSubFamilia", '+
                            'T0."U_SYS_CAT4", '+
                            'T0."U_SYS_CAT5", '+
                            'T0."U_SYS_CAT6", '+
                            'T0."U_SYS_CAT7", '+
                            'T0."U_SYS_CAT8", '+
                            'T0."BHeight1"  as "Height", '+
                            'T0."BWidth1" as "Width", '+
                            'T0."BLength1" as "Length", '+
                            'T0."BVolume" as "Volume", '+
                            'T0."BWeight1"  as "Weight" '+
                            'FROM "SBO_MINISO_COLOMBIA"."OITM"  T0 '+
                            'INNER JOIN "SBO_MINISO_COLOMBIA"."OUGP"  T1 ON T0."UgpEntry" = T1."UgpEntry" '+
                            'INNER JOIN "SBO_MINISO_COLOMBIA"."OITB" T2 ON T0."ItmsGrpCod" = T2."ItmsGrpCod" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."@SUBSUBFAMILIA" SSF ON T0."U_SUBSUBFAMILIA" = SSF."Code" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."@SUBFAMILIA" SF ON T0."U_SUBFAMILIA" = SF."Code" ' + 
                            'ORDER BY T0."ItemCode" ')
            registros=cursor.fetchall()
            for registro in registros:
                storageTemplate=StorageTemplate(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], registro[10], 
                                  registro[11], registro[12], registro[13], registro[14], registro[15], registro[16])
                storagesTemplatesList.append(storageTemplate)
            return storagesTemplatesList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)

    def getPreciosCol(self, numRegistros):
        try:
            print('Entro a getPrecios')
            conexion=self.getConexion()
            print('Obtuvo la conexión')
            cursor=conexion.cursor()
            preciosList=[]
            registros=''
            if numRegistros:
                registros='TOP '+numRegistros
            cursor.execute('SELECT '+registros+' T0."ItemCode", '+ 
                            'C0."BcdCode" as "Codigo_Barras", '+
                            'F."ItmsGrpNam" as "Categoria", '+ 
                            'T0."U_SUBFAMILIA" as "Subcategoria", '+ 
                            'T0."U_SUBSUBFAMILIA" as "Clase", '+
                            'T0."ItemName", '+ 
                            'T6."UgpCode"  as "Storage_Template", '+
                            'T0."U_SYS_GUML" as "ST_USR", '+
                            'T0."U_SYS_SLICE"  as "Licencia", '+
                            'T0."BHeight1"  as "Height", '+  
                            'T0."BWidth1" as "Width", '+ 
                            'T0."BLength1" as "Length", '+
                            'T0."BVolume" as "Volume", '+ 
                            'T0."BWeight1"  as "Weight", '+
                            'T1."Price" as "ESTANDAR_SIN_IVA", '+ 
                            'T2."Price" as "ESTANDAR_CON_IVA", '+ 
                            'T3."Price" as "ADICIONAL_SIN_IVA", '+
                            'T4."Price" as "ADICIONAL_CON_IVA", '+
                            'T5."Price" as "AEROPUERTO_SIN_IVA", '+
                            'T8."Price" as "AEROPUERTO_CON_IVA", '+
                            'T7."CardName" as "Proveedor" '+
                            'FROM "SBO_MINISO_COLOMBIA"."OITM" T0  '+ 
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T1 ON T0."ItemCode" = T1."ItemCode" and T1."PriceList"=3 '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T2 ON T0."ItemCode" = T2."ItemCode" and T2."PriceList"=4 '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T3 ON T0."ItemCode" = T3."ItemCode" and T3."PriceList"=5 '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T4 ON T0."ItemCode" = T4."ItemCode" and T4."PriceList"=6 '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T5 ON T0."ItemCode" = T5."ItemCode" and T5."PriceList"=13 '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."ITM1" T8 ON T0."ItemCode" = T8."ItemCode" and T8."PriceList"=14 '+
                            'INNER JOIN "SBO_MINISO_COLOMBIA"."OITB" F ON T0."ItmsGrpCod" = F."ItmsGrpCod" '+ 
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."@SUBSUBFAMILIA" SSF ON T0."U_SUBSUBFAMILIA" = SSF."Code" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."@SUBFAMILIA" SF ON T0."U_SUBFAMILIA" = SF."Code" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."OUGP"  T6 ON T0."UgpEntry" = T6."UgpEntry" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."OCRD" T7 ON T0."CardCode" = T7."CardCode" '+
                            'LEFT JOIN "SBO_MINISO_COLOMBIA"."OBCD" C0 ON C0."ItemCode"=T0."ItemCode" '+
                            'where T0."SellItem" = \'Y\' AND T0."validFor" = \'Y\' '+ 
                            'order by T0."ItemCode"')
            print('Se ejecuto el query')
            registros=cursor.fetchall()
            itemCode=''
            precio=PrecioCol('','','','','','','','','','','','','','','','','','','','','')
            for registro in registros:
                if itemCode!=registro[0]:
                    precio=PrecioCol(registro[0], registro[1], registro[2], registro[3], registro[4], registro[5], registro[6], registro[7], registro[8], registro[9], 
                                registro[10], registro[11], registro[12], registro[13], registro[14], registro[15], registro[16], registro[17], registro[18], registro[19], registro[20])
                    preciosList.append(precio)
                    itemCode=registro[0]
                else:
                    precio.codigoBarras=precio.codigoBarras+', '+registro[1]
            return preciosList
        except Exception as exception:
            logger.error(f"Se presento una incidencia al obtener los registros: {exception}")
            raise exception
        finally:
            if conexion!= None:
                self.closeConexion(conexion)