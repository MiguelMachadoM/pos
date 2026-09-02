/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {PaymentScreen} from "@point_of_sale/app/screens/payment_screen/payment_screen";
import {bindFixedHotkey, bindShortcut, bindShortcutRecord} from "./bind_shortcut.esm";
import {
    extraPaymentShortcuts,
    formatShortcutLabel,
    isTextInput,
    paymentMethodId,
    shortcutLabel,
} from "./keyboard_map.esm";

function notify(service, message) {
    service.add(message);
}

function firstMethodByType(component, type) {
    return (component.payment_methods_from_config || []).find((method) => method.type === type);
}

function methodOnThisPos(component, methodLike) {
    const id = paymentMethodId(methodLike);
    if (!id) {
        return null;
    }
    return (component.payment_methods_from_config || []).find((method) => method.id === id) || null;
}

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        const pos = this.pos;
        const notInInput = () => !isTextInput(document.activeElement);

        bindShortcut(
            pos,
            "pay_cash",
            () => {
                const method = firstMethodByType(this, "cash");
                if (!method) {
                    notify(this.notification, _t("No cash payment method is configured."));
                    return;
                }
                this.addNewPaymentLine(method);
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "pay_bank",
            () => {
                const method = firstMethodByType(this, "bank");
                if (!method) {
                    notify(this.notification, _t("No card payment method is configured."));
                    return;
                }
                this.addNewPaymentLine(method);
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "customer",
            () => {
                this.pos.selectPartner();
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "invoice",
            () => {
                this.toggleIsToInvoice();
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "print_receipt",
            () => this._shortcutPrintReceipt(),
            {isAvailable: notInInput}
        );
        for (const rec of extraPaymentShortcuts(pos)) {
            bindShortcutRecord(
                pos,
                rec,
                () => {
                    const method = methodOnThisPos(this, rec.payment_method_id);
                    if (!method) {
                        return;
                    }
                    this.addNewPaymentLine(method);
                },
                {
                    isAvailable: () =>
                        notInInput() && Boolean(methodOnThisPos(this, rec.payment_method_id)),
                }
            );
        }
        bindFixedHotkey(
            pos,
            "enter",
            () => {
                this.validateOrder(false);
            },
            {isAvailable: notInInput}
        );
        bindFixedHotkey(
            pos,
            "escape",
            () => {
                this.pos.onClickBackButton();
            },
            {isAvailable: notInInput}
        );
    },

    _shortcutPrintReceipt() {
        if (this.pos.config.iface_print_auto) {
            notify(
                this.notification,
                _t("Automatic printing is enabled; the print shortcut is inactive.")
            );
            return;
        }
        if (!this.currentOrder) {
            notify(this.notification, _t("There is no ticket to print."));
            return;
        }
        this.pos.printReceipt({order: this.currentOrder});
    },

    paymentMethodShortcutLabel(paymentMethod) {
        if (!this.pos.config.iface_keyboard_shortcuts) {
            return "";
        }
        const extra = extraPaymentShortcuts(this.pos).find(
            (rec) => paymentMethodId(rec.payment_method_id) === paymentMethod.id
        );
        if (extra) {
            return formatShortcutLabel(extra);
        }
        if (paymentMethod.type === "cash") {
            const cashMethods = (this.payment_methods_from_config || []).filter(
                (method) => method.type === "cash"
            );
            if (cashMethods[0]?.id === paymentMethod.id) {
                return shortcutLabel(this.pos, "pay_cash");
            }
        }
        if (paymentMethod.type === "bank") {
            const bankMethods = (this.payment_methods_from_config || []).filter(
                (method) => method.type === "bank"
            );
            if (bankMethods[0]?.id === paymentMethod.id) {
                return shortcutLabel(this.pos, "pay_bank");
            }
        }
        return "";
    },

    get invoiceShortcutLabel() {
        if (!this.pos.config.iface_keyboard_shortcuts) {
            return "";
        }
        return shortcutLabel(this.pos, "invoice");
    },

    get customerShortcutLabel() {
        if (!this.pos.config.iface_keyboard_shortcuts) {
            return "";
        }
        return shortcutLabel(this.pos, "customer");
    },
});
