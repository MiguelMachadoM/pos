Open a Point of Sale session and go to the product screen.

- Products **with** an image show the name and internal reference on the overlay band.
- Hover the card (desktop) to expand the band and read the full product name.
- Products **without** an image behave like standard Odoo PoS cards.

No extra PoS addon is required for the reference line. Other addons that show
`default_code` on the ticket or order lines keep their own behaviour.

After code or asset changes, upgrade the module on the database and refresh the PoS
session (close and reopen, or hard-refresh the browser) so SCSS/JS assets reload.
