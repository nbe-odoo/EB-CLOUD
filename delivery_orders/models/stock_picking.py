from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def allocate_stock(self):
        for rec in self:
            rec.action_assign()
