When products are shown in the Point of Sale grid **without a search query**,
they are sorted using the **POS product grid order** of the active POS
configuration. Out of the box:

1. Favorites first (if enabled)
2. Sequence (ascending)
3. Internal reference (ascending)
4. Product name (ascending)

You can add **Top sales (descending)** as the first sort row to surface
best-selling products first within each group (favorites / non-favorites).

Mark products as favorites (star on the product form or in the POS product
info popup) to pin them to the top of the grid while keeping the same inner
sort order.

Set **Sequence** on the product form (Point of Sale tab) or when editing a
product from the POS. Lower values appear first. New products default to
**1000**. On install, products at Odoo's create default (``1``) are moved to
``1000`` so they share that baseline.

**Top sales** quantities are not updated on each sale. Enable **Recompute top
sales daily** in POS settings to run the scheduled action *POS sequence:
recompute top sales quantities* (default 03:00 in the company timezone). Change
**local hour**, **minute** and **timezone** on that job under *Settings →
Technical → Automation → Scheduled Actions*.
