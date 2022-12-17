# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'CRM',
    'version': '1.2',
    'category': 'Sales/CRM',
    'sequence': 15,
    'summary': 'Track leads and close opportunities',
    'description': "",
    'website': 'https://www.odoo.com/page/crm',
    'depends': [
        'base_setup',
    ],
    'data':[
        'security/ir.model.access.csv',
        'views/device_model_view.xml',
        'views/content_model_view.xml',
        'views/menu_views.xml',
        'cron.xml',
        'views/action.xml'
        ],
    'css': ['static/src/css/crm.css'],
    'installable': True,
    'application': True,
    'auto_install': False

}
