from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id', 'company_id')
    def onchange_partner(self):
        if self.partner_id.has_limit == True:
            message = _('The outstanding payments limit for %s has been reached.\n'
                        ' Are you sure you want to continue? ' %(self.partner_id.name))
            warning_mess = {
                'title': _('Warning message!'),
                'message': message
            }
            return {'warning': warning_mess}

