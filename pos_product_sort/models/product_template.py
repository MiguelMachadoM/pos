# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models

# New products and the install baseline use 1000 so the POS grid is not
# dominated by Odoo's create default (1). Lower values still sort first.
DEFAULT_PRODUCT_SEQUENCE = 1000
ODOO_CREATE_SEQUENCE = 1


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sequence = fields.Integer(
        default=DEFAULT_PRODUCT_SEQUENCE,
        help="Gives the sequence order when displaying a product list, "
        "including the POS grid when Sequence is used in "
        "Point of Sale > Configuration > Settings > POS product grid order. "
        "Lower values appear first. New products default to 1000 so they do "
        "not jump to the front of the POS grid. On install, rows still at "
        "Odoo's create default (1) are set to 1000; other Sequence values "
        "are left unchanged.",
    )
