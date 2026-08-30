# Copyright 2026 Miguel Machado <memachado@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.modules.module import get_manifest
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPosProductCardOverlayModule(TransactionCase):
    def test_depends_only_on_point_of_sale(self):
        """Overlay ships its own default_code line; no extra PoS addon required."""
        manifest = get_manifest("pos_product_card_overlay")
        self.assertEqual(manifest.get("depends"), ["point_of_sale"])
        self.assertNotIn(
            "pos_product_display_default_code",
            manifest.get("depends"),
        )

    def test_pos_assets_declared(self):
        manifest = get_manifest("pos_product_card_overlay")
        pos_assets = manifest.get("assets", {}).get("point_of_sale._assets_pos", [])
        self.assertTrue(
            any(path.endswith("product_card_overlay.esm.js") for path in pos_assets)
        )
        self.assertTrue(
            any(path.endswith("product_card_overlay.scss") for path in pos_assets)
        )
        self.assertTrue(any(path.endswith("product_card.xml") for path in pos_assets))
