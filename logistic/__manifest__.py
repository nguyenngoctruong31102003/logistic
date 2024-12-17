# Part of Odoo. See LICENSE file for full copyright and licensing details.  
{
    'name': 'T4POST LOGISTIC',
    'version': '1.0',
    'sequence': 0,
    'category': 'Logistic',
    'summary': 'Tutorial addon for learning purposes',
    'description': """
        This is a tutorial addon that inherits res.partner model
        with completely new views and menu items.
    """,
    # 'contacts'
    'depends': ['base', 'web', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        
        'views/menu_item_customers.xml',
        'views/menu_item_products.xml',
        'views/menu_item_contacts.xml',
        'views/menu_items.xml',
    ],
    'installable': True,
    'application': True,
    
    'assets': {
         'web.assets_backend':
        [
            'logistic/static/src/js/*.js',
            'logistic/static/src/xml/*.xml',
        ]
    },
    'license': 'LGPL-3',
}
