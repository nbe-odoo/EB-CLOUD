from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    untaxed_amount_reserved = fields.Float(compute='_compute_untaxed_reserved', string='Untaxed Amount Reserved', store=True)
    untaxed_amount_undelivered = fields.Float(compute='_compute_untaxed_undelivered', string='Untaxed Undelivered', store=True)
    quantity_reserved = fields.Float(compute='_compute_qty_reserved', string='Quantity Reserved', store=True)
    quantity_undelivered = fields.Float(compute='_compute_qty_undelivered', string='Quantity Undelivered', store=True)

    @api.depends('order_id.picking_ids.move_lines.reserved_availability')
    def _compute_untaxed_reserved(self):
        for rec in self:
            rec.untaxed_amount_reserved = 0
            for pick in rec.order_id.picking_ids:
                for move in pick.move_lines:
                    rec.untaxed_amount_reserved += move.reserved_availability * rec.price_unit

    @api.depends('order_id.picking_ids.move_lines.product_uom_qty', 'order_id.picking_ids.move_lines.quantity_done')
    def _compute_untaxed_undelivered(self):
        for rec in self:
            rec.untaxed_amount_undelivered = 0
            for pick in rec.order_id.picking_ids:
                for move in pick.move_lines:
                    rec.untaxed_amount_undelivered = (move.product_uom_qty - move.quantity_done) * rec.price_unit

    @api.depends('order_id.picking_ids.move_lines.reserved_availability')
    def _compute_qty_reserved(self):
        for rec in self:
            rec.quantity_reserved = 0
            for pick in rec.order_id.picking_ids:
                for move in pick.move_lines:
                    rec.quantity_reserved += move.reserved_availability

    @api.depends('order_id.picking_ids.move_lines.product_uom_qty', 'order_id.picking_ids.move_lines.quantity_done')
    def _compute_qty_undelivered(self):
        for rec in self:
            rec.quantity_undelivered = 0
            for pick in rec.order_id.picking_ids:
                for move in pick.move_lines:
                    rec.quantity_undelivered = move.product_uom_qty - move.quantity_done