/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {TextInputPopup} from "@point_of_sale/app/utils/input_popups/text_input_popup";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {bindFixedHotkey, bindShortcut} from "./bind_shortcut.esm";
import {isProductSearchInput, isTextInput} from "./keyboard_map.esm";
import {
    afterSearchProductAdded,
    clearProductSearch,
    focusProductSearch,
} from "./search_hold.esm";

function selectedLine(pos) {
    return pos.get_order()?.get_selected_orderline();
}

function notify(service, message) {
    service.add(message);
}

function controlButtonContext(component) {
    const ctx = Object.create(ControlButtons.prototype);
    ctx.pos = component.pos;
    ctx.dialog = component.dialog;
    ctx.notification = component.notification;
    ctx.env = component.env;
    Object.defineProperty(ctx, "currentOrder", {
        get: () => component.pos.get_order(),
    });
    return ctx;
}

function callControlButton(component, methodName) {
    const fn = ControlButtons.prototype[methodName];
    if (typeof fn !== "function") {
        return false;
    }
    fn.call(controlButtonContext(component));
    return true;
}

function setNumpadMode(component, mode) {
    component.numberBuffer.capture();
    component.numberBuffer.reset();
    component.pos.numpadMode = mode;
}

patch(ProductScreen.prototype, {
    setup() {
        super.setup(...arguments);
        const pos = this.pos;

        const notInInput = () => !isTextInput(document.activeElement);
        const inSearch = () => isProductSearchInput(document.activeElement);

        bindShortcut(pos, "search", () => focusProductSearch(), {
            isAvailable: notInInput,
        });
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
            "discount_line",
            () => {
                if (!this.pos.config.manual_discount) {
                    notify(this.notification, _t("Line discounts are not enabled on this POS."));
                    return;
                }
                if (!selectedLine(this.pos)) {
                    notify(this.notification, _t("Select a product line first."));
                    return;
                }
                setNumpadMode(this, "discount");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "price",
            () => {
                if (!this.pos.cashierHasPriceControlRights()) {
                    notify(
                        this.notification,
                        _t("You are not allowed to change prices on this POS.")
                    );
                    return;
                }
                if (!selectedLine(this.pos)) {
                    notify(this.notification, _t("Select a product line first."));
                    return;
                }
                setNumpadMode(this, "price");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "quantity",
            () => {
                setNumpadMode(this, "quantity");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "discount_global",
            () => {
                if (
                    !this.pos.config.module_pos_discount ||
                    !this.pos.config.discount_product_id
                ) {
                    notify(this.notification, _t("Global discount is not available."));
                    return;
                }
                if (!callControlButton(this, "clickDiscount")) {
                    notify(this.notification, _t("Global discount is not available."));
                }
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "tickets",
            () => {
                this.pos.showScreen("TicketScreen");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "refund",
            () => {
                callControlButton(this, "clickRefund");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "pricelist",
            () => {
                if (!this.pos.config.use_pricelist) {
                    notify(this.notification, _t("Pricelists are not enabled on this POS."));
                    return;
                }
                callControlButton(this, "clickPricelist");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "fiscal",
            () => {
                if (!(this.pos.config.fiscal_position_ids || []).length) {
                    notify(this.notification, _t("No fiscal position is available."));
                    return;
                }
                callControlButton(this, "clickFiscalPosition");
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "note",
            async () => {
                const line = selectedLine(this.pos);
                if (!line) {
                    notify(this.notification, _t("Select a product line first."));
                    return;
                }
                const payload = await makeAwaitable(this.dialog, TextInputPopup, {
                    title: _t("Internal Note"),
                    rows: 4,
                    startingValue: line.getNote() || "",
                });
                if (typeof payload === "string") {
                    line.setNote(payload);
                }
            },
            {isAvailable: notInInput}
        );
        bindShortcut(
            pos,
            "remove_line",
            () => {
                const line = selectedLine(this.pos);
                if (!line) {
                    notify(this.notification, _t("Select a product line first."));
                    return;
                }
                this.pos.get_order().removeOrderline(line);
            },
            {isAvailable: notInInput}
        );

        bindFixedHotkey(
            pos,
            "escape",
            () => {
                clearProductSearch(this.pos);
            },
            {
                bypassEditableProtection: true,
                isAvailable: () =>
                    inSearch() || Boolean((this.pos.searchProductWord || "").trim()),
            }
        );
        bindFixedHotkey(
            pos,
            "enter",
            () => {
                const matches = this.productsToDisplay || [];
                if (matches.length === 1) {
                    this.addProductToOrder(matches[0]);
                }
            },
            {bypassEditableProtection: true, isAvailable: inSearch}
        );
        bindFixedHotkey(
            pos,
            "enter",
            () => {
                if (!this.currentOrder?.is_empty()) {
                    this.pos.pay();
                }
            },
            {isAvailable: notInInput}
        );
        bindFixedHotkey(
            pos,
            "arrowup",
            () => this._selectOrderlineByOffset(-1),
            {allowRepeat: true, isAvailable: notInInput}
        );
        bindFixedHotkey(
            pos,
            "arrowdown",
            () => this._selectOrderlineByOffset(1),
            {allowRepeat: true, isAvailable: notInInput}
        );
    },

    _selectOrderlineByOffset(offset) {
        const order = this.pos.get_order();
        const lines = order?.get_orderlines?.() || [];
        if (!lines.length) {
            return;
        }
        const current = order.get_selected_orderline();
        let index = lines.indexOf(current);
        if (index < 0) {
            index = offset > 0 ? -1 : 0;
        }
        const next = lines[index + offset];
        if (next) {
            this.pos.selectOrderLine(order, next);
        }
    },

    async addProductToOrder(product) {
        const result = await super.addProductToOrder(product);
        afterSearchProductAdded(this.pos);
        return result;
    },
});
