Install the module. **Depends only on** ``point_of_sale``. Independent from
``pos_config_logo``, ``pos_config_shop_identity`` and
``l10n_es_pos_config_shop_identity`` (compatible if they are installed; no
manifest dependency).

In *Point of Sale → Configuration → Settings → Bills & Receipts → Compact
ticket*, pick a size per section:

- Header (shop name / address in ``.pos-receipt-contact``)
- Order number (core ``.tracking-number``, e.g. 007); can be Hidden
- Product lines
- Totals (including the bold TOTAL line)
- Footer (Powered by Odoo, order name, date)

Enable **Hide qty when 1** to drop the unit-price breakdown on single-unit
lines (on by default). After changing values, close and reopen the POS so
the client reloads ``pos.config``.
