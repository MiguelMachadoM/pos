# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo.tests.common import TransactionCase


class TestPosProductFlexibleSearch(TransactionCase):
    """Smoke tests for pos.config extension."""

    def test_pos_config_has_flexible_search_fields(self):
        PosConfig = self.env["pos.config"]
        self.assertIn("pos_product_search_min_chars", PosConfig._fields)

    def test_res_config_settings_pos_settings_alias_field(self):
        ResConfig = self.env["res.config.settings"]
        self.assertIn("pos_pos_product_search_min_chars", ResConfig._fields)

    def test_pos_load_fields_include_sequence(self):
        config = self.env["pos.config"].search([], limit=1)
        if not config:
            self.skipTest("No pos.config")
        fields_list = self.env["product.product"]._load_pos_data_fields(config.id)
        self.assertIn("sequence", fields_list)
