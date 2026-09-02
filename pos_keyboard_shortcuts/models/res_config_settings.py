# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_iface_keyboard_shortcuts = fields.Boolean(
        related="pos_config_id.iface_keyboard_shortcuts",
        readonly=False,
    )
    keyboard_search_hold_seconds = fields.Selection(
        [("0", "Off"), ("5", "5 seconds"), ("10", "10 seconds")],
        string="Keep product search filter",
        config_parameter="pos_keyboard_shortcuts.search_hold_seconds",
        default="5",
        help="After adding a product from search, keep the filter so another "
        "match can be tapped, and unfocus the box so the barcode scanner is "
        "not captured. Off leaves the native search.",
    )
