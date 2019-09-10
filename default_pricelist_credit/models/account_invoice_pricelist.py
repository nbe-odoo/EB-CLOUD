# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    pricelist_id = fields.Many2one(
        'product.pricelist', 'Pricelist')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.pricelist_id = self.partner_id.property_product_pricelist.id
        self.currency_id = self.partner_id.property_product_pricelist.currency_id
