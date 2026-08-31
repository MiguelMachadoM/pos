# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

RECEIPT_FONT_SIZES = [
    ("small", "Small"),
    ("medium", "Medium"),
    ("large", "Large"),
]

TRACKING_FONT_SIZES = [
    ("hidden", "Hidden"),
    ("small", "Small"),
    ("medium", "Medium"),
    ("large", "Large"),
]

_COMPACT_POS_FIELDS = [
    "receipt_font_header",
    "receipt_font_tracking",
    "receipt_font_lines",
    "receipt_font_totals",
    "receipt_font_footer",
    "receipt_hide_unit_qty",
    "receipt_product_name_max",
]


class PosConfig(models.Model):
    _inherit = "pos.config"

    receipt_font_header = fields.Selection(
        selection=RECEIPT_FONT_SIZES,
        string="Receipt header size",
        default="medium",
        required=True,
    )
    receipt_font_tracking = fields.Selection(
        selection=TRACKING_FONT_SIZES,
        string="Receipt order number size",
        default="small",
        required=True,
        help="Size of the large order number (e.g. 007) on the ticket.",
    )
    receipt_font_lines = fields.Selection(
        selection=RECEIPT_FONT_SIZES,
        string="Receipt product lines size",
        default="small",
        required=True,
    )
    receipt_font_totals = fields.Selection(
        selection=RECEIPT_FONT_SIZES,
        string="Receipt totals size",
        default="medium",
        required=True,
    )
    receipt_font_footer = fields.Selection(
        selection=RECEIPT_FONT_SIZES,
        string="Receipt footer size",
        default="small",
        required=True,
    )
    receipt_hide_unit_qty = fields.Boolean(
        string="Hide qty line when quantity is 1",
        default=True,
        help="If the quantity is 1, hide the '1.00 x price / Unit' line.",
    )
    receipt_product_name_max = fields.Integer(
        string="Receipt product name max length",
        default=60,
        required=True,
        help="Maximum characters of the product name on the printed ticket. "
        "Use a higher value with a smaller product-line font. "
        "Set 0 to skip JS truncation (CSS ellipsis still applies).",
    )

    @api.constrains("receipt_product_name_max")
    def _check_receipt_product_name_max(self):
        for rec in self:
            if rec.receipt_product_name_max < 0:
                raise ValidationError(
                    _("Product name max length on the receipt cannot be negative.")
                )

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if not fields:
            fields = list(self._fields)
        else:
            fields = list(fields)
        for fname in _COMPACT_POS_FIELDS:
            if fname not in fields:
                fields.append(fname)
        return fields
