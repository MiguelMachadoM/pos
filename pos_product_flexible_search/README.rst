===========================
POS product flexible search
===========================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpos-lightgray.png?logo=github
    :target: https://github.com/OCA/pos/tree/18.0/pos_product_flexible_search
    :alt: OCA/pos

|badge1| |badge2| |badge3|

**Table of contents**

.. contents::
   :local:

Description
===========

In Odoo 18 the Point of Sale filters products with a contiguous substring match on
``searchString``. This module relaxes that behaviour on the product screen:

* **Ordered tokens with gaps** (similar to older POS): spaces in the query become
  flexible gaps between words in order.
* **Unordered tokens** (two or more words): every word must appear somewhere in the
  product ``searchString``, in any order (substring match per word).
* **Search more** uses the same per-word rule on the server (``name``,
  ``default_code``, ``barcode``), so products not yet loaded in the session still
  appear.
* **Search ranking:** match quality, then product sequence (lower first), then name.

The filter runs on the **full POS product list** (``this.products``), not only the
current category.

On large catalogs the client caches a normalized haystack per product, tokenizes
the query once, and reuses the last result when the getter is read more than once.

The module does **not** define which fields are searched: it uses the same
``searchString`` getter as core and any other installed addons (see *Context*).

Configuration
=============

**Where (Odoo 18):** **Settings → Point of Sale** (company settings), pick a shop in
**Point of Sale** at the top, then open the **PoS Interface** block (same place as
**Log in with Employees**, **Hide pictures in POS**, OCA *Alternative point of sale logo*,
*Remove Order Line in POS*, etc.). There you will find **POS product search** with
**POS: minimum characters for product search** (default: 5). Use 0 to filter from the
first character (can be heavy on very large catalogs).

The value is stored on the selected ``pos.config`` record (same as other options on
that screen). It is also available on the legacy **Point of Sale → Configuration →
Point of Sales** form for the same shop, if you open that record directly.

The client-side filter starts only when the search box has at least this many characters.

Usage
=====

Open a POS session, go to the product screen and type in the product search box.
Multiple words may be in any order once the minimum character threshold is reached.

If a match is missing from the grid, use **Load more / Search more** (or Enter).
The server matches each word separately on name, internal reference and barcode,
not the whole phrase as one contiguous string. Results are ranked by match score,
then sequence (lower first), then name. Core POS already debounces the search box
(500 ms).

Context: ``searchString``
==========================

This addon only matches against ``product.product.searchString`` in the POS client.

**Core Odoo 18** builds it from ``display_name``, ``barcode`` and ``default_code``.

Other addons may **patch** that getter and append data (for example purchase seller
lines). A common pattern is OCA *pos_supplierinfo_search*, which adds supplier names;
the partner ``display_name`` often includes the commercial entity name, so tokens can
match even when they do not appear in the short product title.

If removing a vendor line from the product purchase tab changes search results, the
cause is the **extended ``searchString``**, not the flexible matching rules here.

**Grid sort:** ``pos_product_sort`` applies favorites / top-sales only when
browsing (no search text). It does not re-sort ``getProductsBySearchWord``.
Search hits are ordered by this module: match score, then ``sequence`` (lower
first), then name.

Other POS addons
================

``pos_product_sort`` only applies the configurable grid order when **browsing**
(no search text). Search results keep this module's ranking (match, sequence,
name); that addon does not re-sort ``getProductsBySearchWord``.

Other addons that still replace ``getProductsBySearchWord`` can override this
behaviour: the **last** patch in the POS asset bundle wins. To keep flexible search,
declare ``pos_product_flexible_search`` as a dependency of that module so it loads
after it, or merge the logic in one JS file.

Addons that extend ``searchString`` change **which text** is matched, independently of
this module.

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
`OCA/pos <https://github.com/OCA/pos/tree/18.0/pos_product_flexible_search>`__
repository on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

Changelog
=========

See ``readme/HISTORY.md``.
