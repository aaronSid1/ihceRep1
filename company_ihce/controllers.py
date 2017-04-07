from openerp.osv import fields, osv
from openerp import models, fields, api, exceptions, tools, SUPERUSER_ID 
from openerp.tools.translate import _
from openerp import http
from datetime import datetime
import locale
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf-8')
#pdb.set_trace()

class Register(http.Controller):

    @http.route('/signup/', auth='public', website=True, methods=['GET'])
    def index(self, **kw):
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        
        i = []
        for x in atentionareas:
            i.append(x.name)
 
        emprered = http.request.env['emprereds']
        emprereD = emprered.search([('name','!=','')])

        ie = []
        for x in emprereD:
            ie.append(x.name)

        return http.request.render('company_ihce.form', {            
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'areas': i,
            'empr': ie,
        })

    @http.route('/signup/', auth='public', website=True, methods=['POST'])
    def reg(self, **kw):
        print "INSIDE" + str(http.request.params)
        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']
        Res = http.request.env['res.users']
        emprered = http.request.env['emprereds']
        
        #------------------------------Aqui va el listado de areas de atencion-------------#
        Atentionareas = http.request.env['atention.area']
        atentionareas = Atentionareas.search([('name','!=','')])
        i = []
        for x in atentionareas:
            i.append(x.name)
        #------------------------------Consulta si el user_login existe-------------# 
        responseL = http.request.params
        responsel = str(responseL['user_l'])
        empreredname = str(responseL['empr'])

        usuarioActivo = Companies.search([('user_login','=',responsel)])
        emprereId = emprered.search([('name','=',empreredname)])


        iemp = []
        for x in emprereId:
            iemp.append(x.id) 


        nombre = str(responseL['name_people']) + " " + str(responseL['apaterno']) + " " + str(responseL['amaterno']) 



        emprereD = emprered.search([('name','!=','')])

        ie = []
        for x in emprereD:
            ie.append(x.name)


        types = str(responseL['types'])

      
        if types == "Emprendedor":
            types = "emprendedor"
        if types == "Persona Fisica":
            types = "fisica"
        if types == "Persona Moral":
            types = "moral"


        var = len(usuarioActivo)
        if var == 0 :
            #pdb.set_trace()
            http.request.params.update({'name_commercial':nombre, 'company': True, 'diagnostico': True,'state': 'draft','date': datetime.now(),'name': nombre,'emprered': iemp[0], 'user_login':responsel, 'atention_area':Atentionareas, 'type':types})
            com = Companies.create2(http.request.params)
            #com.write({})
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Gracias por registrarte.',
            'areas': i,
            'empr': ie,
            })
            
        else :
            return http.request.render('company_ihce.form', {
            'types': ['Emprendedor','Persona Fisica','Persona Moral'],
            'message': 'Usuario ya Registrado',
            'areas': i,
            'empr': ie,
            })


            
class seguimiento(http.Controller):

    @http.route('/seguimiento/signup/', auth='public', website=True, methods=['GET'])
    def index(self, **kw):
        return http.request.render('company_ihce.forms_user', {            
            
        })

    @http.route('/seguimiento/signup/', auth='public', website=True, methods=['POST'])
    def a_log(self, **kw):
        print "INSIDE" + str(http.request.params)
        Companies = http.request.env['companies.ihce']
        Login = http.request.env['login.ihce']

        responseL = http.request.params
        responsel = str(responseL['user_l'])
        responseP = str(responseL['password_login'])
        

        usuarioActivo = Companies.search([('user_login','=',responsel), ('password_login','=',responseP)])

        var = len(usuarioActivo)
        if var == 1 :
            return http.request.render('company_ihce.forms', {
            'message': 'Gracias puedes continuar para agendar una asesoria',
            'id': usuarioActivo.id,
            'name': usuarioActivo.name,
            })
            
        else :
            return http.request.render('company_ihce.forms_user', {
            'message': 'Usuario no registrado, registrate para crear una aseosria',
            })     

    @http.route('/seguimiento/asesoria/', auth='public', website=True, methods=['POST'])
    def reg_ase(self, **kw):
        Asesorias = http.request.env['asesorias.ihce']
        #http.request.params.update({'name_commercial':nombre, 'rfc':nombre})
        com = Asesorias.create2(http.request.params)


        return http.request.render('company_ihce.forms_user',{
            'message': 'Gracias, tu asesoria esta registrada',
            })



