/** @odoo-module **/

import { ConfirmPopup } from "@point_of_sale/app/utils/confirm_popup/confirm_popup";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { useService } from "@web/core/utils/hooks";

export class AddPaymentPopupWidget extends ConfirmPopup {
    static template = "pos_advance_cash_payment.AddPaymentPopupWidget";

    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
    }

    addPayment () {
		var self = this;			
		let partner = this.props.partner;		
		var payment_type = $('#payment_type').val();
		var entered_amount = $("#entered_amount").val();

		if(!entered_amount || parseFloat(entered_amount) == 0){
			alert('Please enter valid amount !!!!');
		}else{			
			self.orm.call('pos.order',
				'create_customer_payment',
				[0, partner.id, payment_type, entered_amount],
			).then(function(output) {
				alert('Customer Payment Created !!!!');
				let old_ledger_balance = parseFloat(partner.ledger_balance)
				let new_bal = old_ledger_balance - parseFloat(entered_amount)
				partner.ledger_balance = new_bal;
				self.props.close({ confirmed: true});
			});	
		}		
	}
}