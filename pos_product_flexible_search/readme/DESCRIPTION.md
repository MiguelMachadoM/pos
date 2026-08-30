In Odoo 18 the Point of Sale filters products with a contiguous substring match on
`searchString`. This module relaxes that behaviour on the product screen:

- **Ordered tokens with gaps** (similar to older POS): spaces in the query become
  flexible gaps between words in order.
- **Unordered tokens** (two or more words): every word must appear somewhere in the
  product `searchString`, in any order (substring match per word).
- **Search more** uses the same per-word rule on the server (`name`, `default_code`,
  `barcode`), so products not yet loaded in the POS session still appear.
- **Search ranking:** match quality, then `product.template` sequence (lower first),
  then name. Items with sequence 5 therefore appear above sequence 1000 when the
  match is otherwise equal.

The filter runs on the **full POS product list** (`this.products`), not only the
current category.

On large catalogs the client precomputes a normalized search haystack per product,
tokenizes the query once, and reuses the last result when OWL re-reads the getter
(same approach as Odoo 19 / Tecnativa POS search speed work).

The module does **not** define which fields are searched: it uses the same
`searchString` getter as core and any other installed addons (see *Context* below).
