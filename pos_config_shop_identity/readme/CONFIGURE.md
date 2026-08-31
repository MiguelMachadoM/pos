To configure this module, you need to:

- Go to *Point of Sale > Configuration > Settings*
- Select the point of sale
- Enable *Custom ticket header identity*
- Fill in shop name, street, ZIP (search by code or city), city, province,
  phone and optional email

The ZIP field uses ``base_location`` locations. Example: type ``28001`` and
pick ``28001, Madrid``; city and province fill in. Geonames / Spanish
toponyms must be imported in the database (``base_location_geonames_import``
and/or ``l10n_es_toponyms``).

VAT and website on the ticket stay those of the company. Empty shop fields
are omitted (they do not fall back to company name, address, phone or email).
The logo is unchanged; use `pos_config_logo` for that.

If the database uses Spanish POS (`l10n_es_pos_oca`), install
`l10n_es_pos_config_shop_identity` as well.
