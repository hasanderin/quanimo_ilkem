# -*- coding: utf-8 -*-
# Copyright (C) 2023 Quanimo (https://www.quanimo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, api, models


class UpdateSalePriceWizard(models.TransientModel):
    _name = 'update.sale.price.wizard'

    disable_update_button = fields.Boolean(default=False)
    rate = fields.Float(string='Rate')
    update_line = fields.One2many('update.sale.price.wizard.line', 'parent_id')

    @api.onchange('rate')
    def onchange_rate(self):
        for line in self.update_line:
            line.rate = self.rate
            line.onchange_rate()

    def action_update_product_prices(self):
        self.ensure_one()

        self.disable_update_button = True

        for item in self.update_line:
            item.product_id.product_tmpl_id.write({
                'list_price': item.price,
            })

        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'update.sale.price.wizard',
            'target': 'new',
            'res_id': self.id
        }

    def action_print_label(self):
        data = {
            'product_ids': [line.product_id.id for line in self.update_line]
        }
        return self.env.ref('quanimo_soluti_product.action_product_sale_label_report').report_action(self, data)


class UpdateSalePriceWizardLine(models.TransientModel):
    _name = 'update.sale.price.wizard.line'

    parent_id = fields.Many2one('update.sale.price.wizard')
    product_id = fields.Many2one('product.product', required=True)
    list_price = fields.Float(related='product_id.product_tmpl_id.list_price')
    list_price_change_date = fields.Date(related='product_id.product_tmpl_id.list_price_change_date')
    rate = fields.Float(string='Rate')
    price = fields.Float('Price')

    @api.onchange('rate', 'list_price')
    def onchange_rate(self):
        for rec in self:
            if rec.price > 0.0:
                rec.price = rec.list_price + (rec.list_price * rec.rate / 100)
