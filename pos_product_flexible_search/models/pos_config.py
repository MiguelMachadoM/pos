# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_product_search_min_chars = fields.Integer(
        string="POS: minimum characters for product search",
        default=5,
        help="The POS client-side product filter runs only when the search text has at least "
        "this many characters. Use 0 to filter from the first character (heavy on large catalogs).",
    )

    @api.constrains("pos_product_search_min_chars")
    def _check_pos_product_search_min_chars(self):
        for rec in self:
            if (
                rec.pos_product_search_min_chars is not None
                and rec.pos_product_search_min_chars < 0
            ):
                raise ValidationError(
                    _(
                        "Minimum characters for POS product search must be zero or positive."
                    )
                )

    @api.model
    def _load_pos_data_fields(self, config_id):
        field_names = super()._load_pos_data_fields(config_id)
        extra = ["pos_product_search_min_chars"]
        if not field_names:
            base = list(self._fields)
        else:
            base = list(field_names)
        for fname in extra:
            if fname in self._fields and fname not in base:
                base.append(fname)
        return base
