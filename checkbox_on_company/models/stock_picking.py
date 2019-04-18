from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PaymentLimitWizard(models.TransientModel):
    _name = "payment.limit.wizard"
    message = fields.Char(readonly=True, default=_('The outstanding payments limit for the customer has been reached.'
                                                   '\n Are you sure you want to continue? '))

    stock_pick_id = fields.Many2one('stock.picking')

    def my_validate_method(self):
        print(self.stock_pick_id)
        return self.stock_pick_id.button_validate()


class StockPicking(models.Model):
    _inherit = 'stock.picking'


    @api.multi
    def button_validate_limit(self):

        if self.partner_id.has_limit == True:
            context = {
                'default_stock_pick_id': self.id,
            }
            return {
                'name': _('Payment Limit Warning'),
                'type': 'ir.actions.act_window',
                'res_model': 'payment.limit.wizard',
                'view_type': 'form',
                'view_mode': 'form',
                'context': context,
                'target': 'new',
            }
        else:
            return self.button_validate()