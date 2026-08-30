===============================
PoS Product Card Image Overlay
===============================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpos-lightgray.png?logo=github
    :target: https://github.com/OCA/pos/tree/18.0/pos_product_card_overlay
    :alt: OCA/pos

|badge1| |badge2| |badge3|

**Table of contents**

.. contents::
   :local:

Description
===========

In the Odoo 18 Point of Sale product grid, products with an image use a short white
strip under the photo for the name (two lines). Long titles and internal references
are often truncated.

This module draws the label **on top of the image**: a semi-transparent dark band at
the bottom with white text, a smaller font, and the internal reference
(``default_code``) on its own line when present. On pointer hover (desktop), the band
grows upward over the image to show the full name without changing the card size in
the grid.

Products **without** an image keep the standard full-card text layout.

**Dependencies:** only ``point_of_sale``. The internal reference is rendered by this
addon from standard PoS ``default_code``, so it does **not** depend on
``pos_product_display_default_code``. If another addon prefixes the visible name with
``[CODE]``, that prefix is stripped on the overlay to avoid duplicating the reference.

When a product has a **PoS color** set on the template, the image area shows a colored
left bar and a thin frame around the photo (see changelog).

Configuration
=============

No configuration is required.

Install or upgrade the module from **Apps** (technical name:
``pos_product_card_overlay``). Product images and optional **Color** on the product
template (Point of Sale tab) work as in standard Odoo; this module only changes how
labels are rendered on image cards.

Usage
=====

Open a Point of Sale session and go to the product screen.

* Products **with** an image show the name and internal reference on the overlay band.
* Hover the card (desktop) to expand the band and read the full product name.
* Products **without** an image behave like standard Odoo PoS cards.

The module can coexist with other PoS addons (for example addons that show
``default_code`` on ticket or order lines) without changing their behaviour.

After code or asset changes, upgrade the module on the database and refresh the PoS
session so SCSS/JS assets reload.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/MiguelMachadoM/Odoo18-Addons/issues>`_.
Please check there whether your issue has already been reported.

Credits
=======

Authors
-------

* Miguel Machado
* Odoo Community Association (OCA)

Contributors
------------

* Miguel Machado <memachado@gmail.com>

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
`OCA/pos <https://github.com/OCA/pos/tree/18.0/pos_product_card_overlay>`__
repository on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

Changelog
=========

See ``readme/HISTORY.md``.
