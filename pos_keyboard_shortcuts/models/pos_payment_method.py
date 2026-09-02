# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    def write(self, vals):
        result = super().write(vals)
        if "config_ids" in vals:
            extras = self.env["pos.keyboard.shortcut"].search(
                [
                    ("action", "=", "pay_method"),
                    ("payment_method_id", "in", self.ids),
                ]
            )
            extras._check_duplicate_combo()
        return result
