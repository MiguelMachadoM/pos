To configure this module, you need to:

- Go to *Point of Sale > Configuration > Settings*
- Select the point of sale
- Enable *Custom ticket header identity*
- Fill in shop name, street, ZIP (search by code or city), city, province,
  phone and optional email

The ZIP field uses ``base_location`` locations. Example: type ``11204`` and
pick ``11204, Algeciras, Cádiz``; city and province fill in. Geonames / Spanish
toponyms must be imported in the database (``base_location_geonames_import``
and/or ``l10n_es_toponyms``).

VAT and website on the ticket stay those of the company. Empty shop fields
are omitted (they do not fall back to company name, address, phone or email).
The logo is unchanged; use `pos_config_logo` for that.

If the database uses Spanish POS (`l10n_es_pos_oca`), install
`pos_config_shop_identity_l10n_es` as well.
