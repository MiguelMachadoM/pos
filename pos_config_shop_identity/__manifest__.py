# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
{
    "name": "POS shop identity on receipts",
    "summary": "Per POS commercial name, address and phone on the ticket header",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "maintainers": ["MiguelMachadoM"],
    "development_status": "Beta",
    "depends": ["point_of_sale", "base_location"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_config_shop_identity/static/src/js/**/*.js",
            "pos_config_shop_identity/static/src/xml/**/*.xml",
            "pos_config_shop_identity/static/src/scss/**/*.scss",
        ],
    },
    "installable": True,
}
