# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

import json

import odoo.tests
from odoo import Command

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPosGridSortConfig(TestPoSCommon):
    def test_pos_config_default_sort_lines(self):
        config = self.basic_config
        config.init_default_grid_sort_lines_all()
        self.assertEqual(len(config.pos_product_grid_sort_line_ids), 3)
        keys = config.pos_product_grid_sort_line_ids.sorted("sequence").mapped(
            "field_key"
        )
        self.assertEqual(keys, ["sequence", "default_code", "name"])

    def test_pos_config_sort_spec_json(self):
        config = self.basic_config
        config.write(
            {
                "pos_product_grid_sort_line_ids": [
                    Command.clear(),
                    Command.create(
                        {
                            "sequence": 1,
                            "field_key": "top_sales",
                            "direction": "desc",
                        }
                    ),
                    Command.create(
                        {
                            "sequence": 2,
                            "field_key": "name",
                            "direction": "asc",
                        }
                    ),
                ]
            }
        )
        spec = json.loads(config.pos_product_grid_sort_spec)
        self.assertEqual(
            spec,
            [
                {"key": "top_sales", "direction": "desc"},
                {"key": "name", "direction": "asc"},
            ],
        )

    def test_pos_config_load_pos_data_includes_sort_spec(self):
        fields_list = self.env["pos.config"]._load_pos_data_fields(self.basic_config.id)
        self.assertIn("pos_product_grid_sort_spec", fields_list)

    def test_pos_config_favorites_first_default_and_load(self):
        config = self.basic_config
        self.assertTrue(config.pos_product_grid_favorites_first)
        fields_list = self.env["pos.config"]._load_pos_data_fields(config.id)
        self.assertIn("pos_product_grid_favorites_first", fields_list)

    def test_product_load_pos_data_includes_is_favorite(self):
        fields_list = self.env["product.product"]._load_pos_data_fields(
            self.basic_config.id
        )
        self.assertIn("is_favorite", fields_list)

    def test_favorite_on_template_visible_on_variant(self):
        template = self.env["product.template"].create(
            {
                "name": "Favorite POS test",
                "available_in_pos": True,
                "list_price": 1.0,
                "is_favorite": True,
            }
        )
        variant = template.product_variant_id
        self.assertTrue(variant.is_favorite)

    def test_product_load_pos_data_includes_top_sales(self):
        fields_list = self.env["product.product"]._load_pos_data_fields(
            self.basic_config.id
        )
        self.assertIn("pos_top_sales_qty", fields_list)

    def test_recompute_top_sales_qty(self):
        product = self.env["product.product"].create(
            {
                "name": "Top sales test",
                "available_in_pos": True,
                "list_price": 5.0,
            }
        )
        product._recompute_pos_top_sales_qty()
        self.assertEqual(product.pos_top_sales_qty, 0.0)
