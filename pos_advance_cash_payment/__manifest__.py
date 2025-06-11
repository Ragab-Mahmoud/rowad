# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

{
    "name": "POS Advance Payment & Register Payment in Odoo",
    "version": "17.0.0.0",
    "category": "Point of Sale",
    'summary': 'Apps point of sale advance payment from POS touchscreen pos register payment advance payment in POS point of sales advance payment pos advance cash payment pos cash payment POS Advanced Product Ordering POS Advanced payment point of sale register payment',
    "description": """

	POS Advance Payment Or Register Payment
This apps helps to record customer payment/Receipt from the POS touchscreen which will recorded as customer payment/receipt in backend which can be reconciled with the invoice or with due payment . Also it will helps to record as advance payment from the customer.
key features:
odoo advance payment in POS register payment in pos
odoo pos advance payment advance cash in pos
odoo pos cash pos advance cash pos cash payment
odoo payment receipt in POS 
odoo POS payment receipt
pos invoice payment pos accounting payment pos register payment pos voucher payment pos payment 
    pos payment from pos screen invoice payment from POS screen register payment from pos screen
    pay invoice from POS screen accounting payment from POS screen
    point of sale invoice payment point of sale accounting payment point of sale register payment
    point of sale voucher payment point of sale payment payment from point of sale screen
    pos invoice payment from point of sale screen register payment from point of sale screen
    pay invoice from point of sale screen accounting payment from point of sale screen pos multiple invoice payment
    pos mass invoice payment point of sales multiple invoice payment point of sales mass invoice payment
This module will take the advance payment from the customer by POS touchscreen.
This module helps to register payment from the customer by POS touch Screen.
    Sales representatives needs to take payments about the invoices that have been issued before. Those payments are Customer Receipts on the backend. POS cash payment, POS Advance payment, POS payment, Payment on POS screen , POS screen payment, Advance Payment on POS, Advance Payment on point of sale, point of sale advance payment.
    """,
    "author": "BrowseInfo",
    "website": "https://www.browseinfo.com",
    'price': 19.00,
    'currency': "EUR",
    "depends": ['base', 'sale', 'point_of_sale'],
    "data": ['security/ir.model.access.csv',
             ],
    'assets': {
        'point_of_sale._assets_pos': [
            'pos_advance_cash_payment/static/src/js/AddPaymentPopupWidget.js',
            'pos_advance_cash_payment/static/src/js/PartnerListScreen.js',
            'pos_advance_cash_payment/static/src/js/models.js',
            'pos_advance_cash_payment/static/src/xml/pos_extended.xml',
        ],
    },
    "auto_install": False,
    "installable": True,
    'live_test_url': 'https://youtu.be/mon8YCCKY2w',
    "images": ['static/description/Banner.gif'],
    'license': 'OPL-1',
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
