# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
{
    "name": "POS compact receipt lines",
    "summary": "Compact POS tickets: per-section font sizes, smaller order number, TOTAL in bold",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/pos",
    "license": "AGPL-3",
    "maintainers": ["MiguelMachadoM"],
    "development_status": "Beta",
    "depends": ["point_of_sale"],
    "data": [
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_receipt_compact/static/src/js/**/*.js",
            "pos_receipt_compact/static/src/xml/**/*.xml",
            "pos_receipt_compact/static/src/scss/**/*.scss",
        ],
    },
    "installable": True,
}
