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
############################################################################ 

{
    "name": "Desarrollo Empresarial IHCE",
    "version": "1.0",
    "depends": ["base",'courses_ihce'],
    "author": "Grupo Altegra",
    "category": "Custom Modules",
    "description": "Área de desarrollo empresarial, registro de marca, código de barras, patentes y FDA",
    "data" :[
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/sequence.xml',
        'security/servicios_by_user.xml',
        'views/resgister_mark_view.xml',
        'views/time_ihce_view.xml',
        'views/catalog_business.xml',
        'views/bar_code_view.xml',
        'views/patents_view.xml',
        'views/fda_view.xml',
        'views/company_view.xml',
        "demo/time_demo.xml",
        ],
    "demo" : [
        #~ "demo/time_demo.xml",
    ],
    'test': [],
    'installable': True,
    'active': False,
    'certificate': False,
}
