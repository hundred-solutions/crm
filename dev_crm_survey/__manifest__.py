# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'CRM Survey answer print | lead survey | Pipeline Survey',
    'version': '17.0',
    'sequence': 1,
    'category': 'Sales',
    'description':
        """
        This Module add below functionality into odoo

        1.CRM Survey\n
        
        Customer CRM Survey to print answer and sent survey to customer on lead and pipeline lead survey pipeline survey lead survey answear lead print survey

    """,
    'summary': 'Customer CRM Survey to print answer and sent survey to customer on lead and pipeline lead survey pipeline survey lead survey answear lead print survey',
    'depends': ['crm', 'survey', 'website'],
    'data': [
        'data/template_survey_start.xml',
        'security/ir.model.access.csv',
        'views/pipeline.xml',
        'views/crm_survey_template.xml',
        
        
    ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':15.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k'
    'pre_init_hook' :'pre_init_check',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: