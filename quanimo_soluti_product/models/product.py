# -*- coding: utf-8 -*-
# Copyright (C) 2023 Quanimo (https://www.quanimo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, api, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sequence_id = fields.Many2one('ir.sequence', domain=[('code', 'ilike', 'product.product.default_code')],
                                  string='Sequence')
    list_price_change_date = fields.Date()
    price_rate = fields.Float('List Price Rate')

    @api.depends('product_variant_ids', 'product_variant_ids.price_rate')
    def _compute_price_rate(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.price_rate = template.product_variant_ids.price_rate
        for template in (self - unique_variants):
            template.price_rate = False

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if 'sequence_id' in val and val.get('sequence_id') and not val.get('default_code', False):
                seq_rec = self.env['ir.sequence'].browse(val['sequence_id'])
                val['default_code'] = self.env['ir.sequence'].next_by_code(seq_rec.code)

        return super(ProductTemplate, self).create(vals_list)

    def write(self, vals):
        default_code = vals.get('default_code', self.default_code)
        sequence_id = vals.get('sequence_id', self.sequence_id and self.sequence_id.id or False)

        if not default_code and sequence_id:
            seq_rec = self.env['ir.sequence'].browse(sequence_id)
            vals['default_code'] = self.env['ir.sequence'].next_by_code(seq_rec.code)

        if 'list_price' in vals:
            vals['list_price_change_date'] = fields.Date.today()

        return super(ProductTemplate, self).write(vals)

    def action_print_label(self):
        data = {
            'product_ids': [id for id in self.mapped('product_variant_id').ids]
        }
        return self.env.ref('quanimo_soluti_product.action_product_sale_label_report').report_action(self, data)


class ProductProduct(models.Model):
    _inherit = 'product.product'

    sequence_id = fields.Many2one('ir.sequence', domain=[('code', 'ilike', 'product.product.default_code')],
                                  string='Sequence')
    price_rate = fields.Float('List Price Rate')

    @api.model_create_multi
    def create(self, vals_list):
        for val in vals_list:
            if 'sequence_id' in val and val.get('sequence_id') and not val.get('default_code', False):
                seq_rec = self.env['ir.sequence'].browse(val['sequence_id'])
                val['default_code'] = self.env['ir.sequence'].next_by_code(seq_rec.code)

        return super(ProductProduct, self).create(vals_list)

    def write(self, vals):
        default_code = vals.get('default_code', self.default_code)
        sequence_id = vals.get('sequence_id', self.sequence_id and self.sequence_id.id or False)

        if not default_code and sequence_id:
            seq_rec = self.env['ir.sequence'].browse(sequence_id)
            vals['default_code'] = self.env['ir.sequence'].next_by_code(seq_rec.code)

        return super(ProductProduct, self).write(vals)

    def action_print_label(self):
        data = {
            'product_ids': [id for id in self.ids]
        }
        return self.env.ref('quanimo_soluti_product.action_product_sale_label_report').report_action(self, data)
