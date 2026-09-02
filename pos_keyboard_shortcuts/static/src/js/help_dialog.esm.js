/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {Component} from "@odoo/owl";
import {Dialog} from "@web/core/dialog/dialog";
import {_t} from "@web/core/l10n/translation";
import {formatShortcutLabel, paymentMethodId, shortcutRecords} from "./keyboard_map.esm";

const ACTION_LABELS = {
    search: () => _t("Focus product search"),
    customer: () => _t("Customer"),
    discount_line: () => _t("Line discount"),
    price: () => _t("Line price"),
    quantity: () => _t("Quantity"),
    discount_global: () => _t("Global discount"),
    tickets: () => _t("Orders / tickets"),
    refund: () => _t("Refund"),
    pricelist: () => _t("Pricelist"),
    fiscal: () => _t("Fiscal position"),
    note: () => _t("Note"),
    remove_line: () => _t("Remove line"),
    help: () => _t("This help"),
    cancel_order: () => _t("Cancel order"),
    pay_cash: () => _t("Cash payment"),
    pay_bank: () => _t("Card payment"),
    pay_method: () => _t("Payment method"),
    invoice: () => _t("Toggle invoice"),
    print_receipt: () => _t("Print full receipt"),
    print_basic: () => _t("Print basic receipt"),
};

const SCOPE_LABELS = {
    product: () => _t("Products"),
    payment: () => _t("Payment"),
    receipt: () => _t("Receipt"),
    global: () => _t("Always"),
};

export class ShortcutHelpDialog extends Component {
    static template = "pos_keyboard_shortcuts.ShortcutHelpDialog";
    static components = {Dialog};
    static props = {
        close: Function,
        pos: Object,
    };

    get rows() {
        const methodIds = new Set(
            (this.props.pos.config.payment_method_ids || []).map((method) => method.id)
        );
        return shortcutRecords(this.props.pos)
            .filter((rec) => {
                if (rec.action !== "pay_method") {
                    return true;
                }
                return methodIds.has(paymentMethodId(rec.payment_method_id));
            })
            .map((rec) => {
                let action = (ACTION_LABELS[rec.action] || (() => rec.action))();
                if (rec.action === "pay_method") {
                    action =
                        rec.payment_method_id?.display_name ||
                        rec.payment_method_id?.name ||
                        action;
                }
                return {
                    keyId: String(rec.id),
                    action,
                    scope: (SCOPE_LABELS[rec.scope] || (() => rec.scope))(),
                    key: formatShortcutLabel(rec),
                };
            });
    }

    get fixedRows() {
        return [
            {key: "↑ ↓", action: _t("Previous / next order line"), scope: _t("Products")},
            {key: "Enter", action: _t("Go to payment"), scope: _t("Products")},
            {key: "Enter", action: _t("Add unique search result"), scope: _t("Search")},
            {key: "Enter", action: _t("Validate order"), scope: _t("Payment")},
            {key: "Enter", action: _t("New order"), scope: _t("Receipt")},
            {key: "Esc", action: _t("Clear search and release focus"), scope: _t("Search")},
            {key: "Esc", action: _t("Back to products"), scope: _t("Payment")},
        ];
    }
}
