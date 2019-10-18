# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        res = super(AccountInvoice, self)._onchange_partner_id()
        
        self.pricelist_id = self.partner_id.property_product_pricelist.id
        self.currency_id = self.partner_id.property_product_pricelist.currency_id
        
        return res


class AccountInvoiceLIne(models.Model):
    _inherit = 'account.invoice.line'

    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        res = super(AccountInvoiceLIne, self)._onchange_uom_id()
        if self.product_id and self.invoice_id.pricelist_id:
            self.price_unit = self.invoice_id.pricelist_id.get_product_price(self.product_id, 1.0, self.invoice_id.partner_id)
        return res
