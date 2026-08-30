# Copyright 2026 Miguel Machado <memachado@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon

# 1x1 PNG so the product card takes the image/overlay layout.
_TINY_PNG = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQ"
    "AAAABJRU5ErkJggg=="
)


@tagged("post_install", "-at_install")
class TestUi(TestPointOfSaleHttpCommon):
    def test_product_card_overlay_tour(self):
        self.env["product.product"].create(
            {
                "name": "Overlay Test Product With A Long Name",
                "available_in_pos": True,
                "default_code": "OVL-001",
                "image_1920": _TINY_PNG,
            }
        )
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.start_tour(
            "/pos/ui?config_id=%d" % self.main_pos_config.id,
            "PosProductCardOverlayTour",
            login="pos_user",
        )
