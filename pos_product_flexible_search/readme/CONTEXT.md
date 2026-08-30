## What is inside `searchString`?

This addon only matches against `product.product.searchString` in the POS client.

**Core Odoo 18** builds it from `display_name`, `barcode` and `default_code`
(`addons/point_of_sale/static/src/app/models/product_product.js`).

Other addons may **patch** that getter and append data (for example purchase
**seller** lines). A common pattern is OCA *pos_supplierinfo_search*, which adds
supplier names and codes; the partner `display_name` often includes the
**commercial entity name**, so tokens like a brand name can match even when they
do not appear in the short product title on the card.

If removing a vendor line from the product purchase tab changes search results,
the cause is the **extended `searchString`**, not the flexible matching rules in
this module.

**Grid sort:** `pos_product_sort` applies favorites / top-sales only when browsing
(no search text). It does not re-sort `getProductsBySearchWord`. Search hits are
ordered by this module: match score, then `sequence` (lower first), then name.
