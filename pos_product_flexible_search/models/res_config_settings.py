# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # Core POS settings `create` strips the first ``pos_`` prefix and writes the rest
    # to ``pos.config``; the target field name must therefore be ``pos_<rest>`` here
    # so that ``rest`` is ``pos_product_search_min_chars`` on ``pos.config``.
    pos_pos_product_search_min_chars = fields.Integer(
        related="pos_config_id.pos_product_search_min_chars",
        readonly=False,
    )
