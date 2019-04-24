from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleReport(models.Model):
    _inherit = 'sale.report'

    untaxed_amount_reserved = fields.Float(string='Untaxed Amount Reserved', readonly=True)
    untaxed_amount_undelivered = fields.Float(string='Untaxed Amount Undelivered', readonly=True)
    quantity_reserved = fields.Float(string='Quantity Reserved', readonly=True)
    quantity_undelivered = fields.Float(string='Quantity Undelivered', readonly=True)
    effective_date = fields.Date(string='Effective Date', readonly=True)
    commitment_date = fields.Date(string='Commitment Date', readonly=True)

    def _query(self, with_clause='', fields={}, groupby='', from_clause=''):
        fields['untaxed_amount_reserved'] = ', l.untaxed_amount_reserved'
        fields['untaxed_amount_undelivered'] = ', l.untaxed_amount_undelivered'
        fields['quantity_reserved'] = ', l.quantity_reserved'
        fields['quantity_undelivered'] = ', l.quantity_undelivered'
        fields['effective_date'] = ', s.effective_date'
        fields['commitment_date'] = ', s.commitment_date'

        groupby += ', l.untaxed_amount_reserved, l.untaxed_amount_undelivered, l.quantity_reserved, l.quantity_undelivered, s.effective_date, s.commitment_date'

        return super(SaleReport, self)._query(with_clause, fields, groupby, from_clause)
