/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {ReceiptScreen} from "@point_of_sale/app/screens/receipt_screen/receipt_screen";
import {bindFixedHotkey, bindShortcut} from "./bind_shortcut.esm";
import {isTextInput, shortcutLabel} from "./keyboard_map.esm";

patch(ReceiptScreen.prototype, {
    setup() {
        super.setup(...arguments);
        const pos = this.pos;
        const notInInput = () => !isTextInput(document.activeElement);
        bindShortcut(
            pos,
            "print_receipt",
            () => {
                this.doFullPrint.call();
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "print_basic",
            () => {
                if (!this.pos.config.basic_receipt) {
                    this.notification.add(_t("Basic receipt printing is not enabled on this POS."));
                    return;
                }
                this.doBasicPrint.call();
            },
            {isAvailable: notInInput}
        );
        bindFixedHotkey(
            pos,
            "enter",
            () => {
                this.orderDone();
            },
            {isAvailable: notInInput}
        );
    },

    get printFullShortcutLabel() {
        if (!this.pos.config.iface_keyboard_shortcuts) {
            return "";
        }
        return shortcutLabel(this.pos, "print_receipt");
    },

    get printBasicShortcutLabel() {
        if (!this.pos.config.iface_keyboard_shortcuts) {
            return "";
        }
        return shortcutLabel(this.pos, "print_basic");
    },
});
