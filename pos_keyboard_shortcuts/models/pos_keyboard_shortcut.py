# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

RESERVED_KEYS = frozenset(
    {
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        ".",
        ",",
        "+",
        "-",
        "backspace",
        "delete",
        "enter",
        "escape",
        "esc",
        "tab",
        "space",
        "arrowup",
        "arrowdown",
        "arrowleft",
        "arrowright",
    }
)

ACTION_SELECTION = [
    ("search", "Focus product search"),
    ("customer", "Customer"),
    ("discount_line", "Line discount mode"),
    ("price", "Line price mode"),
    ("quantity", "Quantity mode"),
    ("discount_global", "Global discount"),
    ("tickets", "Orders / tickets"),
    ("refund", "Refund"),
    ("pricelist", "Pricelist"),
    ("fiscal", "Fiscal position"),
    ("note", "Line / order note"),
    ("remove_line", "Remove selected line"),
    ("help", "Show shortcut help"),
    ("cancel_order", "Cancel current order"),
    ("pay_cash", "Cash payment"),
    ("pay_bank", "Card / bank payment"),
    ("pay_method", "Specific payment method"),
    ("invoice", "Toggle invoice"),
    ("print_receipt", "Print full receipt"),
    ("print_basic", "Print basic receipt"),
]


class PosKeyboardShortcut(models.Model):
    _name = "pos.keyboard.shortcut"
    _description = "POS keyboard shortcut"
    _inherit = ["pos.load.mixin"]
    _order = "sequence, id"

    name = fields.Char(compute="_compute_name", store=True)
    action = fields.Selection(
        ACTION_SELECTION,
        required=True,
        index=True,
        default="pay_method",
    )
    key = fields.Char(
        required=True,
        size=20,
        help="Letter or named key. Case is ignored. Digits and POS numpad keys " "cannot be used.",
    )
    ctrl = fields.Boolean(string="Ctrl")
    alt = fields.Boolean(string="Alt")
    shift = fields.Boolean(string="Shift")
    scope = fields.Selection(
        [
            ("product", "Product screen"),
            ("payment", "Payment screen"),
            ("receipt", "Receipt screen"),
            ("global", "All screens"),
        ],
        required=True,
        default="product",
    )
    sequence = fields.Integer(default=10)
    payment_method_id = fields.Many2one(
        "pos.payment.method",
        string="Payment method",
        ondelete="cascade",
        help="Extra payment shortcut (second card, instant-transfer method, "
        "and so on). The letter is only shown on shops that use this method. "
        "E and T remain the first cash / first bank method of each shop.",
    )
    is_builtin = fields.Boolean(compute="_compute_is_builtin")

    _sql_constraints = [
        (
            "payment_method_uniq",
            "unique(payment_method_id)",
            "Each payment method can only have one extra shortcut.",
        ),
    ]

    @api.depends("action")
    def _compute_is_builtin(self):
        for rec in self:
            rec.is_builtin = bool(rec._origin.id) and rec.action != "pay_method"

    @api.depends("action", "key", "ctrl", "alt", "shift", "payment_method_id")
    def _compute_name(self):
        action_labels = dict(self._fields["action"].selection)
        for rec in self:
            action_name = action_labels.get(rec.action) or rec.action or ""
            if rec.action == "pay_method" and rec.payment_method_id:
                action_name = rec.payment_method_id.display_name
            rec.name = "%s (%s)" % (action_name, rec.display_hotkey())

    def display_hotkey(self):
        self.ensure_one()
        parts = []
        if self.ctrl:
            parts.append("Ctrl")
        if self.alt:
            parts.append("Alt")
        if self.shift:
            parts.append("Shift")
        parts.append((self.key or "").strip().upper())
        return "+".join(parts)

    def _normalized_key(self):
        self.ensure_one()
        return (self.key or "").strip().lower()

    def _combo_tuple(self):
        self.ensure_one()
        return (self._normalized_key(), bool(self.ctrl), bool(self.alt), bool(self.shift))

    @api.constrains("key")
    def _check_reserved_key(self):
        for rec in self:
            key = rec._normalized_key()
            if not key:
                raise ValidationError(_("A shortcut key is required."))
            if key in RESERVED_KEYS:
                raise ValidationError(
                    _(
                        "The key '%(key)s' is reserved by the Point of Sale "
                        "(numpad, barcode buffer, Enter/Escape/arrows)."
                    )
                    % {"key": rec.key}
                )

    @api.constrains("action")
    def _check_action_unique(self):
        for rec in self:
            if rec.action == "pay_method":
                continue
            domain = [("action", "=", rec.action)]
            if rec.id:
                domain.append(("id", "!=", rec.id))
            if self.search_count(domain):
                raise ValidationError(_("Each POS shortcut action can only be defined once."))

    @api.constrains("action", "payment_method_id")
    def _check_payment_method_action(self):
        for rec in self:
            if rec.action == "pay_method":
                if not rec.payment_method_id:
                    raise ValidationError(_("A payment method is required for this shortcut."))
            elif rec.payment_method_id:
                raise ValidationError(_("Only extra payment shortcuts can be linked to a method."))

    def _pos_config_ids(self):
        self.ensure_one()
        return set(self.payment_method_id.config_ids.ids)

    def _same_key_allowed(self, other):
        """Same letter is OK when extras never appear on the same shop."""
        self.ensure_one()
        if self.action != "pay_method" or other.action != "pay_method":
            return False
        if not self.payment_method_id or not other.payment_method_id:
            return False
        configs_self = self._pos_config_ids()
        configs_other = other._pos_config_ids()
        if not configs_self or not configs_other:
            return True
        return not (configs_self & configs_other)

    @api.constrains("action", "key", "ctrl", "alt", "shift", "scope", "payment_method_id")
    def _check_duplicate_combo(self):
        all_recs = self.search([])
        by_id = {r.id: r for r in all_recs}
        for rec in self:
            combo = rec._combo_tuple()
            for other in all_recs:
                if other.id == rec.id:
                    continue
                if other._combo_tuple() != combo:
                    continue
                same_screen = (
                    rec.scope == "global" or other.scope == "global" or rec.scope == other.scope
                )
                if not same_screen:
                    continue
                if rec._same_key_allowed(other):
                    continue
                raise ValidationError(
                    _(
                        "Shortcut %(combo)s is already used by '%(other)s'. "
                        "The same combination cannot be used twice on the same "
                        "screen (or as a global shortcut)."
                    )
                    % {
                        "combo": rec.display_hotkey(),
                        "other": by_id[other.id].name or other.action,
                    }
                )

    @api.ondelete(at_uninstall=False)
    def _unlink_only_pay_method(self):
        for rec in self:
            if rec.action != "pay_method":
                raise UserError(_("Only extra payment shortcuts can be deleted."))

    @api.onchange("action")
    def _onchange_action_pay_method(self):
        if self.action == "pay_method":
            self.scope = "payment"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("action") == "pay_method":
                vals.setdefault("scope", "payment")
        return super().create(vals_list)

    @api.model
    def _load_pos_data_domain(self, data):
        return []

    @api.model
    def _load_pos_data_fields(self, config_id):
        return [
            "id",
            "action",
            "key",
            "ctrl",
            "alt",
            "shift",
            "scope",
            "sequence",
            "payment_method_id",
        ]
