/* Copyright 2026 Miguel Machado <memachado@gmail.com>
   License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as Dialog from "@point_of_sale/../tests/tours/utils/dialog_util";
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("PosProductCardOverlayTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            Dialog.confirm("Open Register"),
            {
                content: "Product with image uses the overlay class",
                trigger: "article.product.o_pos_product_card_overlay",
            },
            {
                content: "Internal reference is rendered on the overlay band",
                trigger:
                    "article.o_pos_product_card_overlay .product-default-code:contains(OVL-001)",
            },
        ].flat(),
});
