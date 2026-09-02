# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestPosKeyboardShortcuts(TransactionCase):
    def test_pos_config_fields(self):
        self.assertIn("iface_keyboard_shortcuts", self.env["pos.config"]._fields)
        self.assertIn("keyboard_search_hold_seconds", self.env["pos.config"]._fields)

    def test_default_shortcuts_loaded(self):
        shortcuts = self.env["pos.keyboard.shortcut"].search([])
        self.assertTrue(shortcuts)
        actions = set(shortcuts.mapped("action"))
        self.assertIn("search", actions)
        self.assertIn("discount_line", actions)
        self.assertIn("fiscal", actions)
        self.assertIn("pay_cash", actions)
        self.assertIn("invoice", actions)
        self.assertIn("print_basic", actions)

    def test_reserved_key_rejected(self):
        rec = self.env["pos.keyboard.shortcut"].search([("action", "=", "search")], limit=1)
        with self.assertRaises(ValidationError):
            rec.write({"key": "5"})

    def test_duplicate_combo_same_scope(self):
        search = self.env["pos.keyboard.shortcut"].search(
            [("action", "=", "search")], limit=1
        )
        customer = self.env["pos.keyboard.shortcut"].search(
            [("action", "=", "customer")], limit=1
        )
        with self.assertRaises(ValidationError):
            customer.write({"key": search.key, "ctrl": False, "alt": False, "shift": False})

    def test_same_letter_different_scope_allowed(self):
        tickets = self.env["pos.keyboard.shortcut"].search(
            [("action", "=", "tickets")], limit=1
        )
        pay_bank = self.env["pos.keyboard.shortcut"].search(
            [("action", "=", "pay_bank")], limit=1
        )
        self.assertEqual(tickets.key, pay_bank.key)
        self.assertNotEqual(tickets.scope, pay_bank.scope)

    def test_search_hold_seconds_accepts_off(self):
        ICP = self.env["ir.config_parameter"].sudo()
        config = self.env["pos.config"].search([], limit=1)
        if not config:
            self.skipTest("No pos.config")
        ICP.set_param("pos_keyboard_shortcuts.search_hold_seconds", "0")
        config.invalidate_recordset(["keyboard_search_hold_seconds"])
        self.assertEqual(config.keyboard_search_hold_seconds, 0)
        ICP.set_param("pos_keyboard_shortcuts.search_hold_seconds", "7")
        config.invalidate_recordset(["keyboard_search_hold_seconds"])
        self.assertEqual(config.keyboard_search_hold_seconds, 5)

    def test_session_loads_shortcut_model(self):
        session = self.env["pos.session"]
        config = self.env["pos.config"].search([], limit=1)
        if not config:
            self.skipTest("No pos.config")
        models = session._load_pos_data_models(config.id)
        self.assertIn("pos.keyboard.shortcut", models)

    def _bank_journal(self):
        journal = self.env["account.journal"].search([("type", "=", "bank")], limit=1)
        if not journal:
            self.skipTest("No bank journal")
        return journal

    def test_extra_payment_shortcut(self):
        method = self.env["pos.payment.method"].create(
            {"name": "Bizum Shop 1", "journal_id": self._bank_journal().id}
        )
        rec = self.env["pos.keyboard.shortcut"].create(
            {
                "action": "pay_method",
                "key": "z",
                "payment_method_id": method.id,
            }
        )
        self.assertEqual(rec.scope, "payment")

    def test_cannot_unlink_builtin(self):
        rec = self.env["pos.keyboard.shortcut"].search(
            [("action", "=", "pay_cash")], limit=1
        )
        with self.assertRaises(UserError):
            rec.unlink()

    def test_pay_method_requires_method(self):
        with self.assertRaises(ValidationError):
            self.env["pos.keyboard.shortcut"].create(
                {"action": "pay_method", "key": "z"}
            )

    def test_same_letter_disjoint_payment_methods(self):
        configs = self.env["pos.config"].search([], limit=2)
        if len(configs) < 2:
            self.skipTest("Need two POS configs")
        journal = self._bank_journal()
        method1 = self.env["pos.payment.method"].create(
            {
                "name": "Bizum Shop 1",
                "journal_id": journal.id,
                "config_ids": [(6, 0, [configs[0].id])],
            }
        )
        method2 = self.env["pos.payment.method"].create(
            {
                "name": "Bizum Shop 2",
                "journal_id": journal.id,
                "config_ids": [(6, 0, [configs[1].id])],
            }
        )
        self.env["pos.keyboard.shortcut"].create(
            {"action": "pay_method", "key": "z", "payment_method_id": method1.id}
        )
        extra = self.env["pos.keyboard.shortcut"].create(
            {"action": "pay_method", "key": "z", "payment_method_id": method2.id}
        )
        self.assertEqual(extra.key, "z")

    def test_same_letter_overlapping_payment_methods(self):
        config = self.env["pos.config"].search([], limit=1)
        if not config:
            self.skipTest("No pos.config")
        journal = self._bank_journal()
        method1 = self.env["pos.payment.method"].create(
            {
                "name": "Card A",
                "journal_id": journal.id,
                "config_ids": [(6, 0, [config.id])],
            }
        )
        method2 = self.env["pos.payment.method"].create(
            {
                "name": "Card B",
                "journal_id": journal.id,
                "config_ids": [(6, 0, [config.id])],
            }
        )
        self.env["pos.keyboard.shortcut"].create(
            {"action": "pay_method", "key": "z", "payment_method_id": method1.id}
        )
        with self.assertRaises(ValidationError):
            self.env["pos.keyboard.shortcut"].create(
                {"action": "pay_method", "key": "z", "payment_method_id": method2.id}
            )
