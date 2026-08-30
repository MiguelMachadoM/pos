/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {patch} from "@web/core/utils/patch";
import {ProductScreen} from "@point_of_sale/app/screens/product_screen/product_screen";
import {unaccent} from "@web/core/utils/strings";

const _flexCacheKey = Symbol("flexSearchCacheKey");
const _flexCacheVal = Symbol("flexSearchCacheVal");
const hayByProduct = new WeakMap();

/** Minimum character threshold from pos.config (fallback 5). */
function configMinChars(pos) {
    const raw =
        pos.config?.pos_product_search_min_chars ??
        pos.config?.raw?.pos_product_search_min_chars;
    const n = Number(raw);
    if (!Number.isFinite(n) || n < 0) {
        return 5;
    }
    return n;
}

/** Lowercased unaccented whitespace-separated tokens (non-empty). */
function tokenize(searchWord) {
    return unaccent(searchWord.toLowerCase(), false)
        .trim()
        .split(/\s+/)
        .filter(Boolean);
}

/**
 * Case-insensitive RegExp: punctuation softened to ".", spaces to ".+" (ordered).
 * Built once per query, not per product.
 */
function flexibleSearchPattern(normalizedQuery) {
    if (!queryHasFlexiblePunctuation(normalizedQuery) && !normalizedQuery.includes(" ")) {
        return null;
    }
    try {
        let query = normalizedQuery.replace(
            /[\[\]\(\)\+\*\?\.\-\!\&\^\$\|\~\_\{\}\:\,\\\/]/g,
            "."
        );
        query = query.replace(/ +/g, ".+");
        return new RegExp(query, "i");
    } catch {
        return null;
    }
}

function queryHasFlexiblePunctuation(query) {
    return /[\[\]()+\*\?.\-!&|^$~_{}:,\\/]/.test(query);
}

/** Cached unaccented lowercase searchString (same idea as Odoo PR 241668 / Tecnativa #266039). */
function getHay(product) {
    const src = product.searchString || "";
    let entry = hayByProduct.get(product);
    if (!entry || entry.src !== src) {
        entry = {src, hay: unaccent(src, false).toLowerCase()};
        hayByProduct.set(product, entry);
    }
    return entry.hay;
}

function allTokensInHay(tokensLongFirst, hay) {
    for (let i = 0; i < tokensLongFirst.length; i++) {
        if (!hay.includes(tokensLongFirst[i])) {
            return false;
        }
    }
    return true;
}

function minTokenIndex(tokens, hay) {
    let best = Number.MAX_SAFE_INTEGER;
    for (let i = 0; i < tokens.length; i++) {
        const idx = hay.indexOf(tokens[i]);
        if (idx !== -1 && idx < best) {
            best = idx;
        }
    }
    return best;
}

/** Product.template sequence (lower first). Missing value sorts like 1000. */
function sequenceValue(product) {
    const raw = product.sequence ?? product.raw?.sequence;
    const n = Number(raw);
    return Number.isFinite(n) ? n : 1000;
}

/**
 * Server domain for Search more: every token must match name, default_code or
 * barcode (AND of ORs). Unlike core, spaces are not a single contiguous ILIKE.
 */
function tokenSearchDomain(searchProductWord) {
    const tokens = (searchProductWord || "").trim().split(/\s+/).filter(Boolean);
    const domain = [];
    for (const token of tokens) {
        domain.push(
            "|",
            "|",
            ["name", "ilike", token],
            ["default_code", "ilike", token],
            ["barcode", "ilike", token]
        );
    }
    domain.push(["available_in_pos", "=", true], ["sale_ok", "=", true]);
    return domain;
}

patch(ProductScreen.prototype, {
    /** Same trimmed text as the search box once `pos_product_search_min_chars` is reached. */
    get searchWord() {
        const raw = (this.pos.searchProductWord || "").trim();
        const minLen = configMinChars(this.pos);
        if (raw.length < minLen) {
            return "";
        }
        return raw;
    },

    getProductsBySearchWord(searchWord) {
        const products = this.products;
        const cacheKey = `${searchWord}\x1e${products.length}`;
        if (this[_flexCacheKey] === cacheKey && this[_flexCacheVal]) {
            return this[_flexCacheVal];
        }

        const tokens = tokenize(searchWord);
        if (tokens.length === 0) {
            this[_flexCacheKey] = cacheKey;
            this[_flexCacheVal] = products;
            return products;
        }

        const tokensLongFirst = tokens.slice().sort((a, b) => b.length - a.length);
        const normalizedQuery = unaccent(searchWord.toLowerCase(), false).trim();
        const re = tokens.length === 1 ? flexibleSearchPattern(normalizedQuery) : null;

        const scored = [];
        for (let i = 0; i < products.length; i++) {
            const product = products[i];
            const hay = getHay(product);
            let score = Number.MAX_SAFE_INTEGER;
            let ok = false;

            if (tokens.length >= 2) {
                if (allTokensInHay(tokensLongFirst, hay)) {
                    ok = true;
                    score = minTokenIndex(tokens, hay);
                }
            } else if (re) {
                const j = hay.search(re);
                if (j !== -1) {
                    ok = true;
                    score = j;
                }
            } else {
                const j = hay.indexOf(tokens[0]);
                if (j !== -1) {
                    ok = true;
                    score = j;
                }
            }

            if (!ok) {
                continue;
            }
            scored.push({
                product,
                score,
                seq: sequenceValue(product),
                hay,
            });
        }

        scored.sort((a, b) => {
            if (a.score !== b.score) {
                return a.score - b.score;
            }
            if (a.seq !== b.seq) {
                return a.seq - b.seq;
            }
            if (a.hay < b.hay) {
                return -1;
            }
            if (a.hay > b.hay) {
                return 1;
            }
            return 0;
        });

        const result = scored.map((row) => row.product);
        this[_flexCacheKey] = cacheKey;
        this[_flexCacheVal] = result;
        return result;
    },

    loadProductFromDBDomain(searchProductWord) {
        return tokenSearchDomain(searchProductWord);
    },
});
