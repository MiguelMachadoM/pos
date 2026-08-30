To configure this module, you need to:

* The POS settings screen is translated in Spanish (``i18n/es_ES.po`` /
  ``i18n/es.po``). After installing or updating the module, reload the
  settings page (Ctrl+F5) if labels still appear in English.
* Go to *Point of Sale > Configuration > Settings* and select your POS shop.
* **POS grid: favorites first** (default on): favorite products appear above
  the rest. Within each group the sort order below still applies. Favorites use
  Odoo's standard *Favorite* flag (star on the product form or in the POS
  product info popup).
* In **POS product grid order**, add, remove or reorder rows. Each row is one
  sort field and a direction (ascending / descending). The first row has the
  highest priority.
* Default rows: **Sequence** (asc), **Internal reference** (asc), **Name**
  (asc).
* Optional **Top sales** uses the stored field *POS quantity sold* (sum of
  quantities on paid POS order lines, all POS configurations). Turn on
  **Recompute top sales daily** in the same POS settings screen to activate the
  scheduled action *POS sequence: recompute top sales quantities* (off by
  default; one job for all shops). Default run time is **03:00** in the
  **company timezone** (or the timezone set on that cron). Hour, minute and
  timezone can still be edited under *Settings → Technical → Automation →
  Scheduled Actions*. Quantities are not updated after each POS sale.
* On each product (*Point of Sale > Products > Products*), set **Sequence**
  (lower values appear earlier when that criterion is used). The same field is
  editable from the POS product edit popup. New products default to **1000**.
  On install, products still at Odoo's create default (``1``) are set to
  ``1000``; any other Sequence is left unchanged.
