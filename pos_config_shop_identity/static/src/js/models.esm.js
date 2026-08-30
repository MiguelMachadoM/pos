import {PosStore} from "@point_of_sale/app/store/pos_store";
import {patch} from "@web/core/utils/patch";

function _nonEmpty(value) {
    return value ? value : false;
}

function _commaLine(parts) {
    return parts
        .map((part) => (part || "").toString().trim())
        .filter(Boolean)
        .join(", ");
}

patch(PosStore.prototype, {
    getReceiptHeaderData() {
        const result = super.getReceiptHeaderData(...arguments);
        const cfg = this.config;
        if (!cfg?.shop_identity_enabled) {
            return result;
        }
        const shopIdentity = {
            name: cfg.shop_identity_name || "",
            street: cfg.shop_identity_street || "",
            street2: cfg.shop_identity_street2 || "",
            zip: cfg.shop_identity_zip || "",
            city: cfg.shop_identity_city || "",
            state: cfg.shop_identity_state_name || "",
            phone: cfg.shop_identity_phone || "",
            email: cfg.shop_identity_email || "",
        };
        shopIdentity.addressLine = _commaLine([
            shopIdentity.street,
            shopIdentity.street2,
            shopIdentity.zip,
            shopIdentity.city,
            shopIdentity.state,
        ]);
        const companyVat = result.company?.vat || this.company?.vat || "";
        const vatLabel =
            result.company?.country_id?.vat_label ||
            this.company?.country_id?.vat_label ||
            "";
        shopIdentity.vat = companyVat;
        shopIdentity.vatLabel = vatLabel;
        result.shopIdentity = shopIdentity;
        if (result.company) {
            result.company = {
                ...result.company,
                name: _nonEmpty(shopIdentity.name),
                phone: false,
                email: false,
                vat: false,
                street: false,
                street2: false,
                zip: false,
                city: false,
                state_id: false,
            };
        }
        return result;
    },
});
