Open a POS session, go to the product screen and type in the product search box as
you would in a legacy flexible search: multiple words may be in any order once the
minimum character threshold is reached.

If a matching product is missing from the grid (limited POS catalog load), click
**Search more** (or press Enter). The server looks up each word separately on name,
internal reference and barcode — the same idea as Smart Search — instead of one
contiguous phrase. New hits are merged into the session and ranked with the rest
(sequence, then name).

On large catalogs the filter is written to avoid repeating ``unaccent`` / regex
work per product and per OWL re-render. Core POS already debounces the search box
(500 ms).
