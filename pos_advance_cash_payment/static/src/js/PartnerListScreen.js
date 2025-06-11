/** @odoo-module */

import { PartnerListScreen } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";
import { Component, onMounted, useExternalListener, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { AddPaymentPopupWidget } from "@pos_advance_cash_payment/js/AddPaymentPopupWidget";

patch(PartnerListScreen.prototype, {
	setup() {
        super.setup();
        this.popup = useService("popup");
	},

	addPayment(partner){
		this.popup.add(AddPaymentPopupWidget, {'partner': partner});
	}
});