/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {_t} from "@web/core/l10n/translation";
import {ControlButtons} from "@point_of_sale/app/screens/product_screen/control_buttons/control_buttons";
import {makeAwaitable} from "@point_of_sale/app/store/make_awaitable_dialog";
import {SelectionPopup} from "@point_of_sale/app/utils/input_popups/selection_popup";
import {shortcutLabel, shortcutsEnabled} from "./keyboard_map.esm";

function withShortcut(pos, action, title) {
    if (!shortcutsEnabled(pos)) {
        return title;
    }
    const label = shortcutLabel(pos, action);
    return label ? `${title}  (${label})` : title;
}

patch(ControlButtons.prototype, {
    shortcutLabel(action) {
        if (!shortcutsEnabled(this.pos)) {
            return "";
        }
        return shortcutLabel(this.pos, action);
    },

    async clickFiscalPosition() {
        const currentFiscalPosition = this.currentOrder.fiscal_position_id;
        const fiscalPosList = [
            {
                id: -1,
                label: this.pos.config.module_pos_restaurant ? _t("Dine in") : _t("Original Tax"),
                isSelected: false,
                item: "none",
            },
        ];
        for (const fiscalPos of this.pos.config.fiscal_position_ids) {
            fiscalPosList.push({
                id: fiscalPos.id,
                label: fiscalPos.name,
                isSelected: currentFiscalPosition
                    ? fiscalPos.id === currentFiscalPosition.id
                    : false,
                item: fiscalPos,
            });
        }

        const selectedFiscalPosition = await makeAwaitable(this.dialog, SelectionPopup, {
            list: fiscalPosList,
            title: withShortcut(this.pos, "fiscal", _t("Choose the tax you want to apply")),
        });

        if (!selectedFiscalPosition) {
            return;
        }

        if (selectedFiscalPosition === "none") {
            this.currentOrder.update({
                fiscal_position_id: false,
            });
            return;
        }

        this.currentOrder.update({
            fiscal_position_id: selectedFiscalPosition ? selectedFiscalPosition.id : false,
        });
    },

    async clickPricelist() {
        const selectionList = this.getPricelistList();
        const payload = await makeAwaitable(this.dialog, SelectionPopup, {
            title: withShortcut(this.pos, "pricelist", _t("Select the pricelist")),
            list: selectionList,
        });

        if (payload) {
            this.pos.selectPricelist(payload);
        }
    },
});
