.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpos-lightgray.png?logo=github
    :target: https://github.com/OCA/pos/tree/18.0/pos_config_shop_identity
    :alt: OCA/pos

|badge1| |badge2| |badge3|

POS shop identity on receipts
=============================

**Table of contents**

.. contents::
   :local:

Per POS commercial name, address, phone and email on the printed ticket
header, without changing the company (same VAT / NIF).

Depends on ``point_of_sale`` and OCA ``base_location`` (ZIP search fills
city and province). Independent from ``pos_config_logo`` (logos only).
Install both if each shop needs its own logo and its own header text.

Empty shop fields are omitted: they do not fall back to the company legal
name, address, phone or email. VAT / NIF and website stay those of the
company.

The header is compacted for thermal tickets: shop name slightly larger,
street/ZIP/city/province on one wrapping line, phone and email on one line
with small icons. Font sizes of that block can be tuned by
``pos_receipt_compact``.

Spanish simplified invoice (``Factura simplificada: number``) is a separate
glue addon: ``pos_config_shop_identity_l10n_es``.


Configuration
=============

Go to *Point of Sale > Configuration > Settings*, select the POS, enable
*Custom ticket header identity* and fill in the shop fields. Search the ZIP
field (for example ``11204``) to fill city and province.

Usage
=====

Open that POS, complete an order and print or display the receipt. The header
uses the shop identity of that configuration.

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
`OCA/pos <https://github.com/OCA/pos/tree/18.0/pos_config_shop_identity>`__
repository on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

Changelog
=========

See ``readme/HISTORY.md``.
