Retail tickets with long product names (reference + attributes) wrap to two
bold lines plus a quantity row, so a 20-line order becomes a very long slip.
The core POS also prints a huge tracking number (``007``) and leaves extra
vertical gaps in the footer (``<br/>`` plus ``<p>`` margins around
"Powered by Odoo").

This module compacts the **printed / preview ticket** of that POS. It does
**not** change the cashier cart, and it does **not** rewrite the header
identity (logo, shop name, Spanish simplified invoice).

## Dependency

``depends`` is only ``point_of_sale``. There is no dependency on
``pos_config_logo``, ``pos_config_shop_identity``,
``l10n_es_pos_config_shop_identity`` or ``l10n_es_pos_oca``. Those addons
may be installed together; this module does not inherit their templates.

## OWL templates inherited

Only two core QWeb/OWL templates, both ``t-inherit-mode="extension"``
(xpath, not a full replace of the receipt).

``point_of_sale.OrderReceipt``
(``static/src/xml/order_receipt.xml``):

- Target: root ``div.pos-receipt``.
- Change: add ``t-att-class="compactReceiptClass"``.
- Why: CSS classes ``o_rcpt_header_*``, ``o_rcpt_track_*``,
  ``o_rcpt_lines_*``, ``o_rcpt_totals_*``, ``o_rcpt_footer_*`` are applied
  per POS settings. The footer XML ("Powered by Odoo", order name, date)
  is **not** replaced, so the core Spanish translation stays
  ("Con la tecnología de Odoo"). The visual gap is closed in SCSS.

``point_of_sale.Orderline``
(``static/src/xml/orderline.xml``):

- Target: ``li.price-per-unit`` (the ``1.00 x price / Unit`` row).
- Change: ``t-if="!line.hideQtyBreakdown"``.
- Why: hide that row when quantity is 1. The flag is set only in
  ``export_for_printing``, so the **cart** still shows the qty line
  (``hideQtyBreakdown`` is unset there).

``point_of_sale.ReceiptHeader`` is **not** inherited. Tracking number and
header font size are CSS under ``.pos-receipt`` (``.tracking-number``,
``.pos-receipt-contact``) so logo / shop identity / simplified-invoice
modules keep their own xpaths.

## Backend views

``point_of_sale.res_config_settings_view_form``
(``views/res_config_settings_views.xml``):

- Inserts the *Compact ticket* setting block inside
  ``pos_bills_and_receipts_section``.
- Why: per-POS font sizes and the "hide qty when 1" checkbox, without a
  dedicated ``pos.config`` form.

## JavaScript patches

``static/src/js/receipt_compact.esm.js``:

- ``PosOrder.export_for_printing``: after ``super``, attach
  ``compactReceipt`` from ``this.config``, truncate each printed
  ``productName`` to 60 characters (fallback), and set
  ``hideQtyBreakdown`` when ``|qty| ≈ 1``. Cart ``getDisplayData()``
  is not patched.
- ``OrderReceipt``: getter ``compactReceiptClass`` for the root CSS
  classes.
- ``Orderline.props``: optional ``line.hideQtyBreakdown`` so OWL accepts
  the extra key on receipt lines.

## CSS (no extra templates)

``static/src/scss/receipt_compact.scss``, scoped to ``.pos-receipt`` so
the cart is untouched:

- Tighter padding; hide direct-child ``<br/>`` (header/footer gaps).
  Does **not** style ``.pos-receipt-logo`` (that is ``pos_config_logo``).
- Footer last block: zero ``<p>`` margin so "Powered by Odoo" sits next
  to the order name/date.
- ``.receipt-total`` font-weight 700 (TOTAL in bold).
- Product name stays on one line: ``min-width: 0`` on ``.product-name``,
  ``flex-shrink: 0`` on ``.product-price``, and ``white-space: nowrap
  !important`` on the inner ``.text-wrap`` (core Orderline uses
  Bootstrap ``text-wrap``, which otherwise wraps onto two lines).
- Font sizes from the ``o_rcpt_*`` classes; tracking uses ``rem`` and
  ``!important`` to override Bootstrap ``fs-1`` and the self-order
  ``font-size: 100px`` inline style.

## Models

``pos.config`` fields (loaded into the POS via ``_load_pos_data_fields``):
``receipt_font_header``, ``receipt_font_tracking``, ``receipt_font_lines``,
``receipt_font_totals``, ``receipt_font_footer``, ``receipt_hide_unit_qty``.
``res.config.settings`` exposes them as related fields.
