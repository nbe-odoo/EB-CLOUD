# -*- coding: utf-8 -*-
{
    'name': "Estella - Success Pack - Delivery orders",

    'summary': """
        Option Allocate available stock for Delivery Orders""",

    'description': """
        Option Allocate available stock for Delivery Orders
    """,

    'author': "Odoo S.A.",
    'website': "http://www.odoo.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'product_availability',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_stock'],

    # always loaded
    'data': [
        'actions/stock_picking.xml'
    ],
}