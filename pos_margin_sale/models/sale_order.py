from odoo import _, api, fields, models
from odoo.exceptions import ValidationError



class SaleOrder(models.Model):
    _inherit = 'sale.order'


    is_rental_order_installed_true = fields.Boolean(default=False, compute='_compute_is_rental_order_installed', store=False)

    def _compute_is_rental_order_installed(self):
        for record in self:
            if hasattr(self, 'is_rental_order') and self.is_rental_order:
                record.is_rental_order_installed_true = True
            else:
                record.is_rental_order_installed_true = False

    def action_confirm(self):

        if self.is_rental_order_installed_true:
            return super(SaleOrder, self).action_confirm()  

        skip_check_price = self._context.get('skip_check_price')
        check_product = self.check_product_price()
        blocking_warning = self.env['ir.config_parameter'].sudo().get_param('post_margin_sale.blocking_transaction_order')
        if len(check_product) > 0 and not skip_check_price:
            product_str = ('\n').join(f" {i + 1}. {product.display_name} minimum price is {product.currency_id.symbol}. {product.minimum_sale_price:.2f}" for i,product in enumerate(check_product))
            product_str_fr = ('\n').join(f" {i + 1}. {product.display_name} le prix minimum est {product.currency_id.symbol}. {product.minimum_sale_price:.2f}" for i,product in enumerate(check_product))
            message = (_(f"Price of this product is less than minimum sale price \n\n{product_str}"))
            message_Fr = f"Le prix de ce produit est inférieur au prix de vente minimum \n\n{product_str_fr}"
            user_language = self.detect_user_language()
            if blocking_warning:
                    if user_language == 'French':
                        raise ValidationError(_(f"{message_Fr} \n\nTransaction bloquée car prix inférieur au prix minimum de vente."))
                    else:
                        raise ValidationError(_(f"{message} \n\nTransaction blocked due to price being lower than the minimum sale price."))
            else:
                message += "\n\nDo you want to continue with the quotation for making sale order?"
                message_Fr += "\n\nVoulez-vous continuer avec le devis pour passer commande ?"
                wizard = self.env['sale.confirmation.wizard'].create({'message': message})
                wizard.with_context(lang='fr_FR').write({
                'message': message_Fr})
                return {
                    'type': 'ir.actions.act_window',
                    'name': _('Confirm minimum sale price'),
                    'view_mode': 'form',
                    'res_model': 'sale.confirmation.wizard',
                    'target': 'new',
                    'res_id': wizard.id,
                }
        return super(SaleOrder, self).action_confirm()

    def detect_user_language(self):
        # Get the user's language from the context
        user_lang = self.env.context.get('lang', 'en_US')  # Default to English if not set

        # Check if the user language is French
        if user_lang.startswith('fr'):
            return 'French'
        else:
            return 'Other'

    def check_product_price(self):
        products = []
        for line in self.order_line:
            if line.price_unit < line.minimum_sale_price:
                products.append(line.product_id)
        return products

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    minimum_sale_price = fields.Float(string="Minimum sale price", related='product_id.minimum_sale_price')