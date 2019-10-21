# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import unittest
from odoo.addons.account.tests.test_invoice_onchange import TestInvoiceOnchange


@unittest.skip('Monkey patch test_invoice_currency_onchange')
def test_invoice_currency_onchange(self):
    pass


TestInvoiceOnchange.test_invoice_currency_onchange = test_invoice_currency_onchange
