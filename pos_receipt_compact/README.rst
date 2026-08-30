.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpos-lightgray.png?logo=github
    :target: https://github.com/OCA/pos/tree/18.0/pos_receipt_compact
    :alt: OCA/pos

|badge1| |badge2| |badge3|

POS compact receipt lines
=========================

**Table of contents**

.. contents::
   :local:

Shorter POS receipts: per-section font sizes, smaller order number, regular
(not bold) product names on one line (ellipsis; 60-character fallback) on the ticket only, no
qty breakdown when the quantity is 1, tighter padding, and a bold TOTAL.

**Depends only on** ``point_of_sale``. Compatible with ``pos_config_logo``,
``pos_config_shop_identity`` and ``l10n_es_pos_config_shop_identity``; it
does not depend on them and does not inherit their templates.

Does **not** change the cashier cart. Does **not** inherit
``point_of_sale.ReceiptHeader`` (header identity stays in the other addons).


Configuration
=============

In *Point of Sale → Configuration → Settings → Bills & Receipts → Compact
ticket*, set Small / Medium / Large for header, order number, product lines,
totals and footer. The order number can also be Hidden. Hide the unit-price
row when qty is 1 (default on). Reopen the POS after changing these values.

Usage
=====

Open the POS, complete an order and display or print the receipt.

Technical notes
===============

What is patched and why (full write-up: ``readme/CONTEXT.md``).

OWL inherits (extension / xpath only)
-------------------------------------

* ``point_of_sale.OrderReceipt``
  (``static/src/xml/order_receipt.xml``): add ``t-att-class`` on
  ``div.pos-receipt`` so per-section CSS classes can be applied. The
  footer nodes ("Powered by Odoo", order name, date) are **not**
  replaced, to keep the core translation.
* ``point_of_sale.Orderline``
  (``static/src/xml/orderline.xml``): ``t-if`` on ``li.price-per-unit``
  to hide ``1.00 x price / Unit`` when quantity is 1 on the **ticket**.

Backend view
------------

* ``point_of_sale.res_config_settings_view_form``
  (``views/res_config_settings_views.xml``): *Compact ticket* block in
  *Bills & Receipts*.

JavaScript (``static/src/js/receipt_compact.esm.js``)
-----------------------------------------------------

* ``PosOrder.export_for_printing``: truncate names to 60 chars (fallback)
  and set ``hideQtyBreakdown`` for printed lines only (cart uses
  ``getDisplayData()`` unchanged).
* ``OrderReceipt.compactReceiptClass``: CSS classes from ``pos.config``.
* ``Orderline.props``: optional ``hideQtyBreakdown``.

CSS (``static/src/scss/receipt_compact.scss``)
---------------------------------------------

Scoped to ``.pos-receipt``: padding, hide extra ``<br/>``, footer
``<p>`` margin, bold ``.receipt-total``, one-line product names
(override Bootstrap ``text-wrap`` so they ellipsize instead of wrapping),
font sizes including ``.tracking-number`` (overrides ``fs-1`` / 100px
without touching ``ReceiptHeader`` XML). Does **not** style
``.pos-receipt-logo`` (``pos_config_logo`` owns that).

Models
------

``pos.config`` fields ``receipt_font_*`` and ``receipt_hide_unit_qty``,
exposed on ``res.config.settings`` and included in
``_load_pos_data_fields``.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/pos/issues>`_.
Please check there whether your issue has already been reported.

Credits
=======

Authors
-------

* Miguel Machado
* Odoo Community Association (OCA)

Contributors
------------

* Miguel Machado

Maintainers
-----------

This module is maintained the same way as `OCA <https://odoo-community.org>`__ addons.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org
   :width: 80px

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-MiguelMachadoM| image:: https://github.com/MiguelMachadoM.png
    :width: 40px
    :height: 40px
    :target: https://github.com/MiguelMachadoM
    :alt: MiguelMachadoM

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-MiguelMachadoM|

This module is hosted in the
`OCA/pos <https://github.com/OCA/pos/tree/18.0/pos_receipt_compact>`__
repository on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

Changelog
=========

See ``readme/HISTORY.md``.
