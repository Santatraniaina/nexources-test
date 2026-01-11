{
    'name': "Nexources - Request",
    'summary': "Manage employees requests",
    'description': """
Long description of module's purpose
    """,
    'author': "Santatra RAKOTOARIMANANA",
    'website': "https://www.yourcompany.com",
    'category': 'Services',
    'version': '0.1',
    'depends': [
        'base',
        'hr',
    ],
    'data': [
        # security
        'security/request_security.xml',
        'security/ir.model.access.csv',
        # views
        'views/request_views.xml',
        'views/hr_employee_views.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
}

