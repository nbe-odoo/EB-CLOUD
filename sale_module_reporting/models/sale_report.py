from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleReport(models.Model):
    _inherit = 'sale.report'

    untaxed_amount_reserved4 = fields.Float(string='Untaxed Amount Reserved', readonly=True)
    untaxed_amount_undelivered4 = fields.Float(string='Untaxed Amount Undelivered', readonly=True)
    quantity_reserved4 = fields.Float(string='Quantity Reserved', readonly=True)
    quantity_undelivered4 = fields.Float(string='Quantity Undelivered', readonly=True)
    effective_date = fields.Date(string='Effective Date', readonly=True)
    commitment_date = fields.Date(string='Commitment Date', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['untaxed_amount_reserved4'] = ', sum(l.untaxed_amount_reserved4) as untaxed_amount_reserved4'
        fields['untaxed_amount_undelivered4'] = ', sum(l.untaxed_amount_undelivered4) as untaxed_amount_undelivered4'
        fields['quantity_reserved4'] = ', sum(l.quantity_reserved4) as quantity_reserved4'
        fields['quantity_undelivered4'] = ', sum(l.quantity_undelivered4) as quantity_undelivered4'
        fields['effective_date'] = ', s.effective_date'
        fields['commitment_date'] = ', s.commitment_date'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)