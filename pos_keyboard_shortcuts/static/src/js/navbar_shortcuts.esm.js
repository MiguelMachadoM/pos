/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {Navbar} from "@point_of_sale/app/navbar/navbar";
import {ShortcutHelpDialog} from "./help_dialog.esm";
import {bindShortcut} from "./bind_shortcut.esm";

patch(Navbar.prototype, {
    setup() {
        super.setup(...arguments);
        const pos = this.pos;
        bindShortcut(pos, "help", () => {
            this.dialog.add(ShortcutHelpDialog, {pos: this.pos});
        });
        bindShortcut(pos, "cancel_order", () => {
            const order = this.pos.get_order();
            if (order) {
                this.pos.onDeleteOrder(order);
            }
        });
    },
});
