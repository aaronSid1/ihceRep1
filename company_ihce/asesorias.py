#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################################################
#    Module Writen to OpenERP, Open Source Management Solution
#    CopyLeft 2012 - http://www.grupoaltegra.com
#    You are free to share, copy, distribute, transmit, adapt and use for commercial purpose
#    More information about license: http://www.gnu.org/licenses/agpl.html
#    info Grupo Altegra (openerp@grupoaltegra.com)
#
#############################################################################
#
#    Coded by: Karen Morales(karen.morales@grupoaltegra.com)
#
#############################################################################
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
############################################################################  

from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp import SUPERUSER_ID
from datetime import datetime, date, timedelta
import time
import pdb


class asesorias_ihce(osv.Model):
    _name = 'asesorias.ihce'
    
    _columns = {
        'name': fields.selection([('asesoria','Asesoría general en servicios ihce'),('marca','Registro de Marca'),('patente','Patente'),('codigo','Código de Barras'),('adecuacion','Adecuación de producto'),('normatividad','Normatividad Nacional'),('tabla','Tabla Nutrimental'),('imagen','Imagen Corporativa y Etiquetado'),('financiamiento','Financiamiento'),('emprendimiento','Emprendimiento'),('shcp','Registro ante la SHCP'),('capital','Formación de Capital Humano'),('aie','AIE'),('aceleracion','Aceleración Empresarial')], "Asesoría"),
        #'name': fields.selection([('asesoria','Asesoría general en servicios ihce'),('marca','Registro de Marca'),('patente','Patente'),('codigo','Código de Barras'),('adecuacion','Adecuación de producto'),('normatividad','Normatividad Nacional'),('tabla','Tabla Nutrimental'),('imagen','Imagen Corporativa y Etiquetado'),('financiamiento','Financiamiento'),('emprendimiento','Emprendimiento'),('shcp','Registro ante la SHCP'),('capital','Formación de Capital Humano'),('aie','AIE'),('manos','Manos a la Obra'),('aceleracion','Aceleración Empresarial')], "Asesoría"),
        #Cambio Realizado por Julio Cesar Lazcano Para que no se generen Asesorias por parte de Manos a la Obra
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'date': fields.date("Fecha"),
        'user_id': fields.many2one('res.users',"Responsable"),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina de Atención'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    def create(self, cr, uid, vals, context=None):
        fecha_actual = datetime.now()
        ase_id = super(asesorias_ihce, self).create(cr, uid, vals, context)
        row = self.browse(cr, uid, ase_id, context=context)
        #~ Agregamos actividad al historial de la empresa
        valor = self.nombres(cr, uid, [ase_id], row.name, context=context)
        
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El beneficiario ha recibido asesoría de ' + str(valor), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        return True



    def create2(self, cr, uid, vals, context=None):
        fecha_actual = datetime.now()
        valor = vals.get('asesoria')

        if valor == 'Registro de Marca':
            valor = "marca"
        if valor == 'Asesoría general en servicios ihce':
            valor = "asesoria"
        if valor == 'Patente':
            valor = "patente"
        if valor == 'Código de Barras':
            valor = "codigo"
        if valor == 'Adecuación de Producto':
            valor = "adecuacion"
        if valor == 'Normatividad Nacional':
            valor = "normatividad"
        if valor == 'Tabla Nutrimental':
            valor = "tabla"
        if valor == 'imagen':
            valor = "Imagen Corporativa y Etiquetado"
        if valor == 'financiamiento':
            valor = "Financiamiento"
        if valor == 'emprendimiento':
            valor = "Emprendimiento"
        if valor == 'shcp':
            valor = "Registro ante la SHCP"
        if valor == 'capital':
            valor = "Formación de Capital Humano"
        if valor == 'aie':
            valor = "AIE"
        if valor == 'manos':
            valor = "Manos a la Obra"
        if valor == 'aceleracion':
            valor = "Aceleración Empresarial"

        if uid == 3:
            uid = 72
            vals.update({'name':str(valor)})
        else: 
            vals.update({'name':str(valor)})

        pdb.set_trace()

        ase_id = super(asesorias_ihce, self).create(cr, uid, vals, context)
        row = self.browse(cr, uid, ase_id, context=context)
        #~ Agregamos actividad al historial de la empresa
        valor = self.nombres(cr, uid, [ase_id], row.name, context=context)
        
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El beneficiario ha recibido asesoría de ' + str(valor), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
        
        return True
        
    def nombres(self, cr, uid, ids, valor, context=None):
        if valor == 'marca':
            return "Registro de Marca"
        elif valor == 'asesoria':
            return "Asesoría general en servicios ihce"
        elif valor == 'patente':
            return "Patente"
        elif valor == 'codigo':
            return "Código de Barras"
        elif valor == 'adecuacion':
            return "Adecuación de Producto"
        elif valor == 'normatividad':
            return "Normatividad Nacional"
        elif valor == 'tabla':
            return "Tabla Nutrimental"
        elif valor == 'imagen':
            return "Imagen Corporativa y Etiquetado"
        elif valor == 'financiamiento':
            return "Financiamiento"
        elif valor == 'emprendimiento':
            return "Emprendimiento"
        elif valor == 'shcp':
            return "Registro ante la SHCP"
        elif valor == 'capital':
            return "Formación de Capital Humano"
        elif valor == 'aie':
            return "AIE"
        elif valor == 'manos':
            return "Manos a la Obra"
        else:
            if valor == 'aceleracion':
                return "Aceleración Empresarial"
        
        return ""
        
class servicios_ihce(osv.Model):
    _name = 'servicios.ihce'
    
    _columns = {
        #'name': fields.selection([('financiamiento','Financiamiento'),('manos','Manos a la Obra'),('adecuacion', 'Adecuación de producto')], "Servicio"),
        #Cambio Realizado por Julio Cesar Lazcano Para que no se generen Servicios por parte de Manos a la Obra
        'name': fields.selection([('financiamiento','Financiamiento'),('adecuacion', 'Adecuación de producto')], "Servicio"),
        'company_id': fields.many2one('companies.ihce', 'Beneficiario'),
        'date': fields.date("Fecha"),
        'user_id': fields.many2one('res.users',"Responsable"),
        'option': fields.selection([('ihce', 'IHCE'),('emprered', 'Emprered')], 'Oficina de atención'),
        'area': fields.many2one('responsible.area', "Departamento"),
        'emprered': fields.many2one('emprereds', 'Emprered'),
    }
    
    _defaults = {
        'user_id': lambda obj, cr, uid, context: uid,
        'option': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).option,
        'area': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).area.id,
        'emprered': lambda self, cr, uid, obj, ctx=None: self.pool['res.users'].browse(cr, uid, uid).emprered.id,
        'date': lambda *a: time.strftime('%Y-%m-%d'),
    }
    
    def create(self, cr, uid, vals, context=None):
        fecha_actual = datetime.now()
        servi_id = super(servicios_ihce, self).create(cr, uid, vals, context)
        row = self.browse(cr, uid, servi_id, context=context)
        
        #~ Agregamos actividad al historial de la empresa
        valor = self.nombres(cr, uid, [servi_id], row.name, context=context)
        
        self.pool.get('crm.ihce').create(cr, uid, {'company_id': row.company_id.id, 'date':fecha_actual, 'name':'El beneficiario ha recibido servicio de ' + str(valor), 'user':uid, 'date_compromise': fecha_actual, 'state':'done'}, context=context)
    
        return True
        
    def nombres(self, cr, uid, ids, valor, context=None):
        if valor == 'financiamiento':
            return "Financiamiento"
        else:
            if valor == 'manos':
                return "Manos a la Obra"
            else:
                if valor == 'adecuacion':
                    return "Adecuación de producto"
        
        return ""
