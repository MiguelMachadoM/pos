# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).
{
    "name": "POS product grid sort",
    "summary": "Configurable POS grid sort (sequence, top sales) and favorites first",
    "version": "18.0.1.0.0",
    "category": "Point of Sale",
    "website": "https://github.com/OCA/pos",
    "author": "Miguel Machado, Odoo Community Association (OCA)",
    "maintainers": ["MiguelMachadoM"],
    "development_status": "Beta",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["product", "point_of_sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/product_template_views.xml",
        "views/product_product_views.xml",
        "views/res_config_settings_views.xml",
        "views/ir_cron_views.xml",
        "data/ir_cron_pos_top_sales.xml",
    ],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_product_sort/static/src/js/**/*.js",
        ],
    },
    "post_init_hook": "post_init_hook",
}
