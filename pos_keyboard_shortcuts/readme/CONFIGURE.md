**Settings → Point of Sale**, select the shop, **PoS Interface**:

- **Keyboard shortcuts**: enable or disable shortcuts on that shop.
- **Keep search filter**: Off, 5 or 10 seconds (**global**). This exists so
  the cashier can tap a second match after adding one product, without
  leaving the search box focused (a focused box would capture the barcode
  scanner). After the delay the filter and the box are cleared. **Off**
  leaves the native POS search (no blur, no delayed clear). The hold also
  stays off when shortcuts are disabled on that shop.
- **Configure shortcut keys** (POS manager): one letter per action,
  case-insensitive. The same letter may be reused on another screen (for
  example **T** = tickets on products, **T** = first bank method on
  payment). Digits and native POS keys (numpad, Enter, Escape, arrows)
  cannot be assigned.

**Default payment keys (by type on that shop)**

- **E** (`pay_cash`): first method whose journal type is cash.
- **T** (`pay_bank`): first method whose journal type is bank.

A shop with no cash method does not charge anything with **E** (a
notification is shown). A second bank method has no letter until you add
it.

**Extra payment rows**

Add a line with action **Specific payment method**, pick the method, and
set a letter. Example: POS 1 has cash + card + an extra bank method; add a
row for that extra method (for example **Z**). POS 2 without that method
does not show **Z** and the key does nothing there.

If POS 1 and POS 2 each have their own extra method, both rows may use
**Z** as long as the methods are not assigned to the same shop. If one
method is shared by both shops, one row is enough.

The same enable flag is on **Point of Sale → Configuration → Point of
Sales**.
