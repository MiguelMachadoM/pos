# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
{
    "name": "POS keyboard shortcuts",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "summary": "Configurable cashier keyboard shortcuts for the Point of Sale",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "maintainers": ["MiguelMachadoM"],
    "website": "https://github.com/OCA/pos",
    "development_status": "Beta",
    "application": False,
    "installable": True,
    "post_init_hook": "post_init_hook",
    "depends": ["point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "data/pos_keyboard_shortcut_data.xml",
        "views/pos_keyboard_shortcut_views.xml",
        "views/pos_config_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_keyboard_shortcuts/static/src/js/**/*.esm.js",
            "pos_keyboard_shortcuts/static/src/xml/**/*.xml",
            "pos_keyboard_shortcuts/static/src/scss/**/*.scss",
        ],
    },
}
