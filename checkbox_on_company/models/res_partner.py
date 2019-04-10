from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_limit = fields.Boolean(string="Active Outstanding Payment Limit", default=False)

