Open the POS, complete an order and show or print the receipt.

Product names stay on one line (CSS ellipsis; JS fallback at the configured
character limit, default 60) and are not bold.
If the quantity is 1, the ``1.00 x price / Unit`` row is hidden (configurable).
TOTAL is printed in bold. The footer ("Powered by Odoo", order name, date) is
tighter, without the extra gap in the middle.

Font sizes follow the values set on this POS. After changing them in Settings,
close the POS session screen and reopen the register so the client reloads the
config. The on-screen cart is unchanged (truncation and hide-qty run only in
``export_for_printing``).
