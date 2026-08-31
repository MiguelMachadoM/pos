# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, fields, models

_SHOP_IDENTITY_POS_FIELDS = [
    "shop_identity_enabled",
    "shop_identity_name",
    "shop_identity_street",
    "shop_identity_street2",
    "shop_identity_zip",
    "shop_identity_city",
    "shop_identity_state_name",
    "shop_identity_phone",
    "shop_identity_email",
]


class PosConfig(models.Model):
    _inherit = "pos.config"

    shop_identity_enabled = fields.Boolean(
        string="Custom ticket header identity",
        help="If enabled, this POS prints the shop name, address, phone and "
        "email below instead of the company ones. VAT and website stay "
        "those of the company.",
    )
    shop_identity_name = fields.Char(
        string="Shop name",
        help="Commercial name printed on the receipt header. Leave empty to "
        "hide the company legal name on this POS ticket.",
    )
    shop_identity_street = fields.Char(string="Street")
    shop_identity_street2 = fields.Char(string="Street 2")
    shop_identity_zip_id = fields.Many2one(
        "res.city.zip",
        string="ZIP Location",
        help="Type the ZIP or city name to fill city and state "
        "(for example 28001 → Madrid).",
    )
    shop_identity_zip = fields.Char(string="ZIP")
    shop_identity_city = fields.Char(string="City")
    shop_identity_state_id = fields.Many2one(
        "res.country.state",
        string="State",
        domain="[('country_id', '=?', shop_identity_country_id)]",
    )
    shop_identity_state_name = fields.Char(
        related="shop_identity_state_id.name",
        store=True,
    )
    shop_identity_country_id = fields.Many2one(
        "res.country",
        string="Country",
        default=lambda self: self.env.company.country_id,
    )
    shop_identity_phone = fields.Char(string="Phone")
    shop_identity_email = fields.Char(string="Email")

    @api.model
    def _shop_identity_vals_from_zip(self, zip_rec):
        if not zip_rec:
            return {}
        vals = {
            "shop_identity_zip": zip_rec.name or "",
            "shop_identity_city": zip_rec.city_id.name or "",
        }
        if zip_rec.city_id.state_id:
            vals["shop_identity_state_id"] = zip_rec.city_id.state_id.id
        if zip_rec.city_id.country_id:
            vals["shop_identity_country_id"] = zip_rec.city_id.country_id.id
        return vals

    @api.model
    def _inject_shop_identity_from_zip_id(self, vals):
        zip_id = vals.get("shop_identity_zip_id")
        if not zip_id:
            return vals
        zip_rec = self.env["res.city.zip"].browse(zip_id)
        extra = self._shop_identity_vals_from_zip(zip_rec)
        for key, value in extra.items():
            vals.setdefault(key, value)
        return vals

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._inject_shop_identity_from_zip_id(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._inject_shop_identity_from_zip_id(vals)
        return super().write(vals)

    @api.onchange("shop_identity_enabled")
    def _onchange_shop_identity_enabled(self):
        if self.shop_identity_enabled and not self.shop_identity_country_id:
            self.shop_identity_country_id = (
                self.company_id.country_id or self.env.company.country_id
            )

    @api.onchange("shop_identity_zip_id")
    def _onchange_shop_identity_zip_id(self):
        if self.shop_identity_zip_id:
            self.update(self._shop_identity_vals_from_zip(self.shop_identity_zip_id))

    @api.onchange("shop_identity_zip")
    def _onchange_shop_identity_zip(self):
        code = (self.shop_identity_zip or "").strip()
        if not code or self.shop_identity_zip_id:
            return
        country = self.shop_identity_country_id or self.env.company.country_id
        domain = [("name", "=", code)]
        if country:
            domain.append(("city_id.country_id", "=", country.id))
        matches = self.env["res.city.zip"].search(domain, limit=2)
        if len(matches) == 1:
            self.shop_identity_zip_id = matches
            self.update(self._shop_identity_vals_from_zip(matches))

    @api.model
    def _load_pos_data_fields(self, config_id):
        fields = super()._load_pos_data_fields(config_id)
        if not fields:
            fields = list(self._fields)
        else:
            fields = list(fields)
        for fname in _SHOP_IDENTITY_POS_FIELDS:
            if fname not in fields:
                fields.append(fname)
        return fields
