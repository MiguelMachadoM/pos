Useful when one company (one NIF) runs several shops with different
commercial names and street addresses. `pos_config_logo` only swaps the
logo; this module swaps the header text for that POS.

Settings: field labels come from the Python ``string=`` (translated in
``i18n/es.po``). ZIP is ``res.city.zip`` from ``base_location``; onchange
fills city, province and the stored ZIP code used on the ticket. The receipt
header prints phone and email with Font Awesome icons (``fa-phone``,
``fa-envelope``). ``pos_receipt_compact`` only scales that contact block; it
does not own the icons.
