/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {SelectPartnerButton} from "@point_of_sale/app/screens/product_screen/control_buttons/select_partner_button/select_partner_button";
import {OrderlineNoteButton} from "@point_of_sale/app/screens/product_screen/control_buttons/customer_note_button/customer_note_button";
import {shortcutLabel, shortcutsEnabled} from "./keyboard_map.esm";

patch(SelectPartnerButton.prototype, {
    get customerShortcutLabel() {
        if (!shortcutsEnabled(this.pos)) {
            return "";
        }
        return shortcutLabel(this.pos, "customer");
    },
});

patch(OrderlineNoteButton.prototype, {
    get noteShortcutLabel() {
        if (!shortcutsEnabled(this.pos)) {
            return "";
        }
        return shortcutLabel(this.pos, "note");
    },
});
