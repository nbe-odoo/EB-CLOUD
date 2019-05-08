# coding: utf-8
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import Warning

class StockMove(models.Model):

    _inherit = 'stock.move'

    new_reserved_availability = fields.Integer('New Reserved Qty')
    reset_reserve = fields.Boolean('Reset Reserved Qty')

    @api.multi
    def write(self, vals):
        self = self.with_context(mail_notrack=True)
        if vals.get('reset_reserve') or vals.get('new_reserved_availability'):
            initial_qty = {}
            if vals.get('reset_reserve'):
                new_reserved_availability = 0
                for rec in self:
                    initial_qty[rec.id] = rec.product_uom_qty
                vals['product_uom_qty'] = 0
                vals['reset_reserve'] = False
                res = super(StockMove, self).write(vals)
                self._action_assign()

            elif vals.get('new_reserved_availability'):
                new_reserved_availability = vals.get('new_reserved_availability')
                for rec in self:
                    initial_qty[rec.id] = rec.product_uom_qty
                    
                    if rec.product_id.type == 'product' and rec.availability < new_reserved_availability :
                        raise Warning('Cannot reserve %s of %s as there are only %s available' % (new_reserved_availability, rec.product_id.name, rec.availability))

                vals['product_uom_qty'] = new_reserved_availability
                vals['new_reserved_availability'] = 0
                res = super(StockMove, self).write(vals)
                self._action_assign()

            for rec in self:
                if initial_qty[rec.id] > new_reserved_availability:
                    rec.write({'product_uom_qty': initial_qty[rec.id]})
        else:
            res = super(StockMove, self).write(vals)

        return res       


class StockPicking(models.Model):

    _inherit = 'stock.picking'

    unreserve_backorder = fields.Boolean()

    @api.model
    def create(self, vals):
        if vals.get('backorder_id'):
            vals['unreserve_backorder'] = True
        return super(StockPicking, self).create(vals)

    @api.multi
    def write(self, vals):
        to_unreserve = self.env['stock.picking']
        for rec in self:
            if rec.move_line_ids and rec.state != 'done' and rec.unreserve_backorder:
                vals['unreserve_backorder'] = False
                to_unreserve |= rec

        res = super(StockPicking, self.with_context(mail_notrack=True)).write(vals)

        to_unreserve.do_unreserve()
        return res