 # -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013-Today OpenERP SA (<http://www.openerp.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#    Code create by: Ing. Luis J. Ortega and Ing. E. Omar Ocamoo 13/03/2018
#
##############################################################################
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from openerp import SUPERUSER_ID
from openerp import models, fields, api, tools
from openerp import http
from openerp.osv import osv
from openerp.exceptions import Warning
import datetime
import time
from datetime import time, datetime, date, timedelta
from openerp import _
import os
import xlrd
from xlrd import open_workbook
import base64
import time
import pytz
import calendar
from stdnum.mx.rfc import (validate,InvalidComponent,InvalidFormat,InvalidLength,InvalidChecksum)
from parse import cargar_MA,cargar_PT
import number_to_letter
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import itertools
from operator import itemgetter
import operator
from itertools import chain
from collections import defaultdict
import random

ODOO_HOME = "/opt/odoo/"
# ODOO_HOME = "/opt/Lafox/odoo"

LAFOX_SELECT_CRUDO_TERMINADO=[
            ('0','Accesorios'),
            ('1','Terminado'),
            ]

LAFOX_SELECT_ESTATUS_PEDIDO=[
            ('P','PREPARACION'),
            ('E','ENVIADO'),
            ('R','RECIBIDO'),
            ]

LAFOX_TYPE_SELECT_VF=[
            ('VENTA','Venta'),
            ('FACTURA','Factura'),
            ]

TIPO_COMPROBANTE_LISTA = [
            ('I','INGRESO'),
            ('E','EGRESO'),
            ('T','TRASLADO'),
            ('N','NÓMINA'),
            ('P','PAGO'),
            ]

