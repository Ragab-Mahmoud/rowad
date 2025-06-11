/** @odoo-module **/

import { Orderline, Product, Order } from "@point_of_sale/app/store/models";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";
import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";


patch(Product.prototype, {
    get_minimum_sale_price() {
        return this.minimum_sale_price;
    },

    get_minimum_sale_price_with_tax() {
        return this.minimum_sale_price_with_tax;
    }
})


patch(Orderline.prototype, {
    set_unit_price(price) {
        super.set_unit_price(price);
    },

    getDisplayData() {
        return {
            productName: this.get_full_product_name(),
            price: this.getPriceString(),
            qty: this.get_quantity_str(),
            unit: this.get_unit().name,
            unitPrice: this.env.utils.formatCurrency(this.get_unit_display_price()),
            unitPriceInt: this.get_unit_display_price(),
            oldUnitPrice: this.env.utils.formatCurrency(this.get_old_unit_display_price()),
            discount: this.get_discount_str(),
            customerNote: this.get_customer_note(),
            internalNote: this.getNote(),
            comboParent: this.comboParent?.get_full_product_name(),
            pack_lot_lines: this.get_lot_lines(),
            price_without_discount: this.env.utils.formatCurrency(
                this.getUnitDisplayPriceBeforeDiscount()
            ),
            attributes: this.attribute_value_ids
                ? this.findAttribute(this.attribute_value_ids, this.custom_attribute_value_ids)
                : [],
            minimumSalePrice: this.env.utils.formatCurrency(this.product.get_minimum_sale_price()), // Added minimum_sale_price
            minimumSalePriceWithTax:  this.env.utils.formatCurrency(this.product.get_minimum_sale_price_with_tax()),
            isLessMinimumSalePrice: this.get_unit_display_price() < this.product.get_minimum_sale_price_with_tax()
        };
    }

});

patch(Order.prototype, {
    async pay() {
        const orderLines = this.get_orderlines();
        const lines = orderLines.filter(line => line.get_unit_display_price() < line.product.get_minimum_sale_price_with_tax());
        const blocked = this.pos.config.is_blocked_warning
        if (lines.length > 0) {
            // Display the confirmation popup with the constructed message
            if (!blocked) {
                const  {confirmed } = await this.env.services.popup.add(ConfirmPopup, {
                    title: _t("Price unit less than minimum price"),
                    body: _t("Some products are below the minimum price. Proceed to payment?")
                });
                if (!confirmed) {
                    return;
                }
            } else {
                await this.env.services.popup.add(ErrorPopup, {
                    title: _t("Price unit less than minimum price"),
                    body: _t("Some products are below the minimum price. Please check !")
                });
                return;
            }
        }
   
        return super.pay(...arguments);
    }
});