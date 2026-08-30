# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_pos_product_grid_sort_line_ids = fields.One2many(
        related="pos_config_id.pos_product_grid_sort_line_ids",
        readonly=False,
    )
    pos_pos_product_grid_favorites_first = fields.Boolean(
        related="pos_config_id.pos_product_grid_favorites_first",
        readonly=False,
    )
    pos_sequence_top_sales_cron_active = fields.Boolean(
        string="Recompute top sales daily",
        compute="_compute_pos_sequence_top_sales_cron_active",
        inverse="_inverse_pos_sequence_top_sales_cron_active",
        readonly=False,
        help="Enable the daily scheduled action that updates POS quantity sold "
        "(used by the Top sales grid sort). Off by default. Shared by all "
        "POS shops. Hour and timezone are set on that scheduled action.",
    )

    def _pos_sequence_top_sales_cron(self):
        return self.env.ref(
            "pos_product_sort.ir_cron_recompute_pos_top_sales_qty",
            raise_if_not_found=False,
        )

    def _compute_pos_sequence_top_sales_cron_active(self):
        cron = self._pos_sequence_top_sales_cron()
        active = bool(cron and cron.active)
        for rec in self:
            rec.pos_sequence_top_sales_cron_active = active

    def _inverse_pos_sequence_top_sales_cron_active(self):
        cron = self._pos_sequence_top_sales_cron()
        if not cron:
            return
        active = any(self.mapped("pos_sequence_top_sales_cron_active"))
        cron.sudo().write({"active": active})
        if active:
            from ..cron_utils import align_top_sales_ir_cron

            align_top_sales_ir_cron(self.env)
