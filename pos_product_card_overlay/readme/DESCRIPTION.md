In the Odoo 18 Point of Sale product grid, products with an image use a short white
strip under the photo for the name (two lines). Long titles and internal references
are often truncated.

This module draws the label **on top of the image**: a semi-transparent dark band at
the bottom with white text, a smaller font, and the internal reference (`default_code`)
on its own line when present. On pointer hover (desktop), the band grows upward over
the image to show the full name without changing the card size in the grid.

Products **without** an image keep the standard full-card text layout.

**Dependencies:** only `point_of_sale`. The internal reference is read from standard
PoS product data (`default_code`) and rendered by this addon, so it does **not**
depend on `pos_product_display_default_code`. If that (or another) addon prefixes the
visible name with `[CODE]`, the prefix is stripped on the overlay to avoid showing
the reference twice.

When a product has a **PoS color** set on the template, the image area shows a colored
left bar and a thin frame.
