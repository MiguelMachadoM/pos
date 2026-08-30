Shorter POS receipts: per-section font sizes, smaller order number, regular
(not bold) product names on one line (ellipsis; 60-character fallback), hidden
qty line when the quantity is 1, tighter padding, and a bold TOTAL.

Depends only on ``point_of_sale``. OWL inherits are limited to
``OrderReceipt`` (CSS classes on the root) and ``Orderline`` (optional hide
of the unit-price row on the ticket). ``ReceiptHeader`` is not patched.
See ``readme/CONTEXT.md`` for the full inventory.
