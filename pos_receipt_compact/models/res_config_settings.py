# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_receipt_font_header = fields.Selection(
        related="pos_config_id.receipt_font_header",
        readonly=False,
    )
    pos_receipt_font_tracking = fields.Selection(
        related="pos_config_id.receipt_font_tracking",
        readonly=False,
    )
    pos_receipt_font_lines = fields.Selection(
        related="pos_config_id.receipt_font_lines",
        readonly=False,
    )
    pos_receipt_font_totals = fields.Selection(
        related="pos_config_id.receipt_font_totals",
        readonly=False,
    )
    pos_receipt_font_footer = fields.Selection(
        related="pos_config_id.receipt_font_footer",
        readonly=False,
    )
    pos_receipt_hide_unit_qty = fields.Boolean(
        related="pos_config_id.receipt_hide_unit_qty",
        readonly=False,
    )
    pos_receipt_product_name_max = fields.Integer(
        related="pos_config_id.receipt_product_name_max",
        readonly=False,
    )
