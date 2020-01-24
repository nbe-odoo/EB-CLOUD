# -*- coding: utf-8 -*-

from odoo import fields, api, models, _

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.onchange('partner_id', 'company_id')
    def _onchange_partner_id(self):
        if self.partner_id.team_id:
            self.team_id = self.partner_id.team_id
