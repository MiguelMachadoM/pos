/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

/**
 * Read shortcut records loaded into the POS and turn them into hotkey strings
 * matching Odoo web (`alt` then `control` then `shift` then the key).
 */

export function shortcutsEnabled(pos) {
    return Boolean(pos?.config?.iface_keyboard_shortcuts);
}

export function shortcutRecords(pos) {
    const records = pos?.models?.["pos.keyboard.shortcut"]?.getAll?.() || [];
    return records.slice().sort((a, b) => (a.sequence || 0) - (b.sequence || 0));
}

export function getShortcut(pos, action) {
    return shortcutRecords(pos).find((rec) => rec.action === action) || null;
}

export function toHotkeyString(rec) {
    if (!rec?.key) {
        return "";
    }
    const parts = [];
    // Same order as getActiveHotkey() on Windows/Linux (alt, control, shift, key).
    if (rec.alt) {
        parts.push("alt");
    }
    if (rec.ctrl) {
        parts.push("control");
    }
    if (rec.shift) {
        parts.push("shift");
    }
    parts.push(String(rec.key).trim().toLowerCase());
    return parts.join("+");
}

export function formatShortcutLabel(rec) {
    if (!rec?.key) {
        return "";
    }
    const parts = [];
    if (rec.ctrl) {
        parts.push("Ctrl");
    }
    if (rec.alt) {
        parts.push("Alt");
    }
    if (rec.shift) {
        parts.push("Shift");
    }
    parts.push(String(rec.key).trim().toUpperCase());
    return parts.join("+");
}

export function shortcutLabel(pos, action) {
    return formatShortcutLabel(getShortcut(pos, action));
}

export function extraPaymentShortcuts(pos) {
    return shortcutRecords(pos).filter((rec) => rec.action === "pay_method");
}

export function paymentMethodId(value) {
    if (!value) {
        return 0;
    }
    if (typeof value === "object") {
        return value.id || 0;
    }
    return value;
}

export function searchHoldSeconds(pos) {
    const raw = pos?.config?.keyboard_search_hold_seconds;
    const n = Number(raw);
    if (n === 0 || n === 10) {
        return n;
    }
    return 5;
}

export function isTextInput(el) {
    if (!el) {
        return false;
    }
    const tag = (el.tagName || "").toUpperCase();
    if (tag === "TEXTAREA") {
        return true;
    }
    if (tag === "INPUT") {
        const type = (el.type || "text").toLowerCase();
        return !["button", "checkbox", "radio", "file", "hidden", "reset", "submit"].includes(
            type
        );
    }
    return Boolean(el.isContentEditable);
}

export function isProductSearchInput(el) {
    if (!el || (el.tagName || "").toUpperCase() !== "INPUT") {
        return false;
    }
    return Boolean(el.closest(".pos-rightheader, .pos-topheader"));
}
