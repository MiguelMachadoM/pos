# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

import odoo.tests

from odoo.addons.point_of_sale.tests.common import TestPoSCommon


@odoo.tests.tagged("post_install", "-at_install")
class TestPosSequence(TestPoSCommon):
    def test_product_template_sequence_default(self):
        template = self.env["product.template"].create(
            {
                "name": "POS sequence default test",
                "list_price": 10.0,
                "available_in_pos": True,
            }
        )
        self.assertEqual(template.sequence, 1000)

    def test_product_template_keeps_explicit_sequence(self):
        template = self.env["product.template"].create(
            {
                "name": "POS sequence explicit test",
                "list_price": 10.0,
                "available_in_pos": True,
                "sequence": 1,
            }
        )
        self.assertEqual(template.sequence, 1)

    def test_realign_baseline_only_changes_odoo_default(self):
        from ..hooks import (
            realign_baseline_product_sequence,
        )

        baseline = self.env["product.template"].create(
            {
                "name": "POS sequence realign 1",
                "list_price": 10.0,
                "available_in_pos": True,
                "sequence": 1,
            }
        )
        featured = self.env["product.template"].create(
            {
                "name": "POS sequence realign 5",
                "list_price": 10.0,
                "available_in_pos": True,
                "sequence": 5,
            }
        )
        realign_baseline_product_sequence(self.env)
        self.assertEqual(baseline.sequence, 1000)
        self.assertEqual(featured.sequence, 5)

    def test_product_variant_inherits_sequence(self):
        template = self.env["product.template"].create(
            {
                "name": "POS sequence related test",
                "list_price": 10.0,
                "available_in_pos": True,
                "sequence": 5,
            }
        )
        variant = template.product_variant_id
        self.assertEqual(variant.sequence, 5)

        variant.sequence = 99
        self.assertEqual(template.sequence, 99)

    def test_product_product_load_pos_data_fields_includes_sequence(self):
        fields_list = self.env["product.product"]._load_pos_data_fields(
            self.basic_config.id
        )
        self.assertIn("sequence", fields_list)
