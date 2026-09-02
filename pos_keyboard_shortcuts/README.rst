======================
POS keyboard shortcuts
======================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :target: https://odoo-community.org/page/development-status
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpos-lightgray.png?logo=github
    :target: https://github.com/OCA/pos/tree/18.0/pos_keyboard_shortcuts
    :alt: OCA/pos

|badge1| |badge2| |badge3|

**Table of contents**

.. contents::
   :local:

Description
===========

Configurable cashier keyboard shortcuts for the Odoo 18 Point of Sale. The key
map is global (POS administrators only). Each shop can enable or disable
shortcuts.

**Search hold.** After a search, the cashier often adds one product and still
needs another card from the same results. If the filter is cleared at once,
those cards vanish. If the search box keeps focus, a barcode scan is typed
into the box instead of adding the scanned product. The hold keeps the
filter for a few seconds and unfocuses the box, then clears the search. It
can be Off / 5 / 10 seconds. Off leaves the native search. The hold also
stays off when shortcuts are disabled on that shop.

**Payments.** **E** and **T** follow the journal type on *that* shop: first
cash method, first bank method. Extra methods need their own row (letter +
payment method). The map is global; only methods assigned to that Point of
Sale show a badge and accept the key. The same letter may be reused on two
methods that never share a shop.


Configuration
=============

**Settings → Point of Sale**, select the shop, **PoS Interface**:

* **Keyboard shortcuts**: enable or disable shortcuts on that shop.
* **Keep search filter**: Off, 5 or 10 seconds (global). Keeps the filter
  so a second match can be tapped, and unfocuses the box so the barcode
  scanner is not captured. Off leaves the native search. The hold also
  stays off when shortcuts are disabled on that shop.
* **Configure shortcut keys** (POS manager): one letter per action,
  case-insensitive. The same letter may be reused on another screen (for
  example **T** = tickets on products, **T** = first bank method on
  payment). Digits and native POS keys (numpad, Enter, Escape, arrows)
  cannot be assigned.
* **E** / **T** are the first cash / first bank method of *that* shop.
  Add a row **Specific payment method** for any extra method. The badge
  only appears on shops that use that method. The same letter may be
  reused on two extra methods that never share a shop.

The same enable flag is on **Point of Sale → Configuration → Point of Sales**.

Usage
=====

Open a POS session with shortcuts enabled. Press **H** for the in-session list
(read-only).

On the product screen, letters run actions when the cursor is **not** in an
input. **B** focuses product search. After you add a product from the results,
the box loses focus (scanner works) and the filter stays 5 or 10 seconds if
the hold is not Off, then it is cleared; **Esc** clears it immediately.

On payment, **C** is customer, **F** toggles invoice, **E** is the first cash
method of that shop, **T** is the first bank method of that shop, **Enter**
validates, **Esc** goes back. Extra methods only show their letter on shops
that have them configured.

On the receipt screen, **I** prints the full receipt, **B** the basic receipt
(if enabled), and **Enter** starts a new order.

Actions that cannot run (no selected line, missing ``pos_discount``, no fiscal
positions, and so on) show a top-right notification and do not block the
cashier or the scanner.

**Ctrl+Alt+C** (default, configurable) cancels the current order, using the
native confirmation when the ticket is not empty.

Default letters (product screen)
================================

* **B** search, **C** customer, **D** line discount, **P** line price, **Q**
  quantity, **G** global discount (``pos_discount``), **T** tickets, **R**
  refund, **L** pricelist, **I** fiscal position, **N** note, **X** remove
  line, **H** help.

Fixed keys: arrows select lines, Enter pays, Esc clears search.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/pos/issues>`_.

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
`OCA/pos <https://github.com/OCA/pos/tree/18.0/pos_keyboard_shortcuts>`__
repository on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.

Changelog
=========

See ``readme/HISTORY.md``.
