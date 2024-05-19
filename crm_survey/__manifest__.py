{
    'name': 'CRM Survey',
    'version': '17.0',
    'sequence': 1,
    'category': 'Sales',
    'description': 'This Module integrate Surveys with CRM',
    'depends': ['crm', 'survey', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/pipeline.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'author': 'Hundred Solutions Pvt.Ltd',
    'website': 'http://www.hundredsolutions.com',    
    'maintainer': 'Hundred Solutions Pvt.Ltd', 
    'support': 'support@hundredsolutions.com',
}