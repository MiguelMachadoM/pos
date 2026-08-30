# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

# Keys must stay in sync with static/src/js/product_screen_pos_product_sort.esm.js
POS_GRID_SORT_FIELD_KEYS = [
    ("sequence", "Sequence"),
    ("default_code", "Internal reference"),
    ("name", "Name"),
    ("top_sales", "Top sales (POS quantity sold)"),
]


class PosConfigProductGridSortLine(models.Model):
    _name = "pos.config.product.grid.sort.line"
    _description = "POS product grid sort criterion"
    _order = "sequence, id"

    config_id = fields.Many2one(
        "pos.config",
        string="POS configuration",
        required=True,
        ondelete="cascade",
    )
    sequence = fields.Integer(default=10)
    field_key = fields.Selection(
        selection=POS_GRID_SORT_FIELD_KEYS,
        string="Sort by",
        required=True,
        default="sequence",
    )
    direction = fields.Selection(
        selection=[("asc", "Ascending"), ("desc", "Descending")],
        string="Direction",
        required=True,
        default="asc",
    )

    @api.constrains("field_key", "config_id")
    def _check_unique_field_key_per_config(self):
        for config in self.mapped("config_id"):
            keys = config.pos_product_grid_sort_line_ids.mapped("field_key")
            if len(keys) != len(set(keys)):
                raise ValidationError(
                    _(
                        "Each sort field can only appear once in the grid order "
                        "for POS configuration '%(config)s'."
                    )
                    % {"config": config.display_name}
                )
