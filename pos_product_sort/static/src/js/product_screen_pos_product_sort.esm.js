/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";

const DEFAULT_SORT_SPEC = [
    {key: "sequence", direction: "asc"},
    {key: "default_code", direction: "asc"},
    {key: "name", direction: "asc"},
];

const NUMBER_KEYS = new Set(["sequence", "top_sales"]);
const STRING_KEYS = new Set(["default_code", "name"]);

function asNumber(value, fallback = 0) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
}

function asString(value) {
    return (value || "").toString().trim().toLowerCase();
}

function productName(product) {
    return product.name || product.display_name || "";
}

function normalizeSortKey(key) {
    return key === "pos_sequence" ? "sequence" : key;
}

/**
 * @param {import("@point_of_sale/app/store/pos_store").PosStore} pos
 * @returns {{key: string, direction: string}[]}
 */
function getSortSpec(pos) {
    const raw = pos.config?.pos_product_grid_sort_spec;
    if (!raw) {
        return DEFAULT_SORT_SPEC;
    }
    try {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length) {
            return parsed
                .filter((row) => row && row.key)
                .map((row) => ({
                    ...row,
                    key: normalizeSortKey(row.key),
                }));
        }
    } catch {
        // Ignore invalid JSON
    }
    return DEFAULT_SORT_SPEC;
}

/**
 * @param {Object} product
 * @param {String} key
 * @returns {number|string}
 */
function sortValue(product, key) {
    switch (key) {
        case "sequence":
            return asNumber(product.sequence, 1000);
        case "default_code":
            return asString(product.default_code);
        case "name":
            return asString(productName(product));
        case "top_sales":
            return asNumber(product.pos_top_sales_qty, 0);
        default:
            return asString(product[key]);
    }
}

function compareField(a, b, key) {
    if (NUMBER_KEYS.has(key)) {
        return sortValue(a, key) - sortValue(b, key);
    }
    if (STRING_KEYS.has(key)) {
        return sortValue(a, key).localeCompare(sortValue(b, key));
    }
    const left = sortValue(a, key);
    const right = sortValue(b, key);
    if (typeof left === "number" && typeof right === "number") {
        return left - right;
    }
    return asString(left).localeCompare(asString(right));
}

/**
 * @param {object[]} products
 * @param {{key: string, direction: string}[]} spec
 */
function sortProductsBySpec(products, spec) {
    const sortSpec = spec.length ? spec : DEFAULT_SORT_SPEC;
    return products.slice().sort((a, b) => {
        for (const {key, direction} of sortSpec) {
            const cmp = compareField(a, b, key);
            if (cmp !== 0) {
                return direction === "desc" ? -cmp : cmp;
            }
        }
        return 0;
    });
}

function isFavoriteProduct(product) {
    return Boolean(product.is_favorite);
}

/**
 * @param {import("@point_of_sale/app/store/pos_store").PosStore} pos
 */
function favoritesFirstEnabled(pos) {
    const raw =
        pos.config?.pos_product_grid_favorites_first ??
        pos.config?.raw?.pos_product_grid_favorites_first;
    return raw !== false && raw !== "false" && raw !== 0;
}

function compareFavorites(a, b) {
    return (isFavoriteProduct(b) ? 1 : 0) - (isFavoriteProduct(a) ? 1 : 0);
}

function sortProductsForPos(products, pos) {
    const spec = getSortSpec(pos);
    if (!favoritesFirstEnabled(pos)) {
        return sortProductsBySpec(products, spec);
    }
    return products.slice().sort((a, b) => {
        const byFavorite = compareFavorites(a, b);
        if (byFavorite !== 0) {
            return byFavorite;
        }
        const sortSpec = spec.length ? spec : DEFAULT_SORT_SPEC;
        for (const {key, direction} of sortSpec) {
            const cmp = compareField(a, b, key);
            if (cmp !== 0) {
                return direction === "desc" ? -cmp : cmp;
            }
        }
        return 0;
    });
}

patch(ProductScreen.prototype, {
    get productsToDisplay() {
        const products = super.productsToDisplay;
        // Browse only. Re-sorting search hits would replace match ranking
        // (core or pos_product_flexible_search) and extra-sort on each keystroke.
        if (this.searchWord) {
            return products;
        }
        return sortProductsForPos(products, this.pos);
    },
});
