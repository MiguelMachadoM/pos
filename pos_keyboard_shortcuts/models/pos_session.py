# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, models


class PosSession(models.Model):
    _inherit = "pos.session"

    @api.model
    def _load_pos_data_models(self, config_id):
        models = super()._load_pos_data_models(config_id)
        if "pos.keyboard.shortcut" not in models:
            models.append("pos.keyboard.shortcut")
        return models
