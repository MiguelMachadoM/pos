import {Orderline} from "@point_of_sale/app/generic_components/orderline/orderline";
import {OrderReceipt} from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {patch} from "@web/core/utils/patch";
import {floatIsZero} from "@web/core/utils/numbers";

/** Default max product name length on the printed / preview receipt. */
export const RECEIPT_PRODUCT_NAME_MAX = 60;

export function truncateReceiptProductName(name, maxLen = RECEIPT_PRODUCT_NAME_MAX) {
    const text = (name || "").toString();
    const max = Number(maxLen);
    if (!Number.isFinite(max) || max <= 0) {
        return text;
    }
    if (text.length <= max) {
        return text;
    }
    return `${text.slice(0, max).trimEnd()}…`;
}

function _compactFromConfig(config) {
    const rawMax = config?.receipt_product_name_max;
    const productNameMax =
        rawMax === 0 || rawMax === "0"
            ? 0
            : Number(rawMax) || RECEIPT_PRODUCT_NAME_MAX;
    return {
        header: config?.receipt_font_header || "medium",
        tracking: config?.receipt_font_tracking || "small",
        lines: config?.receipt_font_lines || "small",
        totals: config?.receipt_font_totals || "medium",
        footer: config?.receipt_font_footer || "small",
        hideUnitQty: Boolean(config?.receipt_hide_unit_qty),
        productNameMax,
    };
}

patch(Orderline, {
    props: {
        ...Orderline.props,
        line: {
            ...Orderline.props.line,
            shape: {
                ...Orderline.props.line.shape,
                hideQtyBreakdown: {type: Boolean, optional: true},
            },
        },
    },
});

patch(OrderReceipt.prototype, {
    get compactReceiptClass() {
        const compact = this.props.data.compactReceipt || {};
        return {
            "pos-receipt": true,
            "p-2": true,
            [`o_rcpt_header_${compact.header || "medium"}`]: true,
            [`o_rcpt_track_${compact.tracking || "small"}`]: true,
            [`o_rcpt_lines_${compact.lines || "small"}`]: true,
            [`o_rcpt_totals_${compact.totals || "medium"}`]: true,
            [`o_rcpt_footer_${compact.footer || "small"}`]: true,
        };
    },
});

patch(PosOrder.prototype, {
    export_for_printing() {
        const result = super.export_for_printing(...arguments);
        const compact = _compactFromConfig(this.config);
        result.compactReceipt = compact;
        const srcLines = this.getSortedOrderlines();
        const decimals = this.currency?.decimal_places ?? 2;
        if (result.orderlines) {
            result.orderlines = result.orderlines.map((line, index) => {
                const src = srcLines[index];
                const qty = src ? src.get_quantity() : 1;
                const hideQtyBreakdown =
                    compact.hideUnitQty && floatIsZero(Math.abs(qty) - 1, decimals);
                return {
                    ...line,
                    productName: truncateReceiptProductName(
                        line.productName,
                        compact.productNameMax,
                    ),
                    hideQtyBreakdown,
                };
            });
        }
        return result;
    },
});
