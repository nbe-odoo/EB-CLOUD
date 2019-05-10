from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    untaxed_amount_reserved = fields.Float(compute='_compute_untaxed_reserved', string='Untaxed Amount Reserved', store=True)
    untaxed_amount_undelivered = fields.Float(compute='_compute_untaxed_undelivered', string='Untaxed Undelivered', store=True)
    quantity_reserved = fields.Float(compute='_compute_qty_reserved', string='Quantity Reserved', store=True)
    quantity_undelivered = fields.Float(compute='_compute_qty_undelivered', string='Quantity Undelivered', store=True)

    @api.multi
    @api.depends('move_ids', 'move_ids.state', 'price_unit', 'move_ids.reserved_availability')
    def _compute_untaxed_reserved(self):
        for so_line in self:
            for delivery in so_line.move_ids:
                if so_line.move_ids and delivery.state not in ['cancel', 'done']:
                    so_line.untaxed_amount_reserved = delivery.reserved_availability * so_line.price_unit
                elif so_line.move_ids and delivery.state in ['cancel', 'done']:
                    so_line.untaxed_amount_reserved = 0

    @api.multi
    @api.depends('move_ids', 'move_ids.state', 'price_unit', 'move_ids.product_uom_qty', 'move_ids.quantity_done')
    def _compute_untaxed_undelivered(self):
        for so_line in self:
            for delivery in so_line.move_ids:
                if so_line.move_ids and delivery.state not in ['cancel', 'done']:
                    so_line.untaxed_amount_undelivered = (delivery.product_uom_qty - delivery.quantity_done) * so_line.price_unit
                elif so_line.move_ids and delivery.state in ['cancel', 'done']:
                    so_line.untaxed_amount_undelivered = 0

    @api.multi
    @api.depends('move_ids', 'move_ids.state', 'move_ids.reserved_availability')
    def _compute_qty_reserved(self):
        for so_line in self:
            for delivery in so_line.move_ids:
                if so_line.move_ids and delivery.state not in ['cancel', 'done']:
                    so_line.quantity_reserved = delivery.reserved_availability
                elif so_line.move_ids and delivery.state in ['cancel', 'done']:
                    so_line.quantity_reserved = 0

    @api.multi
    @api.depends('move_ids', 'move_ids.state', 'move_ids.product_uom_qty', 'move_ids.quantity_done')
    def _compute_qty_undelivered(self):
        for so_line in self:
            for delivery in so_line.move_ids:
                if so_line.move_ids and delivery.state not in ['cancel', 'done']:
                    so_line.quantity_undelivered = delivery.product_uom_qty - delivery.quantity_done
                elif so_line.move_ids and delivery.state in ['cancel', 'done']:
                    so_line.quantity_undelivered = 0