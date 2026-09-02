# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = "pos.config"

    iface_keyboard_shortcuts = fields.Boolean(
        string="Keyboard shortcuts",
        default=True,
        help="Enable cashier keyboard shortcuts on this Point of Sale. "
        "The key map is defined globally in Settings.",
    )
    keyboard_search_hold_seconds = fields.Integer(
        compute="_compute_keyboard_search_hold_seconds",
        help="After adding a product from search, keep the filter so another "
        "match can be tapped, and unfocus the box so the barcode scanner is "
        "not captured. 0 disables the hold (native search). Global setting.",
    )

    def _compute_keyboard_search_hold_seconds(self):
        raw = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("pos_keyboard_shortcuts.search_hold_seconds", "5")
        )
        try:
            hold = int(raw)
        except (TypeError, ValueError):
            hold = 5
        if hold not in (0, 5, 10):
            hold = 5
        for rec in self:
            rec.keyboard_search_hold_seconds = hold

    @api.model
    def _load_pos_data_fields(self, config_id):
        field_names = super()._load_pos_data_fields(config_id)
        extra = ["iface_keyboard_shortcuts", "keyboard_search_hold_seconds"]
        if not field_names:
            base = list(self._fields)
        else:
            base = list(field_names)
        for fname in extra:
            if fname in self._fields and fname not in base:
                base.append(fname)
        return base
