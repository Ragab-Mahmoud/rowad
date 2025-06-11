# -*- coding: utf-8 -*-
{
    'name': "POS Margin Sale",

    'summary': "Ensure products are sold above their minimum price with margin checks in POS and sale orders.",

    'description': """
        The POS Margin Sale module calculates and enforces the minimum sale price and profit margin for each product. 
        When a user attempts to sell a product below its minimum price in either a sale order or a POS order, 
        the system triggers a warning, helping businesses maintain profitability and prevent underpricing.
    """,

    'author': "Doodex",
    'website': "https://www.doodex.net",
    'license': "AGPL-3",
    'category': 'Point of Sale',
    'version': '17.0.1.0',

    'depends': [
        'base', 
        'point_of_sale',  # Fixed: Removed the extra comma
        'product', 
        'sale', 
        'stock_account'
    ],

    'data': [
        'security/ir.model.access.csv',          # Always load security first
        'views/res_config_settings.xml',         # Configuration views should come next
        'views/products.xml',                    # Product view (usually referenced in sale order, so load before)
        'views/sale_order.xml',                  # Sale order view depends on products, so it comes after
        'wizard/sale_confirmation.xml',          # Wizard files related to sale confirmation
        'wizard/wizard_margin_product.xml',      # Wizard for margin product handling
    ],

    'assets': {
        'point_of_sale._assets_pos': [
            'pos_margin_sale/static/src/**/*',   # Point of sale static files, load last
        ]
    },

    'demo': [
        'demo/demo.xml',                         # Demo data is optional, usually loaded at the end
    ],
    'application': True,
    'installable': True,
    'images': ["static/description/banner.png"],
}
