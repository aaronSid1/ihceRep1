from openerp.osv import fields, osv
from openerp import models, fields, api, exceptions, tools, SUPERUSER_ID 
from openerp.tools.translate import _
from openerp import http
from datetime import datetime

#import pdb
#pdb.set_trace()


class Register(http.Controller):

    @http.route('/user/', auth='public', website=True, methods=['GET'])
    def index(self, **kw):
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        
        i = []
        for x in atentionareas:
            i.append(x.name)

        return http.request.render('company_ihce.form', {            
            'types': ['Emprendedor','Persona fisica','Persona moral'],
            'areas': i,
        })

    @http.route('/user/', auth='public', website=True, methods=['POST'])
    def reg(self, **kw):
        print "INSIDE" + str(http.request.params)
        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']
        
        #------------------------------Aqui va el listado de areas de atencion-------------#
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        i = []
        for x in atentionareas:
            i.append(x.name)
        #------------------------------Consulta si el user_login existe-------------# 
        responseL = http.request.params
        responsel = str(responseL['user_login'])
        usuarioActivo = Companies.search([('user_login','=',responsel)])

        
        var = len(usuarioActivo)
        if var == 0 :
            com = Companies.create(http.request.params)
            com.write({'company': True, 'diagnostico': True, 'state': 'draft', 'date': datetime.now()})
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Gracias por registrarte.',
            'areas': i
            })
            
        else :
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Usuario ya Registrado',
            'areas': i
            })

    @app.route('/stanford')
        def stanford_page():
            return """<h1>Hello stanford!</h1>"""
            
    
