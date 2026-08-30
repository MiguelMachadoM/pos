Uses the standard product **Sequence** field and a **configurable sort order**
for the Point of Sale product grid (per ``pos.config``).

Default grid order when no custom lines are set:

1. Sequence (ascending; missing values are treated as 1000)
2. Internal reference / default code (ascending)
3. Name (ascending)

Each shop can change that list in Point of Sale settings: add, remove or
reorder criteria, independently ascending or descending. Supported keys are
Sequence, internal reference, name, and **Top sales** (quantity sold on
paid POS order lines, all shops combined).

**Favorites first** (per POS, enabled by default): products marked as favorites
in Odoo are listed before the rest. The configured sort still applies within
favorites and within non-favorites.

**Top sales** uses a stored quantity per product. It is refreshed on module
install or upgrade and, when enabled, **once per day** by a scheduled action
(off by default; switch it on in POS settings). The local time is configurable
(default 03:00 in the company timezone when the cron has no timezone set). The
POS client does not recompute top sales on each sale.

New products default to **1000**. On install, products still at Odoo's create
default (``1``) are set to ``1000`` so new and existing items share the same
baseline. Lower Sequence values still appear first.

Backend product loading still uses the standard POS product order. The visible
grid order is applied in the POS client when **browsing** the product grid
(``ProductScreen``). Text search keeps the match ranking from core or from
addons such as ``pos_product_flexible_search``; this module does not re-sort
search hits (that would also be expensive on large catalogs).
