**Primary (Odoo 18):** **Settings → Point of Sale**. At the top, select the **Point of
Sale** shop you want to configure. In the **PoS Interface** section (same block as *Log in
with Employees*, *Hide pictures in POS*, OCA *Alternative point of sale logo*, *Remove
Order Line in POS*, etc.), open **POS product search** and set:

- **POS: minimum characters for product search** — client-side filtering starts only
  when the search box has at least this many characters (default: 5). Use 0 to filter
  from the first character (can be heavy on very large catalogs).

The value is saved on the selected ``pos.config`` (same mechanism as the other options on
that page).

**Alternative:** **Point of Sale → Configuration → Point of Sales** → open the shop
record; the same field appears in **POS product search** on the simplified ``pos.config``
form.
