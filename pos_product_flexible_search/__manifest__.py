# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
{
    "name": "POS product flexible search",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Flexible multi-word product search in the Point of Sale",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "images": ["static/description/icon.png"],
    "license": "AGPL-3",
    "website": "https://github.com/OCA/pos",
    "maintainers": ["MiguelMachadoM"],
    "development_status": "Beta",
    "application": False,
    "installable": True,
    "depends": [
        "point_of_sale",
        "product",
    ],
    "data": [
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "/pos_product_flexible_search/static/src/js/product_screen_flexible_search.esm.js",
        ],
    },
}
