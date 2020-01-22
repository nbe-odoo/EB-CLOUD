# -*- coding: utf-8 -*-
{
    'name': "Estella : Sales Team from Customer",

    'summary': """
        Sales Team/Person from the customer form
    """,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customization',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'crm', 'sales_team'],

    # always loaded
    'data': [
        'views/res_partner.xml',
        'views/account_invoice.xml'
    ],

}