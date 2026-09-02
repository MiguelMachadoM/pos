/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {searchHoldSeconds, shortcutsEnabled} from "./keyboard_map.esm";

let holdTimer = null;

export function getSearchInputEl() {
    return document.querySelector(".pos-topheader input, .pos-rightheader input");
}

export function blurProductSearch() {
    const el = getSearchInputEl();
    if (el && document.activeElement === el) {
        el.blur();
    }
}

export function focusProductSearch() {
    const el = getSearchInputEl();
    if (!el) {
        return;
    }
    el.focus();
    el.select();
}

function applySearchClear(pos) {
    pos.searchProductWord = "";
    const el = getSearchInputEl();
    if (!el) {
        return;
    }
    if (el.value) {
        el.value = "";
        el.dispatchEvent(new Event("input", {bubbles: true}));
    }
}

export function clearProductSearch(pos) {
    if (holdTimer) {
        clearTimeout(holdTimer);
        holdTimer = null;
    }
    applySearchClear(pos);
    blurProductSearch();
}

export function scheduleProductSearchClear(pos) {
    if (holdTimer) {
        clearTimeout(holdTimer);
    }
    const ms = searchHoldSeconds(pos) * 1000;
    holdTimer = setTimeout(() => {
        holdTimer = null;
        applySearchClear(pos);
        blurProductSearch();
    }, ms);
}

/**
 * Keep the current search filter so another matching product can be tapped,
 * but drop input focus so the barcode scanner is not captured by the box.
 * After the configured delay the filter and the search text are cleared.
 */
export function afterSearchProductAdded(pos) {
    if (!shortcutsEnabled(pos) || searchHoldSeconds(pos) <= 0) {
        return;
    }
    if (!(pos.searchProductWord || "").trim()) {
        return;
    }
    blurProductSearch();
    scheduleProductSearchClear(pos);
}
