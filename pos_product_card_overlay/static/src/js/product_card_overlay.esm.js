/* Copyright 2026 Miguel Machado <memachado@gmail.com>
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
/** @odoo-module **/

import {patch} from "@web/core/utils/patch";
import {ProductCard} from "@point_of_sale/app/generic_components/product_card/product_card";

/**
 * Read default_code from the standard PoS product payload.
 * Implemented here so this addon does not depend on pos_product_display_default_code.
 */
function productDefaultCode(product) {
    const raw = product?.default_code ?? product?.raw?.default_code;
    if (raw === false || raw === null || raw === undefined) {
        return "";
    }
    return String(raw).trim();
}

/**
 * If another addon prefixed the displayed name with "[CODE] ", strip it so the
 * overlay can show the reference on its own line without duplicating it.
 */
function stripReferencePrefix(name, code) {
    if (!code) {
        return name;
    }
    const bracketed = `[${code}]`;
    if (name.startsWith(bracketed)) {
        return name.slice(bracketed.length).trimStart();
    }
    return name;
}

patch(ProductCard.prototype, {
    get cardReference() {
        const code = productDefaultCode(this.props.product);
        return code ? `[${code}]` : "";
    },

    get cardProductName() {
        const name = this.props.name || "";
        return stripReferencePrefix(name, productDefaultCode(this.props.product));
    },
});
