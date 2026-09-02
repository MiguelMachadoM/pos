Open a POS session with shortcuts enabled. Press **H** for the in-session
list (read-only).

On the product screen, letters run actions when the cursor is **not** in an
input. **B** focuses product search.

After you add a product from the results (if the hold is not Off):

1. The search box **loses focus** so a barcode scan is not typed as a new
   query.
2. The **filter stays** 5 or 10 seconds so you can tap another matching
   card.
3. Then the filter and the box are **cleared**. **Esc** clears them
   immediately.

On payment, **C** is customer, **F** toggles invoice, **E** is the first
cash method of that shop, **T** is the first bank method of that shop,
**Enter** validates, **Esc** goes back. Extra methods only show their
letter on shops that have them. A shop without cash ignores **E** (notice
only). A shop without that extra method does not show its letter.

On the receipt screen, **I** prints the full receipt, **B** the basic
receipt (if enabled on the POS), and **Enter** starts a new order.

Actions that cannot run (no selected line, missing `pos_discount`, no
fiscal positions, and so on) show a top-right notification and do not
block the cashier or the scanner.

**Ctrl+Alt+C** (default, configurable) cancels the current order, using
the native confirmation when the ticket is not empty.
