# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

import odoo.tests
from odoo import fields

from odoo.addons.point_of_sale.tests.common import TestPoSCommon

from ..cron_utils import (
    next_top_sales_cron_nextcall_utc_naive,
)


@odoo.tests.tagged("post_install", "-at_install")
class TestPosTopSalesCron(TestPoSCommon):
    def test_top_sales_cron_detected_by_code(self):
        cron = self.env.ref("pos_product_sort.ir_cron_recompute_pos_top_sales_qty")
        self.assertTrue(cron.is_pos_sequence_top_sales_cron)

    def test_nextcall_uses_america_new_york_local_slot(self):
        cron = self.env.ref("pos_product_sort.ir_cron_recompute_pos_top_sales_qty")
        cron.write(
            {
                "pos_sequence_local_hour": 3,
                "pos_sequence_local_minute": 0,
                "pos_sequence_local_tz": "America/New_York",
            }
        )
        reference = fields.Datetime.to_datetime("2026-05-20 10:00:00")
        next_utc = next_top_sales_cron_nextcall_utc_naive(cron, reference, self.env)
        next_str = fields.Datetime.to_string(next_utc)
        self.assertTrue(next_str.endswith("07:00:00"))

    def test_write_hour_updates_nextcall(self):
        cron = self.env.ref("pos_product_sort.ir_cron_recompute_pos_top_sales_qty")
        cron.write(
            {
                "pos_sequence_local_hour": 4,
                "pos_sequence_local_minute": 30,
                "pos_sequence_local_tz": "UTC",
            }
        )
        self.assertTrue(cron.nextcall)

    def test_top_sales_cron_inactive_by_default(self):
        cron = self.env.ref("pos_product_sort.ir_cron_recompute_pos_top_sales_qty")
        self.assertFalse(cron.active)

    def test_pos_settings_toggle_enables_and_disables_cron(self):
        cron = self.env.ref("pos_product_sort.ir_cron_recompute_pos_top_sales_qty")
        cron.sudo().write({"active": False})
        wizard = self.env["res.config.settings"].create(
            {
                "pos_config_id": self.basic_config.id,
                "pos_sequence_top_sales_cron_active": True,
            }
        )
        self.assertTrue(cron.active)
        wizard.pos_sequence_top_sales_cron_active = False
        self.assertFalse(cron.active)
