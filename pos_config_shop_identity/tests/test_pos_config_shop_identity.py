# Copyright 2026 Miguel Machado
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl-3.0).

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestPosConfigShopIdentity(TransactionCase):
    def _make_config(self):
        config = self.env["pos.config"].search([], limit=1)
        if not config:
            config = self.env["pos.config"].create({"name": "Shop Identity Test"})
        return config

    def _make_cadiz_zip(self):
        country = self.env.ref("base.es")
        state = self.env["res.country.state"].search(
            [("country_id", "=", country.id), ("name", "ilike", "Cádiz")],
            limit=1,
        )
        if not state:
            state = self.env["res.country.state"].create(
                {
                    "name": "Cádiz",
                    "code": "CA",
                    "country_id": country.id,
                }
            )
        city = self.env["res.city"].search(
            [
                ("name", "=", "Algeciras"),
                ("country_id", "=", country.id),
                ("state_id", "=", state.id),
            ],
            limit=1,
        )
        if not city:
            city = self.env["res.city"].create(
                {
                    "name": "Algeciras",
                    "country_id": country.id,
                    "state_id": state.id,
                    "zipcode": "11204",
                }
            )
        zip_rec = self.env["res.city.zip"].search(
            [("name", "=", "11204"), ("city_id", "=", city.id)],
            limit=1,
        )
        if not zip_rec:
            zip_rec = self.env["res.city.zip"].create(
                {"name": "11204", "city_id": city.id}
            )
        return zip_rec

    def test_shop_identity_fields_stored_on_pos_config(self):
        config = self._make_config()
        config.write(
            {
                "shop_identity_enabled": True,
                "shop_identity_name": "Tienda Centro",
                "shop_identity_street": "Calle Mayor 1",
                "shop_identity_street2": "Local 3",
                "shop_identity_zip": "28013",
                "shop_identity_city": "Madrid",
                "shop_identity_phone": "911000000",
                "shop_identity_email": "centro@example.com",
            }
        )
        self.assertTrue(config.shop_identity_enabled)
        self.assertEqual(config.shop_identity_name, "Tienda Centro")
        self.assertEqual(config.shop_identity_city, "Madrid")

    def test_zip_id_fills_city_and_state(self):
        config = self._make_config()
        zip_rec = self._make_cadiz_zip()
        config.write({"shop_identity_zip_id": zip_rec.id})
        self.assertEqual(config.shop_identity_zip, "11204")
        self.assertEqual(config.shop_identity_city, "Algeciras")
        self.assertEqual(config.shop_identity_state_id, zip_rec.city_id.state_id)
        self.assertEqual(config.shop_identity_state_name, zip_rec.city_id.state_id.name)

    def test_load_pos_data_fields_include_shop_identity(self):
        config = self._make_config()
        fields = self.env["pos.config"]._load_pos_data_fields(config.id)
        self.assertIn("shop_identity_enabled", fields)
        self.assertIn("shop_identity_name", fields)
        self.assertIn("shop_identity_street", fields)
        self.assertIn("shop_identity_state_name", fields)
