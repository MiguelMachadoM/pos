# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_shop_identity_enabled = fields.Boolean(
        related="pos_config_id.shop_identity_enabled",
        readonly=False,
    )
    pos_shop_identity_name = fields.Char(
        related="pos_config_id.shop_identity_name",
        readonly=False,
    )
    pos_shop_identity_street = fields.Char(
        related="pos_config_id.shop_identity_street",
        readonly=False,
    )
    pos_shop_identity_street2 = fields.Char(
        related="pos_config_id.shop_identity_street2",
        readonly=False,
    )
    pos_shop_identity_zip_id = fields.Many2one(
        related="pos_config_id.shop_identity_zip_id",
        readonly=False,
    )
    pos_shop_identity_zip = fields.Char(
        related="pos_config_id.shop_identity_zip",
        readonly=False,
    )
    pos_shop_identity_city = fields.Char(
        related="pos_config_id.shop_identity_city",
        readonly=False,
    )
    pos_shop_identity_state_id = fields.Many2one(
        related="pos_config_id.shop_identity_state_id",
        readonly=False,
    )
    pos_shop_identity_country_id = fields.Many2one(
        related="pos_config_id.shop_identity_country_id",
        readonly=False,
    )
    pos_shop_identity_phone = fields.Char(
        related="pos_config_id.shop_identity_phone",
        readonly=False,
    )
    pos_shop_identity_email = fields.Char(
        related="pos_config_id.shop_identity_email",
        readonly=False,
    )

    @api.onchange("pos_shop_identity_enabled")
    def _onchange_pos_shop_identity_enabled(self):
        if self.pos_shop_identity_enabled and not self.pos_shop_identity_country_id:
            self.pos_shop_identity_country_id = self.company_id.country_id

    @api.onchange("pos_shop_identity_zip_id")
    def _onchange_pos_shop_identity_zip_id(self):
        if self.pos_shop_identity_zip_id:
            zip_rec = self.pos_shop_identity_zip_id
            self.pos_shop_identity_zip = zip_rec.name
            self.pos_shop_identity_city = zip_rec.city_id.name
            self.pos_shop_identity_state_id = zip_rec.city_id.state_id
            self.pos_shop_identity_country_id = zip_rec.city_id.country_id
