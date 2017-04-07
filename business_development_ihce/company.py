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
from datetime import date

class companies_ihce(osv.Model):
    _inherit = 'companies.ihce'
    
    def _get_mark(self, cr, uid, ids, field, arg, context=None):
        res = {}
        mark = False

        for row in self.browse(cr, uid, ids, context=context):
            if len(row.mark_id) > 0:
                mark = True
                res[row.id] = True
            else:
                res[row.id] = False
        return res
    
    def _get_code(self, cr, uid, ids, field, arg, context=None):
        res = {}
        code = False

        for row in self.browse(cr, uid, ids, context=context):
            if len(row.code_id) > 0:
                code = True
                res[row.id] = True
            else:
                res[row.id] = False
        return res
    
    def _get_patent(self, cr, uid, ids, field, arg, context=None):
        res = {}
        paten = False

        for row in self.browse(cr, uid, ids, context=context):
            if len(row.patent_id) > 0:
                paten = True
                res[row.id] = True
            else:
                res[row.id] = False
        return res
    
    def _get_fda(self, cr, uid, ids, field, arg, context=None):
        res = {}
        fda = False
        
        for row in self.browse(cr, uid, ids, context=context):
            if len(row.fda_id) > 0:
                fda = True
                res[row.id] = True
            else:
                res[row.id] = False

        return res
        
    _columns = {
        'mark_id': fields.one2many('register.trademark', 'company_id',"Registro de Marca"),
        'code_id': fields.one2many('bar.code', 'company_id',"Código de Barras"),
        'patent_id': fields.one2many('patent.ihce', 'company_id',"Patente"),
        'fda_id': fields.one2many('fda.ihce', 'company_id',"FDA"),
        'mark_register': fields.function(_get_mark, type='boolean', string="Registro de marca"),
        'code_bar': fields.function(_get_code, type='boolean', string="Codigo de barras"),
        'patent': fields.function(_get_patent, type='boolean', string="Patente"),
        'fda': fields.function(_get_fda, type='boolean', string="FDA"),
    }
    
    _defaults = {
        'mark_register': False,
        'code_bar': False,
        'patent': False,
        'fda': False,
    }
    
   
