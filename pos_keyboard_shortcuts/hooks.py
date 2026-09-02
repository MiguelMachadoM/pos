# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).


def post_init_hook(env):
    """Enable shortcuts on existing shops; they can be turned off per POS."""
    configs = env["pos.config"].search([("iface_keyboard_shortcuts", "=", False)])
    if configs:
        configs.write({"iface_keyboard_shortcuts": True})
