# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

import json

from odoo import Command, api, fields, models

DEFAULT_GRID_SORT_LINES = [
    {"sequence": 10, "field_key": "sequence", "direction": "asc"},
    {"sequence": 20, "field_key": "default_code", "direction": "asc"},
    {"sequence": 30, "field_key": "name", "direction": "asc"},
]


class PosConfig(models.Model):
    _inherit = "pos.config"

    pos_product_grid_sort_line_ids = fields.One2many(
        "pos.config.product.grid.sort.line",
        "config_id",
        string="Product grid sort order",
        help="Fields and direction used to order products in the POS grid "
        "(first row = highest priority).",
    )
    pos_product_grid_sort_spec = fields.Char(
        compute="_compute_pos_product_grid_sort_spec",
        store=True,
        help="JSON sort specification sent to the POS client.",
    )
    pos_product_grid_favorites_first = fields.Boolean(
        string="POS grid: favorites first",
        default=True,
        help="When enabled, products marked as favorites in the catalog are shown "
        "before others in the POS grid. Within favorites and non-favorites, the "
        "configured sort order still applies.",
    )

    @api.model
    def _default_pos_product_grid_sort_line_ids(self):
        return [Command.create(line) for line in DEFAULT_GRID_SORT_LINES]

    @api.depends(
        "pos_product_grid_sort_line_ids",
        "pos_product_grid_sort_line_ids.sequence",
        "pos_product_grid_sort_line_ids.field_key",
        "pos_product_grid_sort_line_ids.direction",
    )
    def _compute_pos_product_grid_sort_spec(self):
        for config in self:
            lines = config.pos_product_grid_sort_line_ids.sorted("sequence")
            if not lines:
                spec = DEFAULT_GRID_SORT_LINES
            else:
                spec = [
                    {"key": line.field_key, "direction": line.direction}
                    for line in lines
                ]
            config.pos_product_grid_sort_spec = json.dumps(spec)

    def _ensure_default_grid_sort_lines(self):
        for config in self:
            if not config.pos_product_grid_sort_line_ids:
                config.write(
                    {
                        "pos_product_grid_sort_line_ids": [
                            Command.create(line) for line in DEFAULT_GRID_SORT_LINES
                        ]
                    }
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._ensure_default_grid_sort_lines()
        return records

    @api.model
    def init_default_grid_sort_lines_all(self):
        """Called on module install/upgrade for configs without sort lines."""
        configs = self.search([("pos_product_grid_sort_line_ids", "=", False)])
        configs._ensure_default_grid_sort_lines()
        return True

    @api.model
    def _load_pos_data_fields(self, config_id):
        field_names = super()._load_pos_data_fields(config_id)
        extra = ["pos_product_grid_sort_spec", "pos_product_grid_favorites_first"]
        if not field_names:
            base = list(self._fields)
        else:
            base = list(field_names)
        for fname in extra:
            if fname in self._fields and fname not in base:
                base.append(fname)
        return base

    def action_recompute_pos_top_sales(self):
        products = self.env["product.product"].search([("available_in_pos", "=", True)])
        products._recompute_pos_top_sales_qty()
        return True
