# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    pos_top_sales_qty = fields.Float(
        string="POS quantity sold",
        default=0.0,
        help="Total quantity sold on paid POS orders (all configurations). "
        "Used when «Top sales» is enabled in the POS grid sort order. "
        "Updated by the scheduled action «POS sequence: recompute top sales "
        "quantities» when that job is enabled in POS settings "
        "(Recompute top sales daily).",
    )

    def _recompute_pos_top_sales_qty(self):
        products = self or self.search([("available_in_pos", "=", True)])
        if not products:
            return
        groups = self.env["pos.order.line"].read_group(
            domain=[
                ("product_id", "in", products.ids),
                ("order_id.state", "in", ("paid", "invoiced", "done")),
            ],
            fields=["product_id", "qty:sum"],
            groupby=["product_id"],
        )
        qty_by_product = {
            group["product_id"][0]: group["qty"]
            for group in groups
            if group.get("product_id")
        }
        for product in products:
            product.pos_top_sales_qty = qty_by_product.get(product.id, 0.0)

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields_list = super()._load_pos_data_fields(config_id)
        extras = ("sequence", "pos_top_sales_qty", "is_favorite")
        fields_list = list(fields_list)
        for extra in extras:
            if extra not in fields_list:
                fields_list.append(extra)
        return fields_list
