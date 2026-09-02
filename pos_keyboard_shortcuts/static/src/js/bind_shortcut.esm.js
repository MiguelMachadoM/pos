/** @odoo-module **/
/* Copyright 2026 Miguel Machado
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0). */

import {useHotkey} from "@web/core/hotkeys/hotkey_hook";
import {getShortcut, shortcutsEnabled, toHotkeyString} from "./keyboard_map.esm";

export function bindShortcutRecord(pos, rec, callback, options = {}) {
    const hotkey = toHotkeyString(rec);
    if (!hotkey) {
        return;
    }
    const userAvailable = options.isAvailable;
    useHotkey(hotkey, callback, {
        allowRepeat: options.allowRepeat,
        bypassEditableProtection: options.bypassEditableProtection,
        isAvailable: () => {
            if (!shortcutsEnabled(pos)) {
                return false;
            }
            return userAvailable ? userAvailable() : true;
        },
    });
}

export function bindShortcut(pos, action, callback, options = {}) {
    bindShortcutRecord(pos, getShortcut(pos, action), callback, options);
}

export function bindFixedHotkey(pos, hotkey, callback, options = {}) {
    const userAvailable = options.isAvailable;
    useHotkey(hotkey, callback, {
        allowRepeat: options.allowRepeat,
        bypassEditableProtection: options.bypassEditableProtection,
        isAvailable: () => {
            if (!shortcutsEnabled(pos)) {
                return false;
            }
            return userAvailable ? userAvailable() : true;
        },
    });
}
