# -*- coding: utf-8 -*-
# Copyright (C) 2023 Quanimo (https://www.quanimo.com)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

import math

from odoo import api, models


class ProductSaleLabelViewPdf(models.AbstractModel):
    _name = 'report.quanimo_soluti_product.product_sale_label_view_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        products = []

        for rec in data['product_ids']:
            product = self.env['product.product'].browse(rec)
            if product:
                decimal, price = math.modf(product.product_tmpl_id.list_price)

                products.append({
                    'product': product,
                    'price': int(price),
                    'decimal': int(decimal * 100),
                    'list_price_change_date': product.product_tmpl_id.list_price_change_date
                })
        return {
            'items': products
        }
