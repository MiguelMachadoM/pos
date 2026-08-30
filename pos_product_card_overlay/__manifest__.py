# Copyright 2026 Miguel Machado <memachado@gmail.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "PoS Product Card Image Overlay",
    "summary": "Show product reference and name on a translucent band over the product image",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "maintainers": ["MiguelMachadoM"],
    "development_status": "Beta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["point_of_sale"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_product_card_overlay/static/src/scss/product_card_overlay.scss",
            "pos_product_card_overlay/static/src/js/product_card_overlay.esm.js",
            "pos_product_card_overlay/static/src/xml/product_card.xml",
        ],
        "web.assets_tests": [
            "pos_product_card_overlay/static/tests/tours/product_card_overlay_tour.esm.js",
        ],
    },
}
