# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).


def realign_baseline_product_sequence(env):
    """Set Sequence 1 (Odoo create default) to 1000. Leave any other value."""
    from .models.product_template import (
        DEFAULT_PRODUCT_SEQUENCE,
        ODOO_CREATE_SEQUENCE,
    )

    env.cr.execute(
        """
        UPDATE product_template
           SET sequence = %s
         WHERE sequence = %s
        """,
        (DEFAULT_PRODUCT_SEQUENCE, ODOO_CREATE_SEQUENCE),
    )
    env["product.template"].invalidate_model(["sequence"])


def post_init_hook(env):
    from .cron_utils import align_top_sales_ir_cron

    env["pos.config"].init_default_grid_sort_lines_all()
    env["product.product"].search(
        [("available_in_pos", "=", True)]
    )._recompute_pos_top_sales_qty()
    realign_baseline_product_sequence(env)
    align_top_sales_ir_cron(env)
