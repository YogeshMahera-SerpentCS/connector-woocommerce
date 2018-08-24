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

    @api.multi
    def woo_backend_instance(self):
        print("woo_backend_instance call--------------------")
        # Check that user has selected Shops or not
        if self.instance:
            print("Shop found............", self.instance)
            instances = self.instance
            backend_model = self.env['woo.backend']

            # Checks that user has selected any import/export operations or not
            if self.import_product == False and self.import_product_category == False and self.import_customer == False and self.import_sale_order == False and self.export_product == False and self.update_product == False and self.export_product_category == False and self.update_product_category == False and self.export_customer == False and self.update_customer == False and self.export_sale_order == False and self.update_sale_order == False:
                raise ValidationError("Please Select Any Operation...")

            # Check and call import operations from WooCommerce to Odoo
            if self.import_product == True:
                print("Import Product Selected------------")
                instances.import_products()
            if self.import_product_category == True:
                print("Import Product Category Selected------------")
                instances.import_categories()
            if self.import_customer == True:
                print("Import Customer Selected------------")
                instances.import_customers()
            if self.import_sale_order == True:
                print("Import Sales Orders Selected------------")
                instances.import_orders()

            # Check and call export/update operations from Odoo to WooCommerce
            if self.export_product == True and self.update_product == True:
                context={'export_product': True, 'update_product': True}
                instances.with_context(context).export_product()
            elif self.export_product == True and self.update_product == False:
                context={'export_product': True, 'update_product': False}
                instances.with_context(context).export_product()
            elif self.update_product == True and self.export_product == False:
                context={'export_product': False, 'update_product': True}
                instances.with_context(context).export_product()

            if self.export_product_category == True and self.update_product_category == True:
                context={'export_product_category': True, 'update_product_category': True}
                instances.with_context(context).export_category()
            elif self.export_product_category == True and self.update_product_category == False:
                context={'export_product_category': True, 'update_product_category': False}
                instances.with_context(context).export_category()
            elif self.update_product_category == True and self.export_product_category == False:
                context={'export_product_category': False, 'update_product_category': True}
                instances.with_context(context).export_category()

            if self.export_customer == True and self.update_customer == True:
                context={'export_customer': True, 'update_customer': True}
                instances.with_context(context).export_customer()
            elif self.export_customer == True and self.update_customer == False:
                context={'export_customer': True, 'update_customer': False}
                instances.with_context(context).export_customer()
            elif self.update_customer == True and self.export_customer == False:
                context={'export_customer': False, 'update_customer': True}
                instances.with_context(context).export_customer()

            if self.export_sale_order == True and self.update_sale_order == True:
                context={'export_sale_order': True, 'update_sale_order': True}
                instances.with_context(context).export_saleorder()
            elif self.export_sale_order == True and self.update_sale_order == False:
                context={'export_sale_order': True, 'update_sale_order': False}
                instances.with_context(context).export_saleorder()
            elif self.update_sale_order == True and self.export_sale_order == False:
                context={'export_sale_order': False, 'update_sale_order': True}
                instances.with_context(context).export_saleorder()
