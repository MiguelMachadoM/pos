## 18.0.1.0.0

- Initial OCA release of ``pos_product_sort``:
  - Uses the standard product **Sequence** field (lower values first).
    New products default to **1000**. On install, rows still at Odoo's create
    default (``1``) are set to ``1000``; any other Sequence is left unchanged.
  - Configurable **POS product grid order** per ``pos.config`` (sequence,
    internal reference, name, top sales; ascending or descending).
  - **Favorites first** (Odoo favorite flag, enabled by default per POS).
  - Stored **POS quantity sold** for the top-sales sort key, recomputed on
    install/upgrade and by an optional daily scheduled action (off by default;
    enabled from POS settings) with editable local hour/minute/timezone.
  - POS client (``ProductScreen``) applies the visible grid order when
    browsing; search results keep match ranking. Backend product loading
    stays standard.
