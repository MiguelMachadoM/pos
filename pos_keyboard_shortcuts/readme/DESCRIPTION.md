Configurable cashier keyboard shortcuts for the Odoo 18 Point of Sale. The key
map is global (POS administrators only). Each shop can enable or disable
shortcuts.

**Search hold.** After a search, the cashier often adds one product and still
needs another card from the same results (two similar items). If the filter
is cleared at once, those cards vanish. If the search box keeps focus, a
barcode scan is typed into the box instead of adding the scanned product.
The hold therefore keeps the filter for a few seconds (so another result can
be tapped) and unfocuses the box (so the scanner works), then clears the
search. It can be set to Off / 5 / 10 seconds. Off leaves the native search.
The hold also stays off when shortcuts are disabled on that shop.

**Payments.** **E** and **T** follow the journal type on *that* shop: first
cash method, first bank method. Display names do not matter. Extra methods
(a second card, an instant-transfer method, and so on) need their own row:
a letter plus a payment method. The map is global; at runtime only methods
assigned to that Point of Sale show a badge and accept the key. The same
letter may be reused on two methods that never share a shop.