REGIMEN_FISCAL = [
            ('601','General de Ley Personas Morales'),
            ('603','Personas Morales con Fines no Lucrativos'),
            ('605','Sueldos y Salarios e Ingresos Asimilados a Salarios'),
            ('606','Arrendamiento'),
            ('608','Demás ingresos'),
            ('609','Consolidación'),
            ('610','Residentes en el Extranjero sin Establecimiento Permanente en México'),
            ('611','Ingresos por Dividendos (socios y accionistas)'),
            ('612','Personas Físicas con Actividades Empresariales y Profesionales'),
            ('614','Ingresos por intereses'),
            ('616','Sin obligaciones fiscales'),
            ('620','Sociedades Cooperativas de Producción que optan por diferir sus ingresos'),
            ('621','Incorporación Fiscal'),
            ('622','Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
            ('623','Opcional para Grupos de Sociedades'),
            ('624','Coordinados'),
            ('628','Hidrocarburos'),
            ('607','Régimen de Enajenación o Adquisición de Bienes'),
            ('629','De los Regímenes Fiscales Preferentes y de las Empresas Multinacionales'),
            ('630','Enajenación de acciones en bolsa de valores'),
            ('615','Régimen de los ingresos por obtención de premios'),
            ]

USO_CFDI = [
            ('G01','Adquisición de mercancias'),
            ('G02','Devoluciones, descuentos o bonificaciones'),
            ('G03','Gastos en general'),
            ('I01','Construcciones'),
            ('I02','Mobilario y equipo de oficina por inversiones'),
            ('I03','Equipo de transporte'),
            ('I04','Equipo de computo y accesorios'),
            ('I05','Dados, troqueles, moldes, matrices y herramental'),
            ('I06','Comunicaciones telefónicas'),
            ('I07','Comunicaciones satelitales'),
            ('I08','Otra maquinaria y equipo'),
            ('D01','Honorarios médicos, dentales y gastos hospitalarios.'),
            ('D02','Gastos médicos por incapacidad o discapacidad'),
            ('D03','Gastos funerales.'),
            ('D04','Donativos.'),
            ('D05','Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación).'),
            ('D06','Aportaciones voluntarias al SAR.'),
            ('D07','Primas por seguros de gastos médicos.'),
            ('D08','Gastos de transportación escolar obligatoria.'),
            ('D09','Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
            ('D10','Pagos por servicios educativos (colegiaturas)'),
            ('P01','Por definir'),
            ]
ACCOUNT_STATE = [
            ('draft','Borrador'),
            ('open','Abierto'),
            ('paid','Pagado'),
            ('cancel','Cancelado'),

        ]

METODO_PAGO_SELECTION = [
            ('01','01/Efectivo'),
            ('02','02/Cheque Nominativo'),
            ('03','03/Transferencia Electrónica de Fondos'),
            ('04','04/Tarjetas de Crédito'),
            ('05','05/Monederos Electrónicos'),
            ('06','06/Dinero Electrónico'),
            # ('07','07/Tarjetas Digitales'),
            ('08','08/Vales de Despensa'),
            # ('09','09/Bienes'),
            # ('10','10/Servicio'),
            # ('11','11/Por cuenta de Tercero'),
            ('12','12/Dacioń de Pago'),
            ('13','13/Pago por Subrogación'),
            ('14','14/Pago por Consignación'),
            ('15','15/Condonación'),
            # ('16','16/Cancelación'),
            ('17','17/Compensación'),
            ('23','23/Novación'),
            ('24','24/Confusuón'),
            ('25','25/Remisión de deuda'),
            ('26','26/Prescripción o caducidad'),
            ('27','27/A satisfacción del acreedor'),
            ('28','28/Tarjeta de Débito'),
            ('29','29/Tarjeta de Servicios'),
            ('30','30/Aplicacion de Anticipos'),
            ('31','29/Intermediario de Pago'),
            # ('98','98/No Aplica (NA)'),
            ('99','99/Otros'),
        ]

FORMA_PAGO_SELECTION = [
            ('PUE','Pago en una sola exhibición'),
            ('PPD','Pago en parcialidades o diferido'),
        ]

LAFOX_SELECT_TIPO_CLIENTE=[
            ('0','Fisica'),
            ('1','Moral'),
]

SELECTION_MES = [
            ('01','ENERO'),
            ('02','FEBRERO'),
            ('03','MARZO'),
            ('04','ABRIL'),
            ('05','MAYO'),
            ('06','JUNIO'),
            ('07','JULIO'),
            ('08','AGOSTO'),
            ('09','SEPTIEMBRE'),
            ('10','OCTUBRE'),
            ('11','NOVIEMBRE'),
            ('12','DICIEMBRE'),
        ]
LAFOX_STATE_PRODUCT = [
            ('EXCELENTE','EXCELENTE'),
            ('BUENO','BUENO'),
            ('REGULAR','REGULAR'),
            ('MALO','MALO'),
            ('MUY_MALO','MUY MALO'),

]

LAFOX_SELECT_STATE_CLIENTE=[
            ('0','EN TIEMPO'),
            ('1','RETARDO'),
            ('2','FALTA'),
]
LAFOX_PUNTUALIDAD_PAGO_CLIENTE = [
            ('EXTRAORDINARIO','EXTRAORDINARIO'),
            ('BUENO','BUENO'),
            ('REGULAR','REGULAR'),
            ('MALO','MALO'),
]
LAFOX_MEDIO_CONTACTO = [
            ('LLAMADA','LLAMADA'),
            ('REDES SOCIALES','REDES SOCIALES'),
            ('VISITA','VISITA'),
            ('OTRA','OTRA'),
]


# Inicio de Clase para almacenes
class stock_warehouse(models.Model):
	_name = 'stock.warehouse'
	_inherit = 'stock.warehouse'

	# FIELDS PARA STOCK-WAREHOUSE

	# FUNCIONES PARA STOCK.WAREHOUSE
	# Función que permite redireccionar la vista a otro modelo
	def _get_act_window_dict(self, cr, uid, name, context=None):
		mod_obj = self.pool.get('ir.model.data')
		act_obj = self.pool.get('ir.actions.act_window')
		result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
		result = act_obj.read(cr, uid, [result], context=context)[0]
		return result

	# Funcion que permite visualizar el stock de los productos
	def action_open_quants_button(self, cr, uid, ids, context=None):
		result = self._get_act_window_dict(cr, uid, 'stock.product_open_quants', context=context)
		result['context'] = "{'search_default_locationgroup': 0, 'search_default_internal_loc': 1,'group_by':['product_id','location_id']}"
		return result

stock_warehouse()

class stock_location(osv.osv):
    _name = 'stock.location'
    _inherit = 'stock.location'

stock_location()

class stock_move(osv.osv):
    _name = 'stock.move'
    _inherit = 'stock.move'

    # FIELDS PARA STOCK.MOVE

    # FUNCIONES PARA STOCK.MOVE
    # Función que  permite aprobar el movimiento y revisa si la cantidad de producto esta disponible en el stock
    @api.multi
    def button_approve_move(self):
    	type_alb = self.env['stock.picking.type'].search([('code','=','internal')])
    	product_move =self.env['stock.quant'].search([('location_id','=',self.location_id.id),('product_id','=',self.product_id.id)])
    	product_move_qty=0
    	for qty_pruduct in product_move:
    		product_move_qty = product_move_qty + qty_pruduct.qty

    	# Si no encuentra producto warnin de que no hay producto
        if len(product_move) < 1:
            raise osv.except_osv(("No es posible realizar esta transacción"), ('EL Producto %s,que quiere transferir no se encuentra disponible en el almacén de origen'% self.product_id.name))
    	# Si hay producto pero es menor, lanza alerte de faltante producto
        elif product_move_qty < self.product_uom_qty:
    		raise osv.except_osv(("No es posible realizar esta transacción"),('EL Producto %s que quiere transferir no cuenta con la cantidad necesaria. La cantidad que dese enviar: %s, La cantidad en Stock: %s en %s'% (self.product_id.name,self.product_uom_qty,product_move_qty,self.location_id.complete_name)))
    	# Si hay prodcuto suficiente deja continuar
        else:
    	   self.write({'state':'confirmed','picking_type_id':type_alb[0].id})
stock_move()

#Class product_product inherit
class product_product(models.Model):
    _name='product.product'
    _inherit='product.product'

    clave_prod=fields.Char(string='Clave del producto',require=True,help='Teclea la clave del producto')
    ref_prod=fields.Char(string='Referencia',require=True,help='Teclea la referencia del producto')
    c_t=fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO,require=True,string='Crudo/Terminado')
    moneda_prod=fields.Selection([('PESOS', 'MXN-PESOS'),('DOLARES', 'DLLS-DOLARES')],string='Moneda',require=True)
    iva_prod=fields.Float(string='I.V.A',require=True,help='I.V.A')
    observacion_prod=fields.Text(string='Observaciones',help='Observaciones al producto')
    poveedor_prod=fields.Char(string='Proveedor',help='Proveedor...')

    cantidad_minima=fields.Integer(string='Cant. Min.',require=True)

    grupo_precios_id=fields.Many2one('lafox.grupo.de.precios',string='Grupo de Precios')
    grupo_inventarios_id=fields.Many2one('lafox.grupo.de.inventarios',string='Grupo de Inventarios')
    seguimiento_id = fields.One2many('lafox.seguimiento.venta.producto','account_ids',string='Ventas Realizadas')
    revisar_ventas = fields.Boolean(string='Revisar Ventas realizadas')
    porcentaje_vendido = fields.Float(string='Porcentaje de Venta %')
    mes_venta = fields.Selection(SELECTION_MES,string='Mes de Venta')
    state_product = fields.Selection(LAFOX_STATE_PRODUCT,string='Estatus de Venta')

    # Probando la nueva API
    # @api.multi
    #def pruebas_de_nueva_api(self):
    #
    #     cantidad_por_id=self.env['account.invoice'].search([])
    #
    #     for valores in cantidad_por_id:
    #         datos=valores.amount_total
    #         print datos
    # product_product_busqueda=self.search([])
    # for valores in product_product_busqueda:
    #     print self.env['res.partner'].search([('id','=',valores.id)]).name

    #Funcion para el envio de email cuando la cantidad sea minima de dicho producto con crontab de 1 days.
    def envio_mail_cantidad_minima_products(self, cr, uid, context=None):
        servidor_ids = self.pool.get('res.users').browse(cr, uid, uid)
        servidor_id=self.pool.get('ir.mail_server').search(cr,uid,[('smtp_user','=',"oocampo@bpmtech.com")])
        if len(servidor_id):
            servidor=servidor_id[0]
        else:
            raise osv.except_osv(('¡Error!'),('Sin servicio configurado de email.'))

        servidor=self.pool.get('ir.mail_server').browse(cr,uid,servidor)
        cantidad_product_product=self.pool.get('product.product').search(cr,uid,[('cantidad_minima','!=',0)])

        for id_producto in self.pool.get('product.product').browse(cr, uid,cantidad_product_product):
            var_stock=self.pool.get('stock.quant').search(cr,uid,[('product_id','=',id_producto.id)])
            var_stock_b=sum(self.pool.get('stock.quant').browse(cr,uid,var_stock).mapped('qty'))
            producto_info=id_producto.name_template

            print var_stock_b,id_producto.cantidad_minima

            if var_stock_b<id_producto.cantidad_minima:
                context={}
                context["receptor_email"]='lortega@bpmtech.com'
                context['correo_from']=servidor.smtp_user
                context['nombre_form']=servidor.smtp_user
                context['producto_info']=producto_info
                src_tstamp_str = tools.datetime.now().strftime(tools.misc.DEFAULT_SERVER_DATETIME_FORMAT)
                src_format = tools.misc.DEFAULT_SERVER_DATETIME_FORMAT
                dst_format = DEFAULT_SERVER_DATETIME_FORMAT #format you want to get time in.
                dst_tz_name = self.pool.get('res.users').browse(cr, uid, uid, context=context).tz or 'Mexico/General'
                _now = tools.misc.server_to_local_timestamp(src_tstamp_str, src_format, dst_format, dst_tz_name)
                context['fecha_cotizacion']=_now
                template = self.pool.get('ir.model.data').get_object(cr, SUPERUSER_ID, 'lafox', 'template_email_cantidad_minima_producto')
                self.pool['email.template'].send_mail(cr, uid, template.id, id_producto.id, force_send=True, context=context)

    #Funcion para permitir redireccionar la vista a otro modelo
    def _get_act_window_dict(self, cr, uid, name, context=None):
        mod_obj = self.pool.get('ir.model.data')
        act_obj = self.pool.get('ir.actions.act_window')
        result = mod_obj.xmlid_to_res_id(cr, uid, name, raise_if_not_found=True)
        result = act_obj.read(cr, uid, [result], context=context)[0]
        return result

    #Funcion permite visulizar del producto
    def action_open_quants(self, cr, uid, ids, context=None):
        products = self._get_products(cr, uid, ids, context=context)
        result = self._get_act_window_dict(cr, uid, 'stock.product_open_quants', context=context)
        result['domain'] = "[('product_id','in',[" + ','.join(map(str, products)) + "])]"
        result['context'] = "{'search_default_locationgroup': 1, 'search_default_internal_loc': 1}"
        return result

    #Funcion para retornar los productos
    def _get_products(self, cr, uid, ids, context=None):
        products = []
        for prodtmpl in self.browse(cr, uid, ids, context=None):
            products += [x.id for x in prodtmpl.product_variant_ids]
        return products

    # Cron que permite actualizar los registros de cada producto vendido
    @api.model
    def _cron_execute_ventas(self):
        # Se realiza un busqueda para todas las ventas menores o iguales a hoy con el status pagado
        for search_id_ventas in self.env['account.invoice'].search([('fecha_venta','<=',fields.Date.today()),('state','=','paid')]):
            for product in search_id_ventas.invoice_line:
                # Por cada Venta se obtienen los productos vendidos
                search_product = self.env['lafox.seguimiento.venta.producto'].search([('id_invoice_line','=',product.id)])
                line=[]
                res={}
                res['value']={}
                # Si no se han registrado, se asignan a los registros de cada producto
                if not search_product:
                    dic_lista = {}
                    dic_lista['fecha_venta'] = search_id_ventas.fecha_venta
                    dic_lista['cantidad'] = product.quantity
                    dic_lista['costo'] = product.price_subtotal
                    dic_lista['cliente_venta'] = search_id_ventas.partner_id.id
                    dic_lista['venta_realizada'] = search_id_ventas.nomenclatura
                    dic_lista['id_invoice_line'] = product.id
                    dic_lista['account_ids'] = product.product_id.id

                    self.env['lafox.seguimiento.venta.producto'].sudo().create(dic_lista)
        return True

    @api.model
    def _cron_excute_qty_venta(self):
        # Se crean las constantes para la lista y las fechas de busqueda
        lines=[]
        today=datetime.now()
        dateMonthStart="%s-%s-01" % (today.year, today.month)
        dateMonthEnd="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month)[1])
        # Se crea una busqueda por todas las ventas pagadas y realizadas en el transcurso del mes actual, y los conceptos registrados dentro de cada venta
        for account in self.env['account.invoice'].search([('state','=','paid'),('create_date','>',dateMonthStart),('create_date','<',dateMonthEnd)]):
            for registros in self.env['account.invoice.line'].search([('create_date','>',dateMonthStart),('create_date','<',dateMonthEnd),('invoice_id','=',account.id)]):
                dic_list = {}
                # Si el mes vuelve a iniciar se cambiar todos los estatus inicial
                date_invoice = fields.Date.today()
                if registros.product_id.mes_venta != str(date_invoice[5:7]):
                    registros.product_id.sudo().write({'mes_venta':str(date_invoice[5:7]),'porcentaje_vendido':0.0,'state_product':None})
                # De lo contrario se creaa una lista de diccionarios con todas las ventas realizadas
                else:
                    dic_list['id_valor'] = int (registros.product_id.id)
                    dic_list['name'] = registros.product_id.name
                    dic_list['cantidad'] = registros.quantity

                lines.append(dic_list)

        # Si existe un diccionario y no es nulo se crea un nuevo diccionario y se agrupan por el valor de id_producto
        if lines != []:
            list1 = []
            for key, items in itertools.groupby(lines, operator.itemgetter('id_valor')):
                list1.append(list(items))

            # Para cada agrupación se hace la suma de sus cantidades vendias y se ajusta a que porcentaje y estatus correspondec
            for productos in list1:
                cant_qty = 0
                for sum_value in productos:
                    cant_qty = cant_qty + float(sum_value['cantidad'])

                cant_qty = cant_qty * 10 #[TODO]Se agrega porcentaje fijo en lo que se otorga regla de negocio real

                if cant_qty < 20:
                    state = 'MUY_MALO'
                elif cant_qty < 40 and cant_qty >= 20:
                    state = 'MALO'
                elif cant_qty < 60 and cant_qty >= 40:
                    state = 'REGULAR'
                elif cant_qty < 80 and cant_qty >= 60:
                    state = 'BUENO'
                else:
                    state = 'EXCELENTE'

                # Por cada registro se agrega a cada producto los valors correspondientes en mes de venta, pocertaje ventido y el estatus de cada producto
                id_product_product =  self.env['product.product'].search([('id','=',productos[0]['id_valor'])])
                id_product_product.sudo().write({'mes_venta':str(date_invoice[5:7]),'porcentaje_vendido':cant_qty,'state_product':state})

product_product()

#Class para llenar product.product->grupo_invetario
class lafox_grupo_de_inventarios(models.Model):
    _name='lafox.grupo.de.inventarios'

    # FIELDS PARA lafox_grupo_de_inventarios
    nombre=fields.Char(string='Grupo de inventario',require=True)
    nomenclatura=fields.Char(string='Nomenclatura',required=True)

lafox_grupo_de_inventarios()

class account_invoice(models.Model):
    _name = 'account.invoice'
    _rec_name = "nomenclatura"
    _inherit = 'account.invoice'

    # FUNCION PARA OBTNER EL TOTAL LETRA Y CENTAVOS
    @api.multi
    @api.depends('amount_total')
    def _get_importe_letra(self):
        dic = {}
        decimal = self.get_centavos_letra(self.amount_total)
        importeletra = (number_to_letter.to_word(int(self.amount_total)) + " MXN " + decimal + "/100 ").upper()
        self.total_con_letra = str(importeletra)
        dic[self.id] = importeletra
        return dic

    def get_centavos_letra(self, cantidad):
        centavos = ""
        cantidad_str = str(cantidad)
        cantidad_splitted = cantidad_str.split('.')
        if len(cantidad_splitted) > 1:
            if len(cantidad_splitted[1]) == 1:
                centavos = cantidad_splitted[1] + "0"
            else:
                centavos = cantidad_splitted[1]
        else:
            centavos = "00"
        return centavos

    # Funcion que permite llenar el almacen para ventas segun sea el usuario de ventas
    @api.multi
    @api.depends('user_id')
    def _compute_tipo_almacen(self):
        email = self.user_id.login
        employee_id =  self.env['hr.employee'].search([('work_email','=',email)])
        if employee_id:
            self.stock_venta = employee_id[0].almacenes_id
            if employee_id[0].almacenes_id.complete_name == 'Physical Locations / WH / LOCAL PRODUCTOS TERMINADO':
                self.tipo_producto = '1'
            elif employee_id[0].almacenes_id.complete_name == 'Physical Locations / WH / LOCAL PRODUCTOS ACCESORIOS':
                self.tipo_producto = '0'
            else:
                return False

    #FIELDS PARA ACCOUNT.INVOICE
    nomenclatura = fields.Char(string='Código Nomenclatura')
    fecha_venta = fields.Datetime(string='Fecha de Venta', default=datetime.now())
    tipo_venta = fields.Selection(LAFOX_TYPE_SELECT_VF, string='Tipo de Venta')
    tipo_producto = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO, string='Tipo de Producto', compute='_compute_tipo_almacen', store='True')
    validador=fields.Boolean(string='Pedido con Envio',default='False')
    stock_venta = fields.Many2one('stock.location', string='Tipo de Almacen', compute='_compute_tipo_almacen',store='True')
    # FIELDS PARA FACTURACION
    lugar_exp = fields.Char(string='Lugar y Fecha de Expedicón', index=True, default='MIGUEL HIDALGO, DF')
    fecha_certificacion = fields.Datetime(string='Fecha y Hora de Certificación', index=True)
    fecha_emision = fields.Datetime(string='Fecha y Hora de Emsión', index=True)
    tipo_comprobante = fields.Selection(TIPO_COMPROBANTE_LISTA, string='Tipo de Comprobante', index=True)
    folio_fiscal = fields.Char(string='Folio Fiscal', index=True)
    serie = fields.Char(string='Serie', index=True)
    folio = fields.Char(string='Folio', index=True)
    no_serie_csd_sat = fields.Char(string='NO. Serie CSD de SAT', index=True)
    no_serie_csd_emisor = fields.Char(string='NO. Serie CSD de Emisor', index=True)
    RfcProvCertif = fields.Char(string='RfcProvCertif', index=True)
    metodo_pago = fields.Selection(METODO_PAGO_SELECTION, string='Metodo de Pago', index=True)
    forma_pago = fields.Selection(FORMA_PAGO_SELECTION, string='Forma de Pago', index=True)
    total_con_letra = fields.Char(string='Total con Letra', index=True, compute='_get_importe_letra', store=True)
    cadena_original_s = fields.Char(string='Cadena Original Del Complemento De Certificación Digital Del SAT:', index=True)
    sello_digita_emisor = fields.Char(string='Sello Digital Del Emisor', index=True)
    sello_digita_sat = fields.Char(string='Sello Digital Del SAT', index=True)
    state_ac = fields.Selection(ACCOUNT_STATE, string="Estado", default='draft')
    bind = fields.Boolean (string = "Timbrado", invisible='True')
    xml_64 = fields.Binary(string="XML timbrado",)
    xml_64_cancelado = fields.Binary(string="XML Cancelado",)
    name_facturacion = fields.Char(string='nombre', index=True)
    pass_facturacion = fields.Char(string='pass', index=True)
    qr= fields.Char(string='Codigo QR', size=120)
    acuse = fields.Binary(string="Acuse",)
    regimen_fiscal = fields.Selection(REGIMEN_FISCAL, string='Regimen Fiscal')
    uso_cfdi = fields.Selection(USO_CFDI, string='Uso CFDI')
    # Se modifica el create para poder crear un Codigo irrepetible por cotización
    # [TODO]---Se pude modificar por 'ir.sequence'
    def create(self, cr, uid, values, context=None):
        #validacion de bandera en 'lafox.valida.estatus.boton' cambia a True si las facturas estan en estatus 'paid'
        if self.pool.get('lafox.valida.estatus.boton').search(cr,uid,[('estatus','=',True)]):
            raise osv.except_osv(('¡Error!'),('Ya NO PUEDES realizar mas VENTAS.'))
        else:
            if values['tipo_venta'] == 'FACTURA' and values['tipo_producto'] == '0':
                type_p = 'ACC'
                # Se realiza busqueda para revisar todos los coodigos
                records_fact = self.pool.get('account.invoice').search(cr, SUPERUSER_ID, [('nomenclatura','!=',False),('tipo_venta','=','FACTURA'),('tipo_producto','=','0')], context=context)
                # Si no hay codigos, se inicia en 1 el conteo
                if records_fact == []:
                    new_subfijo = 1
                # Si encuentra trae el ultimo de todos mayor de todos y le aumenta uno
                else:
                    segunda_busqueda = self.browse(cr,uid, records_fact)
                    lista_subfijos = []
                    for elemento in segunda_busqueda:
                        matri = elemento.nomenclatura
                        subfix_temp = int(matri[14:])
                        lista_subfijos.append(subfix_temp)
                    maximo_ele = max(lista_subfijos)
                    new_subfijo = maximo_ele + 1

                # Crea el codígo con el subfijo y la nomenclatura
                anio = str(date.today().year)
                code = 'FACT-'+type_p+'-'+anio+'-'+str(new_subfijo).zfill(6)
                values['nomenclatura'] = code

            elif values['tipo_venta'] == 'FACTURA' and values['tipo_producto'] == '1':
                type_p = 'TER'
                # Se realiza busqueda para revisar todos los coodigos
                records_fact = self.pool.get('account.invoice').search(cr, SUPERUSER_ID, [('nomenclatura','!=',False),('tipo_venta','=','FACTURA'),('tipo_producto','=','1')], context=context)
                # Si no hay codigos, se inicia en 1 el conteo
                if records_fact == []:
                    new_subfijo = 1
                # Si encuentra trae el ultimo de todos mayor de todos y le aumenta uno
                else:
                    segunda_busqueda = self.browse(cr,uid, records_fact)
                    lista_subfijos = []
                    for elemento in segunda_busqueda:
                        matri = elemento.nomenclatura
                        subfix_temp = int(matri[14:])
                        lista_subfijos.append(subfix_temp)
                    maximo_ele = max(lista_subfijos)
                    new_subfijo = maximo_ele + 1

                # Crea el codígo con el subfijo y la nomenclatura
                anio = str(date.today().year)
                code = 'FACT-'+type_p+'-'+anio+'-'+str(new_subfijo).zfill(6)
                values['nomenclatura'] = code

            elif values['tipo_venta'] == 'VENTA' and values['tipo_producto'] == '0':
                type_p = 'ACC'
                # Se realiza busqueda para revisar todos los coodigos
                records_venta = self.pool.get('account.invoice').search(cr, SUPERUSER_ID, [('nomenclatura','!=',False),('tipo_venta','=','VENTA'),('tipo_producto','=','0')], context=context)
                # Si no hay codigos, se inicia en 1 el conteo
                if records_venta == []:
                    new_subfijo = 1
                # Si encuentra trae el ultimo de todos mayor de todos y le aumenta uno
                else:
                    segunda_busqueda = self.browse(cr,uid, records_venta)
                    lista_subfijos = []
                    for elemento in segunda_busqueda:
                        matri = elemento.nomenclatura
                        subfix_temp = int(matri[13:])
                        lista_subfijos.append(subfix_temp)
                    maximo_ele = max(lista_subfijos)
                    new_subfijo = maximo_ele + 1

                # Crea el codígo con el subfijo y la nomenclatura
                anio = str(date.today().year)
                code = 'VEN-'+type_p+'-'+anio+'-'+str(new_subfijo).zfill(6)
                values['nomenclatura'] = code


            else:
                type_p = 'TER'
                # Se realiza busqueda para revisar todos los coodigos
                records_venta = self.pool.get('account.invoice').search(cr, SUPERUSER_ID, [('nomenclatura','!=',False),('tipo_venta','=','VENTA'),('tipo_producto','=','1')], context=context)
                # Si no hay codigos, se inicia en 1 el conteo
                if records_venta == []:
                    new_subfijo = 1
                # Si encuentra trae el ultimo de todos mayor de todos y le aumenta uno
                else:
                    segunda_busqueda = self.browse(cr,uid, records_venta)
                    lista_subfijos = []
                    for elemento in segunda_busqueda:
                        matri = elemento.nomenclatura
                        subfix_temp = int(matri[13:])
                        lista_subfijos.append(subfix_temp)
                    maximo_ele = max(lista_subfijos)
                    new_subfijo = maximo_ele + 1

                # Crea el codígo con el subfijo y la nomenclatura
                anio = str(date.today().year)
                code = 'VEN-'+type_p+'-'+anio+'-'+str(new_subfijo).zfill(6)
                values['nomenclatura'] = code

            # print values
            create = super(account_invoice, self).create(cr, uid, values, context=context)
            return create
            # return 0

    # FUNICON PARA LA CONFIRMACION DE LOS MOVIMIENTOS
    def _create_and_confirm_move(self, cr, uid, ids, vals_stok_move,context=None):
        print vals_stok_move
        ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
        self.pool.get('stock.move').action_done(cr, uid, ide, context=context)

    @api.multi
    def action_paid_venta(self):
        passed = 0
        self.button_reset_taxes()
        # Obtnemo las localizaciones de destino y de origen
        search_id_loc = self.env['stock.location'].search([('complete_name','ilike',self.stock_venta.complete_name)])
        search_id_loc_venta = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / VENTAS')])
        # Por cada producto se revisa que haya suficiente en el stock
        for producto in self.invoice_line:
            sum_qty = sum(self.env['stock.quant'].search([('location_id','=',self.stock_venta.id),('product_id', '=',producto.product_id.id)]).mapped('qty'))
            # Si algun producto no es suficiente se manda warning
            if producto.quantity > sum_qty:
                raise osv.except_osv(("No es posible realizar esta operación"), ('EL Producto %s no tiene disponible la cantidad mencionada.\n Cantidad a vender: %s Cantidad en stock: %s'%(producto.product_id.name,producto.quantity,sum_qty)))
            # De lo conrario se guarda u estatus
            else:
                passed = 1
        # Si cambia el status passed se crean los movimientos para descontar del almacen a un almacen de ventas
        if passed == 1:
            for sell_product in self.invoice_line:
                vals_stok_move= {
                            'location_dest_id': search_id_loc_venta[0].id,
                            'location_id': search_id_loc[0].id,
                            'name': str('FV:VENTA: '+ sell_product.product_id.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(sell_product.product_id.id),
                            'product_uom': int(sell_product.product_id.uom_id.id),
                            #'product_qty': float(tupple_taller.cantidad),
                            'product_uom_qty': float(sell_product.quantity),
                            'propagate': True,

                            }
                # print vals_stok_moves
                self._create_and_confirm_move(vals_stok_move)

        # Una vez realizado la venta se cambia el estatus a pagado
        self.write({'state':'open'})

        #TO-DO-validation
        if self.validador==True:
            dic_list={
            'estatus':'P',
            'grupo_ventas_facturacion':self.nomenclatura,
            }
            get_name=self.env['lafox.seguimiento.pedido'].sudo().create(dic_list)

        return True

    @api.multi
    def button_action_cancel_draft(self):
        if self.state == 'paid' or self.state=='open':
            search_id_loc = self.env['stock.location'].search([('complete_name','ilike',self.stock_venta.complete_name)])
            search_id_loc_venta = self.env['stock.location'].search([('complete_name','ilike','VIRTUAL LOCATIONS / VENTAS')])
            if self.state == 'paid':
                amount_total_n  = self.amount_total * (-1)
            else:
                amount_total_n = 0.0
            for conceptos in  self.invoice_line:
                vals_stok_move= {
                            'location_dest_id': search_id_loc[0].id,
                            'location_id': search_id_loc_venta[0].id,
                            'name': str('FV:VENTA: '+ conceptos.product_id.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(conceptos.product_id.id),
                            'product_uom': int(conceptos.product_id.uom_id.id),
                            #'product_qty': float(tupple_taller.cantidad),
                            'product_uom_qty': float(conceptos.quantity),
                            'propagate': True,

                            }
                # print vals_stok_moves
                self._create_and_confirm_move(vals_stok_move)
            self.sudo().write({'state': 'cancel','amount_total':amount_total_n})
            self.delete_workflow()
            self.create_workflow()

        return True

account_invoice()

class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = 'account.invoice.line'

    #FIELDS PARA account_invoice_line
    image_product = fields.Binary(string='Imagen')

    def _onchange_image_product(self, cr, uid, ids, id_producto, context):
        print "Entra la on_change con id ", id_producto
        print "on stock moveeee "
        # res_prod = super(stock_move, self).onchange_product_id(cr, uid, ids, prod_id, loc_id,loc_dest_id, partner_id)
        # prod_obj = self.pool.get('product.product')
        # obj = prod_obj.browse(cr, uid, prod_id)
        # res_prod['value'].update({'image_product': obj.image_product})
        # return res_prod

        # res = {}
        # if 'tipo_producto' in context:
        #     valor =  context['tipo_producto']
        #     res['domain'] ={}
        #     res['domain']['producto'] = [('c_t','=',valor)]
        #     print tipo_producto
        #     if tipo_producto !='1':
        #         if tipo_producto != '0':
        #             atributos = self.pool.get('product.product').browse(cr, uid, tipo_producto, context=context)
        #             res['value']={
        #                 'descripcion' : atributos.description,
        #                 'piezas' : atributos.cantidad_minima
        #             }
        # return res


account_invoice_line()


class lafox_inventario_producto(models.Model):
    _name = 'lafox.inventario.producto'

    @api.multi
    def _default_usr_id(self):
        return self.env.user.id

    # FIELDS PARA lafox_inventario_producto
    tipo_producto = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO,string='Selecciona un Área')
    producto = fields.Many2one('product.product', string='Producto')
    descripcion = fields.Char(string='Descripción')
    piezas = fields.Char(string='Piezas')
    cantidad = fields.Float(string='Cantidad')
    responsable = fields.Many2one('res.users',string='Responsable', default= _default_usr_id)
    product_id = fields.One2many('lafox.inventario.producto','product_ids', string='Productos ID')
    product_ids = fields.Many2one('lafox.inventario.producto', string='Productos ID')

    # FUNCIONES PARA lafox_inventario_producto
    # Funcion para carga de inventario
    def button_asignar_inventario(self, cr, uid, ids, context=None):
        # Se obtine los datos de la vista acutal
        tabla_crm_lead = self.pool.get('lafox.inventario.producto').browse(cr, uid, ids[0], context=context)
        # Obtenemos los dos stock entre los que se hará el movimiento, de abastecimiento virtual --> stock WH
        #search_id_loc = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Ubicaciones físicas / WH / Existencias')], context=context)
        search_id_loc = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Physical Locations / WH / Stock')], context=context)
        search_id_loc_abas = self.pool.get('stock.location').search(cr, uid, [('complete_name','ilike','Virtual Locations / Procurements')], context=context)

        # Por cada producto se realiza el movimiento correspondiente
        for move in  tabla_crm_lead.product_id:
            vals_stok_move= {
                            'location_dest_id': search_id_loc[0], #12, ## por el  momento ira definido
                            'location_id': search_id_loc_abas[0], #6, ## por el  momento ira definido
                            'name': str('FV:INV:ABAST: '+   move.producto.name),
                            'company_id': 1, #por el momento definido
                            'invoice_state': "none",
                            'partially_available': False,
                            'procure_method': "make_to_stock",
                            'product_id': int(move.producto.id),
                            'product_uom': int(move.producto.uom_id.id),
                            # 'product_qty': float(move.cantidad),
                            'product_uom_qty': float(move.cantidad),
                            'propagate': True,
                            'responsable_id':move
                        }
            ide = self.pool.get('stock.move').create(cr, uid, vals_stok_move, context=context)
            self.pool.get('stock.move').action_done(cr, uid, ide, context=context)
        return True

    def _onchange_domain_producto(self, cr, uid, ids, tipo_producto, context):
        res = {}
        if 'tipo_producto' in context:
            valor =  context['tipo_producto']
            res['domain'] ={}
            res['domain']['producto'] = [('c_t','=',valor)]
            print tipo_producto
            if tipo_producto !='1':
                if tipo_producto != '0':
                    atributos = self.pool.get('product.product').browse(cr, uid, tipo_producto, context=context)
                    res['value']={
                        'descripcion' : atributos.description,
                        'piezas' : atributos.cantidad_minima
                    }
        return res

lafox_inventario_producto()

#Class para llenar product.product->grupo_precio
class lafox_escala_de_precios(models.Model):
    _name='lafox.grupo.de.precios'
    nombre=fields.Char(string='Grupo de precios',require=True)
    nomenclatura=fields.Char(string='Nomenclatura',required=True)
    descuento=fields.Integer(string='Descuento aplicado',require=True)

#Class res.partner para clientes LAFOX
class res_partner(models.Model):
    _name='res.partner'
    _inherit='res.partner'

    #Campos para los Valores del Cliente
    clave_cliente=fields.Char(string='Clave del cliente',require=True)
    lada_cliente=fields.Char(string='Lada', require=True,size=3)
    WhatsApp=fields.Char(string='WhatsApp', require=True,size=10)
    vendedor=fields.Many2one('lafox.clientes.vendedor',string='Vendedor',require=True)
    medio_contacto=fields.Selection(LAFOX_MEDIO_CONTACTO,string='Medio de contacto',require=True)
    referencia=fields.Char(string='Referencia',require=True)
    observaciones=fields.Text(string='Observaciones',require=True)

    #Campos para los Valores del Cliente
    rfc_cliente=fields.Char(string="R.F.C",size=13,require=True)
    metodo_pago=fields.Selection(METODO_PAGO_SELECTION,sting='Metodo de pago')
    fisica_moral=fields.Selection(LAFOX_SELECT_TIPO_CLIENTE,require=True,string='Fisica o Moral')
    moneda_valores=fields.Selection([('PESOS', 'MXN-PESOS'),('DOLARES', 'DLLS-DOLARES')],string='Moneda',require=True)
    limite_credito=fields.Float(string='Limite de Credito',require=True)
    dias_credito=fields.Char(string='Dias de Credito',require=True,size=2)
    escala_precios=fields.Char(string='Grupo de Precios',require=True,size=1)

    #Campos para los Valores del bloque Informativo del Cliente
    metodo_pago_readonly=fields.Selection(METODO_PAGO_SELECTION,string='Metodo de pago',readonly=True)
    saldo_pendiente=fields.Float(string='Saldo pendiente',readonly=True)
    promedio_compra_mensual=fields.Float(string='Compra mensual',readonly=True)
    mayor_compra_mensual=fields.Float(string='Compra mayor',readonly=True)
    ultima_compra_mensual=fields.Float(string='Ultima compra',readonly=True)
    puntualidad_de_pago=fields.Selection(LAFOX_PUNTUALIDAD_PAGO_CLIENTE,string='Puntualidad de pago',require=True)

    # FUNCIONES PARA RES_PARTNER

    # Función que permmite verificar que el RFC para facturar sea el correcto
    @api.multi
    def validate_rfc(self):
        if self.rfc_cliente == "XEXX010101000" or self.rfc_cliente == "XAXX010101000":
            return True
        else:
            try:
                retorno = validate( self.rfc_cliente, validate_check_digits=True)
                return True
            except:
                raise osv.except_osv(("¡Error!"),('El RFC no es Valido, Favor de verificar'))

    def _menor_lista_1(self, cr, uid, ids, lista,context=None):
        mayor = lista[0]['amount']
        # print mayor de lista
        if valor > mayor:
            mayor = valor
        return mayor

    # Cron que permite actualizar los registros de cada producto vendido
    @api.model
    def _cron_execute_ventas_por_cliente(self):
        today=datetime.now()
        dateMonthStart="%s-%s-01" % (today.year, today.month)
        dateMonthEnd="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month)[1])
        line=[]
        # Se crea una busqueda por todas las ventas pagadas y realizadas en el transcurso del mes actual
        for cliente_id in self.env['res.partner'].search([]):
            for account in self.env['account.invoice'].search([('state','=','paid'),('create_date','>',dateMonthStart),('create_date','<',dateMonthEnd),('partner_id','=',cliente_id.id)]):
                dic_line = {}
                dic_line['name']=cliente_id.name
                dic_line['name_id']=cliente_id.id
                dic_line['id_acount']=account.id
                dic_line['amount']=account.amount_total
                line.append(dic_line)


        # Si existe un diccionario y no es nulo se crea un nuevo diccionario y se agrupan por el valor de id_producto
        if line != []:
            list1 = []
            for key, items in itertools.groupby(line, operator.itemgetter('name')):
                list1.append(list(items))

            # Para cada agrupación se hace la suma de sus cantidades vendias y se ajusta a que porcentaje y estatus corresponde
            for ventas in list1:
                venta_m = self._menor_lista_1(ventas)
                partner_id = self.env['res.partner'].search([('id','=',venta_m['name_id'])])
                partner_id.sudo().write({'mayor_compra_mensual':venta_m['amount']})
            # print ventas

res_partner()

class ir_attachment(osv.osv):
    _name = 'ir.attachment'
    _inherit = 'ir.attachment'

    def asignar_products(self, cr, uid, ids, context=None):
        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('ir.attachment').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        file_name, file_extension = os.path.splitext(datas_fname)

        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_partner = cargar_MA(archivo_cargado)
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        for dato in datos_partner:
            # vals['CLAVE'] = dato['CLAVE']
            # vals['CODE_BARRAS'] = dato['CODE_BARRAS']
            # vals['DESCRIPCION'] = dato['DESCRIPCION']
            # vals['UNIDDAD'] = dato['UNIDDAD']
            # vals['GPO_PRECIO'] = dato['GPO_PRECIO']
            # vals['REFERENCIA'] = dato['REFERENCIA']
            # vals['GPO_INVENTARIO'] = dato['GPO_INVENTARIO']
            # vals['MONEDA'] = dato['MONEDA']
            # vals['IVA'] = dato['IVA']
            # vals['PRECIO_BASE'] = dato['PRECIO_BASE']
            # vals['OBSERVACION'] = dato['OBSERVACION']
            # vals['ACTIVO'] = dato['ACTIVO']
            # vals['PROVEEDOR'] = dato['PROVEEDOR']
            # Creamos un nuevo registro en product.product con los valores del diccionario
            print dato
            # new_id = self.pool.get('product.product').create(cr,uid, vals, context=context)

        # return new_id

    def asignar_partner(self, cr, uid, ids, context=None):
        # Declaramos el diccionario para la creación de un partner y obtenemos el archivo que se subio
        vals={}
        attachment_dic = self.pool.get('ir.attachment').read(cr, uid, ids, ['name', 'store_fname', 'datas_fname'], context=context)
        filename = attachment_dic[0]['store_fname']
        datas_fname = attachment_dic[0]['datas_fname']
        file_name, file_extension = os.path.splitext(datas_fname)

        archivo_cargado = ODOO_HOME + '.local/share/Odoo/filestore/' + cr.dbname + '/' + filename
        # Consusmimos el script para el parseo del excel, obteniendo los valores
        datos_partner = cargar_PT(archivo_cargado)
        # Por cada fila del xls creamos un registro con los valores que corresponden a la vista
        for dato in datos_partner:
            vals['CLAVE'] = dato['CLAVE']
            vals['name'] = dato['NOMBRE']
            vals['street'] = dato['DIRECCION']
            vals['street2'] = dato['COLONIA']
            vals['city'] = dato['CIUDAD_DELEG']
            vals['state_id'] = dato['ESTADO']
            vals['zip'] = dato['ZIP']
            vals['country_id'] = dato['PAIS']
            vals['lada_cliente'] = dato['LADA']
            vals['phone'] = dato['TELEFONO']
            vals['mobile'] = dato['MOBILE']
            vals['email'] = dato['EMAIL']
            vals['vendedor'] = dato['VENDEDOR']
            vals['medio_contacto'] = dato['MEDIO_CONTACTO']
            vals['referencia'] = dato['REFERENCIA']
            vals['observaciones'] = dato['OBSERVACION']
            vals['rfc_cliente'] = dato['RFC']
            vals['metodo_pago'] = dato['METODO_PAGO']
            vals['fisica_moral'] = dato['FISICA_MORAL']
            vals['moneda_valores'] = dato['MONEDA']
            vals['limite_credito'] = dato['LIMITE_CREDITO']
            vals['dias_credito'] = dato['DIAS_CREDITO']
            vals['escala_precios'] = dato['ESCALA_PRECIOS']
            vals['saldo_pendiente'] = dato['SALDO_PENDIENTE']
            vals['promedio_compra_mensual'] = dato['PROMEDIO_COMPRA_M']
            vals['mayor_compra_mensual'] = dato['COMPRA_MAYOR']
            vals['ultima_compra_mensual'] = dato['ULT_COMPRA']
            vals['puntualidad_de_pago'] = dato['PUNTUALIDAD_PAGO']
            # Creamos un nuevo registro en product.product con los valores del diccionario
            print vals
            # new_id = self.pool.get('product.product').create(cr,uid, vals, context=context)

        # return new_id


class seguimiento_pedido(models.Model):
    _name='lafox.seguimiento.pedido'

    pedido=fields.Char(string='Pedido',require=True,size=13,help='Introduce el numero del pedido a Enviar')
    estatus=fields.Selection(LAFOX_SELECT_ESTATUS_PEDIDO,require=True,string='Estatus del Pedido')
    contacto_seguimiento=fields.Char(string='Contacto de seguimiento')
    fecha_envio= fields.Datetime(string='Fecha y Hora de envio')
    fecha_entrega= fields.Datetime(string='Fecha y Hora de entrega')
    grupo_ventas_facturacion=fields.Char(string='Ventas y Facturacion',require=True)
    descripcion=fields.Text(string='Observaciones y notas...')
    ventas_ids = fields.Many2one('account.invoice', string='Venta')

seguimiento_pedido()

class lafox_seguimiento_venta_producto(models.Model):
    _name='lafox.seguimiento.venta.producto'
    # Fields para modelo lafox_seguimiento_venta_producto
    fecha_venta = fields.Datetime(string='Fecha de Venta')
    cantidad = fields.Float(string='Cantidad')
    costo = fields.Float(string='Costo-Venta')
    cliente_venta = fields.Many2one('res.partner', string='Cliente')
    account_ids = fields.Many2one('product.product', string='account Id')
    venta_realizada = fields.Char(string='Venta')
    id_invoice_line = fields.Integer(string='In invoice')

lafox_seguimiento_venta_producto()

class res_users(models.Model):
    _name = 'res.users'
    _inherit = 'res.users'

    #FIELDS PARA RES USERS
    # almacenes_id = fields.Many2one('stock.location', string='Almacen')

res_users()
class hr_employee(models.Model):
    _name = 'hr.employee'
    _inherit = 'hr.employee'

    # FIELDS PARA MODEL hr_employee
    departamento_user = fields.Many2one('res.groups', string='Departamento')
    almacenes_id = fields.Many2one('stock.location', string='Almacen')
    action_id = fields.Many2one('ir.actions.actions', string='Acción Inicial')

    # # Modificcación de Create para poder crear usuarios sin necesidad de hacer los dos pasos
    @api.model
    def create(self, vals):
        employee_id = self.env['stock.location'].search([('id','=',int(vals['almacenes_id']))])
        if employee_id:
            almacen_ids = employee_id[0].id
        else:
            almacen_ids = False
        vals_users = {
            'groups_id': [
                [6, False, [int(vals['departamento_user'])]]
            ],
            'name': vals['name'],
            'mobile': vals.get('tel_celular', False),
            'image': vals.get('image_medium', False),
            'phone': vals['work_phone'],
            'login': vals.get('work_email', False),
            'email': vals['work_email'],
            'almacenes_id': almacen_ids,
            'action_id': vals['action_id'],
        }

        self.env['res.users'].sudo().create(vals_users)
        rec = super(hr_employee, self).create(vals)
    #     # ...
        return rec

hr_employee()

class hr_asistencia_employee(models.Model):
    _name = 'hr.asistencia.employee'

    # FIELDS PARA MODEL hr_asistencia_employee
    name = fields.Many2one('hr.employee',string='Empleado', required=True, index=True)
    hora_inicio = fields.Datetime(string='Fecha y hora Asistencia', required=True, index=True )
    hora_display = fields.Datetime(string='Fecha y hora Asistencia', required=True, index=True)
    hora_display_fin = fields.Datetime(string='Final echa y hora Asistencia', required=True, index=True)
    estatus = fields.Selection(LAFOX_SELECT_STATE_CLIENTE ,string='Estatus Asistencia', readonly=True)
    # estatus = fields.Selection(LAFOX_SELECT_STATE_CLIENTE ,string='Estatus Asistencia', readonly=True, compute='_compute_state_employee')

    # Funciones para hr_asistencia_employee
    # @api.one
    # @api.depends('name')
    # def _compute_state_employee(self):
    #     self.estatus =  "0"

    # Función que permite responder el .py para el consumo del ZKT Biometrico
    # [TODO] A espera de revisión de que registros se deberan tomar
    @api.multi
    def value_assistence(self,asistencias):
        print asistencias
        # Obtenemos las zonas horarias para el pintado correcto en Odoo y para la hora incial correspondiente a la CDMX
        UTC_DATE = datetime.utcnow()
        tz=pytz.timezone('America/Mexico_City')
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        STC_DATE  = pytz.utc.localize(UTC_DATE,DATETIME_FORMAT).astimezone(tz)
        UTC_DATE = datetime.strptime(str(UTC_DATE)[0:19],DATETIME_FORMAT)
        STC_DATE = datetime.strptime(str(STC_DATE)[0:19],DATETIME_FORMAT)
        UTC_DATE_TIME =UTC_DATE - STC_DATE
        TZ_TIMEDELTA= (UTC_DATE_TIME.seconds/3600)

        # Si el .py trae registros se obtienen las fechas,nombres y estatus para cada registro.
        for asistencia_usr in asistencias:
            someday = datetime.strptime(str(asistencia_usr[2])[0:8], '%Y%m%d')
            fecha_inicio =  datetime.strptime(str(asistencia_usr[2]), '%Y%m%dT%H:%M:%S')
            display_  = fecha_inicio + timedelta(hours=TZ_TIMEDELTA)
            display_fin  = display_ + timedelta(minutes=20)

            if someday.date()>= date.today():
                variable_estatus = random.randint(0, 2)#[TODO]SE COLOCARA RANDOM EN LO QUE SE DEFINE LA REGLA DE ESTADO

                employee_id = self.env['hr.employee'].search([('otherid','=',int(asistencia_usr[0]))])
                if len(employee_id)>0:
                    values = {}
                    values['name'] = employee_id[0].id
                    values['hora_inicio'] = fecha_inicio
                    values['estatus'] = str(variable_estatus)
                    values['hora_display'] = display_
                    values['hora_display_fin'] = display_fin
                    # Se crea el registro en odoo por cada registro del ZKT
                    self.env['hr.asistencia.employee'].sudo().create(values)


        return True

        # Obtnemos el id de la cotización a usar

hr_asistencia_employee()

class lafox_corteparcial_venta(models.Model):
    _name = 'lafox.corteparcial.venta'
    _auto = False

    # FIELDS PARA MODEL lafox_cortez_ventas
    # code_venta = fields.Many2one('account.invoice',string='Venta')
    nomenclatura_venta = fields.Char(string='Folio Venta')
    cliente_venta = fields.Many2one('res.partner', string='Cliente')
    fecha_venta = fields.Datetime(string='Fecha Venta')
    responsable_venta = fields.Many2one('res.users', string='Responsable')
    total_venta = fields.Float(string='Total Venta')
    estatus_venta = fields.Selection(ACCOUNT_STATE, string='Estatus')

    _order = 'fecha_venta desc'

    # FUNCIÓN QUE PERMITE OBTENER TODAS LAS VENTAS DEL DIA
    def init(self, cr):
        fecha_inicio = date.today()
        fecha_fin = date.today() + timedelta(days=1)
        today=datetime.now()
        dateMonthStart="%s-%s-01" % (today.year, today.month)
        dateMonthEnd="%s-%s-%s" % (today.year, today.month, calendar.monthrange(today.year-1, today.month)[1])

        tools.drop_view_if_exists(cr, 'lafox_corteparcial_venta')
        cr.execute("""
            create or replace view lafox_corteparcial_venta as (
                select
                    min(id) as id,
                    nomenclatura as nomenclatura_venta,
                    partner_id as cliente_venta,
                    fecha_venta as fecha_venta,
                    user_id as responsable_venta,
                    amount_total as total_venta,
                    state as estatus_venta
                from
                    account_invoice
                WHERE
                fecha_venta >= current_date  and fecha_venta <current_date +1
                GROUP BY
                    nomenclatura,fecha_venta,user_id,partner_id,amount_total,state

            )
        """)

lafox_corteparcial_venta()

    # fecha_inicial = fields.Datetime(string='Fecha Inicio')
    # fecha_final = fields.Datetime(string='Fecha fin')
    # tipo_venta = fields.Selection(LAFOX_SELECT_CRUDO_TERMINADO, string='Vendedor de:')

    # venta_total = fields.Float(string='Corte al día')

    # corteventas_ids = fields.Many2one('lafox.cortez.ventas',string='IDS Corte Z')
    # corteventas_id = fields.One2many('lafox.cortez.ventas','corteventas_ids',string='ID Corte Z')

class lafox_clientes_vendedor(models.Model):
    _name='lafox.clientes.vendedor'

    nombres=fields.Char(string='Nombre(s)',require=True)
    apellidos=fields.Char(string='Apellido(s)',require=True)
    movil=fields.Char(string='Movil',require=True,size=10)
    telefono=fields.Char(string='Telefono',size=10)
    area=fields.Char(string='Area/Zona',require=True)
    descripcion=fields.Text(string='Descrip./Obs.',size=50)

lafox_clientes_vendedor()

class lafox_change_monetary(models.Model):
    _name='lafox.change.monetary'

    # Compute para sacar el tipo de moneda en pesos siempre
    @api.model
    def _default_curreny(self):
        currency_id = self.env['res.currency'].search([('name', '=', "MXN")])
        return currency_id[0]

    # Compute para sacar el costo la fecha anteriror
    @api.model
    def _default_date_before(self):
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices_id:
            fecha = prices_id.fecha_cambio
            return fecha

    # Compute para sacar el costo del dolar anteriror
    @api.model
    def _default_price_before(self):
        price = 0.0
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        if prices_id:
            price = prices_id.price_dolar
        return price

    @api.model
    def _default_percent_before(self):
        porcentaje=0.0
        porcentaje_id=self.env['lafox.change.monetary'].search([('id','=',1)])
        if porcentaje_id:
            porcentaje=porcentaje_id.porcentaje_cambio
        else:
            porcentaje = False
        return porcentaje

    #Campos  lafox_change_monetary
    price_dolar = fields.Float(string='Pesos',require=True)
    porcentaje_cambio=fields.Float(string='Porcentaje de descuento nuevo',require=True)
    #----------------------------------------------------------------------------------
    porcentaje_cambio_before=fields.Float(string='Porcentaje anterior', default=_default_percent_before)
    #-------------------------------------------------------------------------------------------------------
    price_before = fields.Float(string='Costo anterior', default=_default_price_before)
    currency_id = fields.Many2one('res.currency',string='Tipo de moneda', default=_default_curreny)
    fecha_cambio = fields.Datetime(string='Fecha y Hora del último cambio', default=_default_date_before)

    # Funcion que permite sobreescribir el mismo regitro y elimina los registros basura
    @api.multi
    def button_change_money(self):
        # Se busca el primer registro y se asigna el valor del dolar
        prices_id = self.env['lafox.change.monetary'].search([('id', '=', 1)])
        fecha = fields.datetime.now()
        prices_id.write({'price_dolar':self.price_dolar,'fecha_cambio':fecha,'porcentaje_cambio':self.porcentaje_cambio})
        self.fecha_cambio = fields.datetime.now()
        # Los registros sobrantes existentes son eliminados
        for price_delete in self.env['lafox.change.monetary'].search([('id', '>', 1)]):
            self.env['lafox.change.monetary'].search([('id','=', price_delete.id)]).unlink()

lafox_change_monetary()



class lafox_realizar_pago(models.Model):
    _name='lafox.realizar.pago'

    # Función que nos permite obtner el monto de venta
    @api.multi
    @api.depends('monto_cambio')
    def _compute_monto_total(self):
        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        self.monto_total =  class_obj.amount_total

    # Funcion para obtener el total de cambio a devolver
    @api.multi
    def _on_change_monto_cambio(self,monto_total,monto_pagado):
        dic = {}
        cambio = monto_pagado - monto_total
        dic['value']={
            'monto_cambio': cambio
            }
        return dic

    # Funcioón para cambiar el status para realizar el pago
    @api.multi
    def action_paid_venta_money(self):
        class_obj = self.env['account.invoice'].browse(self._context.get('active_id'))
        cambio = (self.monto_pagado - self.monto_total)
        if cambio < 0 or self.monto_pagado == 0:
            raise osv.except_osv(('No es posible realizar el pago'), ('La cantidad Pagada es menor al monto Total'))
        else:
            class_obj.sudo().write({'state':'paid'})

    # Compute para sacar el tipo de moneda en pesos siempre
    @api.model
    def _default_curreny(self):
        currency_id = self.env['res.currency'].search([('name', '=', "MXN")])
        return currency_id[0]

    # Campos para la_fox_realizar_pago
    monto_total = fields.Float(string='Monto Total', compute='_compute_monto_total')
    monto_pagado = fields.Float(string='Cantidad Pagada')
    monto_cambio = fields.Float(string='Cambio')
    currency_id = fields.Many2one('res.currency',string='Tipo de moneda', default=_default_curreny)

lafox_realizar_pago()

#Inicia la clase para generar el reporte de ventas dependiendo de las fechas y el cliente...
class lafox_reporte_de_venta(models.Model):
    _name='lafox.reporte.de.venta'

    registro_One2many=fields.One2many('lafox.reporte.de.venta','registro_Many2one',string='Registros')
    registro_Many2one=fields.Many2one('lafox.reporte.de.venta',string='Registros')

    fecha_inicio=fields.Date(string='Fecha de inicio',require=True)
    fecha_final=fields.Date(string='Fecha de fin',require=True)
    seleccion_cliente=fields.Many2one('res.partner',string='Selecciona al cliente')
    seleccion_producto=fields.Many2one('product.product',string='Selecciona el producto')

    nomenclatura_venta_rv=fields.Char(string='Folio Venta')
    cliente_venta_rv=fields.Many2one('res.partner', string='Cliente')
    fecha_venta_rv=fields.Datetime(string='Fecha Venta')
    estatus_venta_rv=fields.Selection(ACCOUNT_STATE, string='Estatus')
    prod_name_rv=fields.Char(string='Producto')
    total_venta_rv=fields.Float(string='Total')

    @api.multi
    def _llenado_reporte_venta(self,fecha_inicio,fecha_final,seleccion_cliente,seleccion_producto):
        lines=[]
        dicct={}
        if fecha_inicio!='False' and fecha_final!='False' and seleccion_cliente==False and seleccion_producto==False:
            for date_range in self.env['account.invoice'].search([('fecha_venta','>=',fecha_inicio),('fecha_venta','<=',fecha_final)]):
                for search_by_product in self.env['account.invoice.line'].search([('invoice_id','=',date_range.id)]):
                    dic_line = {}
                    dic_line['nomenclatura_venta_rv'] = date_range.nomenclatura
                    dic_line['cliente_venta_rv'] = date_range.partner_id
                    dic_line['fecha_venta_rv'] = date_range.fecha_venta
                    dic_line['estatus_venta_rv'] = date_range.state
                    dic_line['prod_name_rv']=search_by_product.name
                    dic_line['total_venta_rv'] = date_range.amount_total
                    lines.append(dic_line)
        elif fecha_inicio!='False' and fecha_final!='False' and seleccion_cliente!=False and seleccion_producto==False:
            for date_range in self.env['account.invoice'].search([('fecha_venta','>=',fecha_inicio),('fecha_venta','<=',fecha_final),('partner_id','=',seleccion_cliente)]):
                for search_by_product in self.env['account.invoice.line'].search([('invoice_id','=',date_range.id)]):
                    dic_line = {}
                    dic_line['nomenclatura_venta_rv'] = date_range.nomenclatura
                    dic_line['cliente_venta_rv'] = date_range.partner_id
                    dic_line['fecha_venta_rv'] = date_range.fecha_venta
                    dic_line['estatus_venta_rv'] = date_range.state
                    dic_line['prod_name_rv']=search_by_product.name
                    dic_line['total_venta_rv'] = date_range.amount_total
                    lines.append(dic_line)
        elif fecha_inicio!='False' and fecha_final!='False' and seleccion_cliente!=False and seleccion_producto!=False:
            for date_range in self.env['account.invoice'].search([('fecha_venta','>=',fecha_inicio),('fecha_venta','<=',fecha_final),('partner_id','=',seleccion_cliente)]):
                for search_by_product in self.env['account.invoice.line'].search([('product_id','=',seleccion_producto),('invoice_id','=',date_range.id)]):
                    dic_line = {}
                    dic_line['nomenclatura_venta_rv'] = date_range.nomenclatura
                    dic_line['cliente_venta_rv'] = date_range.partner_id
                    dic_line['fecha_venta_rv'] = date_range.fecha_venta
                    dic_line['estatus_venta_rv'] = date_range.state
                    dic_line['prod_name_rv']=search_by_product.name
                    dic_line['total_venta_rv'] = date_range.amount_total
                    lines.append(dic_line)
        elif fecha_inicio!='False' and fecha_final!='False' and seleccion_cliente==False and seleccion_producto!=False:
            for date_range in self.env['account.invoice'].search([('fecha_venta','>=',fecha_inicio),('fecha_venta','<=',fecha_final)]):
                for search_by_product in self.env['account.invoice.line'].search([('product_id','=',seleccion_producto),('invoice_id','=',date_range.id)]):
                    dic_line = {}
                    dic_line['nomenclatura_venta_rv'] = date_range.nomenclatura
                    dic_line['cliente_venta_rv'] = date_range.partner_id
                    dic_line['fecha_venta_rv'] = date_range.fecha_venta
                    dic_line['estatus_venta_rv'] = date_range.state
                    dic_line['prod_name_rv']=search_by_product.name
                    dic_line['total_venta_rv'] = date_range.amount_total
                    lines.append(dic_line)
        dicct['value']={'registro_One2many':lines}
        return dicct
#FInaliza la clase de lafox_reporte_de_venta

class lafox_corte_z(models.Model):
     _name='lafox.corte.z'
     registros_z_O=fields.One2many('lafox.corte.z','registros_z_M',string='Ventas')
     registros_z_M=fields.Many2one('lafox.corte.z',string='Registros')
     fecha_corte_z=fields.Datetime(string='Fecha de CORTE Z',readonly=True,default=datetime.now())
     total_corte_z=fields.Float(string='TOTAL del CORTE',readonly=True,index=True,compute='_compute_get_total',store=True)
     nomenclatura_venta_z=fields.Char(string='Folio Venta')
     cliente_venta_z=fields.Many2one('res.partner', string='Cliente')
     fecha_venta_z=fields.Datetime(string='Fecha Venta')
     responsable_venta_z=fields.Many2one('res.users', string='Responsable')
     total_venta_z=fields.Float(string='Total Venta')
     estatus_venta_z=fields.Selection(ACCOUNT_STATE, string='Estatus')

     @api.onchange('fecha_corte_z')
     def _llenado_corte_Z(self):
         today_today=date.today()
         today_tomorrow=today_today+timedelta(days=1)
         lines=[]
         for fill_args in self.env['account.invoice'].search([('fecha_venta','>=',str(today_today)),('fecha_venta','<',str(today_tomorrow)),('state','=','paid')]):
             dic_line = {}
             dic_line['nomenclatura_venta_z'] = fill_args.nomenclatura
             dic_line['cliente_venta_z'] = fill_args.partner_id
             dic_line['fecha_venta_z'] = fill_args.fecha_venta
             dic_line['responsable_venta_z'] = fill_args.user_id
             dic_line['total_venta_z'] =fill_args.amount_total
             dic_line['estatus_venta_z'] =fill_args.state
             lines.append(dic_line)
         self.registros_z_O=lines

     @api.multi
     def button_corte_z(self):
         today_today=date.today()
         today_tomorrow=today_today+timedelta(days=1)

         for ventas_pagadas in self.env['account.invoice'].search([('fecha_venta','>=',str(today_today)),('fecha_venta','<',str(today_tomorrow))]):
             if ventas_pagadas.state=='paid':
                 print 'Puedes realizar el CORTE Z'
                 estatus_venta_z_boton=self.env['lafox.valida.estatus.boton'].search([])
                 print estatus_venta_z_boton
                 estatus_venta_z_boton[0].sudo().write({'estatus':True})
                 #Si estan las ordenes 'paid' el estatus se le cambia la bandera a True mientras tanto estara en False cuando te permita generar ventas
             else:
                 raise osv.except_osv(('No es posible realizar el CORTE-Z'), ('Aún hay facturas con estado BORRADOR-draft y ABIERTAS-open, necesitan estar en PAGADAS-paid'))

     @api.one
     @api.depends('fecha_corte_z')
     def _compute_get_total(self):

         today_today=date.today()
         today_tomorrow=today_today+timedelta(days=1)

         for search_today_sold in self.env['account.invoice'].search([('fecha_venta','>=',str(today_today)),('fecha_venta','<',str(today_tomorrow)),('state','=','paid')]): #debe ser paid
             datos=0
             datos=float(datos)+search_today_sold.amount_total
             self.total_corte_z=datos
lafox_corte_z()

class lafox_valida_estatus_boton(models.Model):
    _name='lafox.valida.estatus.boton'

    estatus=fields.Boolean(string='Estatus',default=True)
    fecha=fields.Date(string='Fecha')

    @api.model
    def _can_view_corte_z(self):
        estado=self.search([])
        fecha_ahora=date.today()
        estado[0].sudo().write({'estatus':False,'fecha':fecha_ahora})

lafox_valida_estatus_boton()

class lafox_escala_de_descuentos(models.Model):
    _name='lafox.escala.de.descuentos'

    escala=fields.Char(string='Escala')
    descuentos=fields.Char(string='Descuento')
    factor=fields.Float(string='Factor')

lafox_escala_de_descuentos()
