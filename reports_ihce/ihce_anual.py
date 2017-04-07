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
#    Coded by: Karen Morales (karen.morales@grupoaltegra.com)
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
#############################################################################

from openerp.osv import osv, fields
import xlwt
import base64
from StringIO import StringIO
import psycopg2
import psycopg2.extras
from openerp.tools.translate import _
import time
from datetime import date
import locale
from PIL import Image
import os
import xmlrpclib
import io, StringIO
from PIL import Image

class reports_ihce(osv.osv_memory):
    _name = "reports.ihce_anual"
    

    _columns = {
        'name':fields.text('Instrucciones'),
        'date': fields.date('Fecha de reporte'),
        'date_ini': fields.date('Fecha Inicio'),
        'date_fin': fields.date('Fecha Final'),
        'xls_file_name':fields.char('xls file name', size=128),
        'xls_file':fields.binary('Archivo', readonly=True),
        'user_id': fields.many2one('res.users',"Responsable"),
    }

    _defaults = {
        'name': "Se creara un archivo .xls con el reporte seleccionado.",
        'date': lambda *a: time.strftime('%Y-%m-%d'),
        'user_id': lambda obj, cr, uid, context: uid,
    }

    #~ Función que crea la hoja de calculo para el informe mensual
    def action_create_report(self, cr, uid, ids, context=None):
        data = self.browse(cr, uid, ids[0], context=context)
        # Creamos la hoja de calculo
        workbook = xlwt.Workbook(encoding='utf-8')
        sheet_principal = workbook.add_sheet('Informe IHCE_ANUAL', cell_overwrite_ok=True)

        # Creamos la Hoja principal
        self.create_principal_sheet(cr, uid, sheet_principal, data, context)
        # Creamos el nombre del archivo
        name = "Informe IHCE_ANUAL.xls"
        # Creamos la ruta con el nombre del archivo donde se guardara
        root = "/tmp/" + str(name)
        # Guardamos la hoja de calculo en la ruta antes creada
        workbook.save(root)
        sprint_file = base64.b64encode(open("/tmp/%s" % (name), 'rb').read())
        # Creamos el Archivo adjunto al sprint
        data_attach = {
            'name': name,
            'datas': sprint_file,
            'datas_fname': name,
            'description': 'Informe Anual IHCE',
            'res_model': 'reports.ihce_anual',
            'res_id': ids[0],
        }
        self.pool.get('ir.attachment').create(cr, uid, data_attach, context=context)
        
        # Se guarda el archivo para poder descargarlo
        self.write(cr, uid, ids, {'xls_file': sprint_file, 'xls_file_name':name})
        
        return True
    
    #~ Función que llena la hoja con los datos correspondientes para el informe mensual
    def create_principal_sheet(self, cr, uid, sheet, data, context={}):
        #ESTILOS
        styleT = xlwt.easyxf(('font: height 260, bold 1, color black; alignment: horizontal center;'))
        styleTa = xlwt.easyxf(('font: height 200, color black; alignment: horizontal center;'))
        styleTT = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center;'))
        styleGA = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour blue_gray;'))
        styleG = xlwt.easyxf(('font: height 220, bold 1, color black; alignment: horizontal center; pattern: pattern solid, fore_colour yellow;'))
        styleV = xlwt.easyxf(('font: height 220, bold 1, color white; alignment: horizontal center; pattern: pattern solid, fore_colour green;'))
        style_n = xlwt.easyxf(('font: height 160, color black; alignment: horizontal left'))
        style_B = xlwt.easyxf(('font: height 190, bold 1, color black; alignment: horizontal left'))
        #CABECERA
        #~ locale.setlocale(locale.LC_ALL, "es_ES")
        sheet.write_merge(0, 0, 0, 11,("INSTITUTO HIDALGUENSE DE COMPETITIVIDAD EMPRESARIAL"), styleT)
        sheet.write_merge(2, 2, 0, 11,(time.strftime('%d de %B del %Y' , time.strptime(data.date, '%Y-%m-%d'))), styleT)
        sheet.write_merge(4, 4, 0, 11,("Resumen anteproyecto del programa operativo anual " + time.strftime('%d-%m-%Y', time.strptime(data.date_ini, '%Y-%m-%d')) + " al " + time.strftime('%d-%m-%Y', time.strptime(data.date_fin, '%Y-%m-%d'))), styleT)
       
       
        #~ EMPRENDIMIENTO
        sheet.write_merge(6, 6, 2, 9,("Instituto Hidalguense de Competitividad Empresarial "), styleGA)
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(7, 7, 2, 9,("Emprendimiento"), styleG)
        sheet.write_merge(8, 8, 2, 8,  "Emprendedores de Alto Impacto", style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(9, 9, 2, 8,  "Platicas/Cursos/Talleres, etc Emprendimiento", style_n)
        courses_empre_ids = self.pool.get('date.courses').search(cr, uid, [('dependence','=','ihce'),('services','=','emprendimiento'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin), ('type','!=','consultoria')], context=None)
        sheet.write(9, 9, len(courses_empre_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(10, 10, 2, 8,  "Asistentes", style_n)
        asis_empre = 0
        for row_asi in self.pool.get('date.courses').browse(cr, uid, courses_empre_ids, context=None):
            asis_empre += row_asi.number_attendees
        sheet.write(10, 9, asis_empre, style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(11,11, 2, 8,  "Asesoría a emprendedores", style_n)
        asesorias_empre_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','emprendimiento')], order='date ASC')
        sheet.write(11, 9, len(asesorias_empre_ids), style_n)
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DESARROLLO EMPRESARIAL~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(13, 13, 2, 9,("Servicios Empresariales"), styleG)
        sheet.write_merge(14, 14, 2, 9,("Asesorías"), styleV)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(15, 15, 2, 8,  "Registro de marca", style_n)
        register_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','marca')], order='date ASC')
        sheet.write(15, 9, len(register_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(16, 16, 2, 8,  "Patente", style_n)
        patent_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce'),('name','=','patente')], order='date ASC')
        sheet.write(16, 9, len(patent_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(17,17, 2, 8,  "Código de Barras", style_n)
        bar_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','codigo'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(17, 9, len(bar_ids), style_n)
        
         #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(18,18, 2, 8,  "Adecuación de Procesos", style_n)
        adec_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','adecuacion'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(18, 9, len(adec_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(19,19, 2, 8,  "Normatividad Nacional", style_n)
        norm_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','normatividad'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(19, 9, len(norm_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(20, 20, 2, 8,  "Pruebas de laboratorio/Tabla nutrimental", style_n)
        fda_ids = self.pool.get('asesorias.ihce').search(cr, uid, [('name','=','tabla'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(20, 9, len(fda_ids), style_n)
       
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ 
        sheet.write_merge(21, 21, 2, 8,  "Total", style_B)
        total = len(register_ids) + len(patent_ids) + len(bar_ids) + len(adec_ids) + len(norm_ids) + len(fda_ids)
        sheet.write(21, 9, total, style_B)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(22, 22, 2, 9,("Servicios"), styleV)
        
        sheet.write_merge(23, 23, 2, 8,  "Registro de marca", style_n)
        register_ids = self.pool.get('register.trademark').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(23, 9, len(register_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(24, 24, 2, 8,  "Patente", style_n)
        patent_ids = self.pool.get('patent.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write(24, 9, len(patent_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(25, 25, 2, 8,  "Membresías Código de Barras", style_n)
        bar_ids = self.pool.get('bar.code').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin),('option','=','ihce')], order='date ASC')
        sheet.write(25, 9, len(bar_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(26, 26, 2, 8,  "Pruebas de laboratorio/Tabla nutrimental", style_n)
        fda_ids = self.pool.get('fda.ihce').search(cr, uid, [('servicio','=','True'),('date','>=',data.date_ini),('date','<=',data.date_fin)], order='date ASC')
        sheet.write(26, 9, len(fda_ids), style_n)
        
        #~ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(27, 27, 2, 8,  "Total", style_B)
        total = len(register_ids) + len(patent_ids) + len(bar_ids) + len(fda_ids)
        sheet.write(27, 9, total, style_B)
        
        
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~FORMACION DE CAPITAL HUMANO~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        sheet.write_merge(29, 29, 2, 9,("Formación de Capital Humano"), styleG)
        sheet.write_merge(30, 30, 2, 8, "Empresas que recibieron consultoría individual para resolver problemas empresariales específicos", style_n)
        sheet.write_merge(31, 31, 2, 8,  "Horas", style_n)
        sheet.write_merge(32, 32, 2, 8 , "Cursos, talleres, diplomados, platicas, etc.", style_n)
        sheet.write_merge(33, 33, 2, 8,  "Horas", style_n)
        sheet.write_merge(34, 34, 2, 8, "Asistentes", style_n)
        
        horas = 0
        horas_con = 0
        asistentes = 0
        company_ids = []
        ban = False
        
        #~ Consultoria, horas y empresas
        consultoria_ids = self.pool.get('date.courses').search(cr, uid, [('type','=','consultoria'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        for row in self.pool.get('date.courses').browse(cr, uid, consultoria_ids, context=None):
            horas_con += row.hours_training
            invitados_ids = self.pool.get('company.invited').search(cr, uid, [('course_id','=', row.id)], context=None)
            for line in self.pool.get('company.invited').browse(cr, uid, invitados_ids, context=None):
                ban = False
                for li in company_ids:
                    if li == line.company_id.id:
                        ban = True
                        break 
                if not ban:
                    company_ids.append(line.company_id.id)
        
        sheet.write(30, 9, len(company_ids), style_n)
        sheet.write(31, 9, horas_con, style_n)
        
        #~ Cursos, talleres, etc
        courses_ids = self.pool.get('date.courses').search(cr, uid, [('type','!=','consultoria'),('services','=','formacion'),('dependence','=','ihce'),('state','=','done'),('date','>=',data.date_ini),('date','<=',data.date_fin)], context=None)
        
        sheet.write(32, 9, len(courses_ids), style_n)
        
        for row in self.pool.get('date.courses').browse(cr, uid, courses_ids, context=None):
            horas += row.hours_training
            asistentes += row.number_attendees
        
        sheet.write(33, 9, horas, style_n)
        sheet.write(34, 9, asistentes, style_n)
        
        
    
        #~ A prtir de aqui se agregan las notas del crm que son marcadas como importantes y las fotografias que se hayan adjuntado al proyecto de crm
        #actividades = self.pool.get('crm.project.ihce').search(cr, uid, [('date','>=',data.date_ini),('date','<=',data.date_fin),('priority','=','1'),('option','=','ihce'),('area','!=',10),('state','=','d-done')], context=None)
        
        #if actividades:
        #    sheet.write_merge(38, 38, 1, 10, "ACTIVIDADES RELEVANTES", styleTT)
            
        #    con = 1
        #    col = 40
        #    style_na = xlwt.easyxf(('font: height 175, color black; alignment: horizontal left'))

         #   for row in self.pool.get('crm.project.ihce').browse(cr, uid, actividades, context=None):
         #       if not row.notes:
         #           sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + str(row.name.encode('utf-8')) + "    " + str(row.date), style_na)
          #      else:
           #         sheet.write_merge(col, (col + 2), 1, 10, str(con) + ".- " + str(row.name.encode('utf-8')) + "    " + str(row.date) + "   " + str(row.notes.encode('utf-8')), style_na)
            #    col = col + 4
             #   j = 1
                
              #  fotos_ids = self.pool.get('ir.attachment').search(cr, uid, [('res_model','=','crm.project.ihce'),('res_id','=',row.id)], context=None)
               # ro = 1
                #for line in self.pool.get('ir.attachment').browse(cr, uid, fotos_ids):
                 #   name = line.name.split('.')
                    #~ Convertimos y guardamos la imagen en formato bmp
                    #try:
                       # img = Image.open("/var/www/img/%s" % (line.name)).convert("RGB").save("/var/www/img/"+str(name[0])+".bmp")
                        #~ Se muestra la imagen
                       # if j == 3:
                      #      ro = 1
                     #       j = 1
                    #        col = col + 16
                   #     sheet.insert_bitmap("/var/www/img/"+str(name[0])+".bmp", col, ro)
                  #      ro = ro + 4
                 #       j = j + 1
                #    except:
                #        print ""
            
               # col = col + 16
               # con = con + 1
        
        return sheet
    
    #~ Función para obtener el nombre del mes
    def meses(self, cr, uid, val, context=None):
        mes = ""
        if val == '01':
            mes = "ENERO"
        elif val == '02':
            mes = "FEBRERO"
        elif val == '03':
            mes = "MARZO"
        elif val == '04':
            mes = "ABRIL"
        elif val == '05':
            mes = "MAYO"
        elif val == '06':
            mes = "JUNIO"
        elif val == '07':
            mes = "JULIO"
        elif val == '08':
            mes = "AGOSTO"
        elif val == '09':
            mes = "SEPTIEMBRE"
        elif val == '10':
            mes = "OCTUBRE"
        elif val == '11':
            mes = "NOVIEMBRE"
        elif val == '12':
            mes = "DICIEMBRE"
        
        return mes

