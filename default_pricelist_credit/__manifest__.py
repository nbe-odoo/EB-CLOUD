# -*- coding: utf-8 -*-
{
    'name': "default_pricelist_credit",

    'summary': """
        Default pricelist on credit note""",

    'description': """
        Default pricelist on credit note
    """,

    'author': "SEA",
    'website': "https://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account.invoice.form.xml',
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}