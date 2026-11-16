## 19.0.1.0.1

- Pay customer invoice/refund from POS on Odoo 19:
  - set ``account_move`` **after** ``add_payment``;
  - replace removed ``_apply_invoice_payments`` with
    ``_create_payment_moves`` + ``_reconcile_invoice_payments``;
  - order state ``invoiced`` → ``paid``;
  - tests: ``TestPoSCommon`` (``TestPointOfSaleCommon`` removed).

