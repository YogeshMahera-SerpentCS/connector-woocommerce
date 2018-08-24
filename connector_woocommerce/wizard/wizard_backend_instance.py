# © 2009 Tech-Receptives Solutions Pvt. Ltd.
# © 2018 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class WooBackendInstance(models.TransientModel):

    _name = 'wizard.backend.instance'
    # _inherit = 'woo.backend'

    instance = fields.Many2many('woo.backend', 'woo_backend_instance_rel', 'name', required=True, string="Shops")
    # instance = fields.Char()

    # Import Product operations fields
    import_product = fields.Boolean()

    # Import Product Category Operations fields
    import_product_category = fields.Boolean()

    # Import Customer operations fields
    import_customer = fields.Boolean()

    # Import Sale Order operations fields
    import_sale_order = fields.Boolean()

    import_shippingzone = fields.Boolean()

    # Export Product operations fields
    export_product = fields.Boolean()
    update_product = fields.Boolean()

    # Export Product Category Operations fields
    export_product_category = fields.Boolean()
    update_product_category = fields.Boolean()

    # Export Customer operations fields
    export_customer = fields.Boolean()
    update_customer = fields.Boolean()

    # Export Sale Order operations fields
    export_sale_order = fields.Boolean()
    update_sale_order = fields.Boolean()

    # Export Delivery Carrier operations fields
    export_shippingzone = fields.Boolean()
    update_shippingzone = fields.Boolean()

    @api.multi
    def woo_backend_instance(self):
        # Check that user has selected Shops or not
        if self.instance:
            instances = self.instance
            backend_model = self.env['woo.backend']

            # Checks that user has selected any import/export operations or not
            if self.export_shippingzone == False and self.update_shippingzone == False and self.import_shippingzone == False and self.import_product == False and self.import_product_category == False and self.import_customer == False and self.import_sale_order == False and self.export_product == False and self.update_product == False and self.export_product_category == False and self.update_product_category == False and self.export_customer == False and self.update_customer == False and self.export_sale_order == False and self.update_sale_order == False:
                raise ValidationError("Please Select Any Operation...")

            # Check and call import operations from WooCommerce to Odoo
            if self.import_shippingzone == True:
                instances.import_shippingzone()
            if self.import_product == True:
                instances.import_products()
            if self.import_product_category == True:
                instances.import_categories()
            if self.import_customer == True:
                instances.import_customers()
            if self.import_sale_order == True:
                instances.import_orders()

            # Check and call export/update operations from Odoo to WooCommerce
            if self.export_product == True or self.update_product == True:
                if self.export_product == True and self.update_product == True:
                    context = {'export_product': True, 'update_product': True}
                elif self.export_product == True and self.update_product == False:
                    context = {'export_product': True, 'update_product': False}
                elif self.update_product == True and self.export_product == False:
                    context = {'export_product': False, 'update_product': True}
                instances.with_context(context).export_product()

            if self.export_product_category == True or self.update_product_category == True:
                if self.export_product_category == True and self.update_product_category == True:
                    context = {'export_product_category': True, 'update_product_category': True}
                elif self.export_product_category == True and self.update_product_category == False:
                    context = {'export_product_category': True, 'update_product_category': False}
                elif self.update_product_category == True and self.export_product_category == False:
                    context = {'export_product_category': False, 'update_product_category': True}
                instances.with_context(context).export_category()

            if self.export_customer == True or self.update_customer == True:
                if self.export_customer == True and self.update_customer == True:
                    context = {'export_customer': True, 'update_customer': True}
                elif self.export_customer == True and self.update_customer == False:
                    context = {'export_customer': True, 'update_customer': False}
                elif self.update_customer == True and self.export_customer == False:
                    context = {'export_customer': False, 'update_customer': True}
                instances.with_context(context).export_customer()

            if self.export_sale_order == True or self.update_sale_order == True:
                if self.export_sale_order == True and self.update_sale_order == True:
                    context = {'export_sale_order': True, 'update_sale_order': True}
                elif self.export_sale_order == True and self.update_sale_order == False:
                    context = {'export_sale_order': True, 'update_sale_order': False}
                elif self.update_sale_order == True and self.export_sale_order == False:
                    context = {'export_sale_order': False, 'update_sale_order': True}
                instances.with_context(context).export_saleorder()

            if self.export_shippingzone == True or self.update_shippingzone == True:
                if self.export_shippingzone == True and self.update_shippingzone == True:
                    context = {'export_shippingzone': True, 'update_shippingzone': True}
                elif self.export_shippingzone == True and self.update_shippingzone == False:
                    context = {'export_shippingzone': True, 'update_shippingzone': False}
                elif self.update_shippingzone == True and self.export_shippingzone == False:
                    context = {'export_shippingzone': False, 'update_shippingzone': True}
                instances.with_context(context).export_shippingzone()
