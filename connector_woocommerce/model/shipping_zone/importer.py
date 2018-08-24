# © 2009 Tech-Receptives Solutions Pvt. Ltd.
# © 2018 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
# See LICENSE file for full copyright and licensing details.

import logging
import base64
import urllib.request
import urllib.error

from odoo.addons.component.core import Component
from odoo.addons.connector.components.mapper import mapping
from odoo.addons.connector.exception import MappingError

_logger = logging.getLogger(__name__)


class ShippingZoneBatchImporter(Component):

    """ Import the WooCommerce Product Categories.

    For every partner in the list, a delayed job is created.
    """

    _name = 'woo.shipping.zone.batch.importer'
    _inherit = 'woo.delayed.batch.importer'
    _apply_on = 'woo.shipping.zone'

    def _import_record(self, woo_id):
        """ Delay a job for the import """
        super(ShippingZoneBatchImporter, self)._import_record(
            woo_id)

    def run(self, filters=None):
        """ Run the synchronization """
        print("RUN CALL---------------------")
        from_date = filters.pop('from_date', None)
        to_date = filters.pop('to_date', None)
        #backend_adapter = self.component(usage='backend.adapter')
        record_ids = self.backend_adapter.search(
            method='get',
            filters=filters,
            from_date=from_date,
            to_date=to_date,
        )
        print("RECORD..................................")
        '''To check that if any product category is deleted from
        WooCommerce then remove reference of that product category from Odoo'''
        ShippingZone_ref = self.env['woo.shipping.zone']
        record = []
        # Get external ids from odoo for comparison
        zone_rec = ShippingZone_ref.search([('external_id', '!=', '')])
        for ext_id in zone_rec:
            record.append(int(ext_id.external_id))
        # Get difference ids
        diff = list(set(record)-set(record_ids))
        for del_woo_rec in diff:
            woo_zone_id = ShippingZone_ref.search([('external_id', '=', del_woo_rec)])
            zone_id = woo_zone_id.odoo_id
            odoo_zone_id = self.env['res.country'].search([('id', '=', zone_id.id)])
            # Delete reference from odoo
            odoo_zone_id.write({
            'woo_bind_ids': [(3, odoo_zone_id.woo_bind_ids[0].id)],
            'sync_data': False,
            'woo_backend_id': None
        })

        _logger.info('search for woo shipping zone %s returned %s',
                     filters, record_ids)
        for record_id in record_ids:
            self._import_record(record_id)


class ShippingZoneImporter(Component):
    _name = 'woo.shipping.zone.importer'
    _inherit = 'woo.importer'
    _apply_on = ['woo.shipping.zone']

    # def _import_dependencies(self):
    #     """ Import the dependencies for the record"""
    #     record = self.woo_record
    #     # import parent category
    #     # the root category has a 0 parent_id
    #     record = record['args']
    #     if record['parent']:
    #         self._import_dependency(record.get('parent'), self.model)
    #     return

    def _create(self, data):
        print("=====================>", data)
        odoo_binding = super(ShippingZoneImporter, self)._create(data)
        # Adding Creation Checkpoint
        self.backend_record.add_checkpoint(odoo_binding)
        return odoo_binding

    def _update(self, binding, data):
        """ Update an Odoo record """
        super(ShippingZoneImporter, self)._update(binding, data)
        # Adding updation checkpoint
        #self.backend_record.add_checkpoint(binding)
        return

    def _before_import(self):
        """ Hook called before the import"""
        return

    def _after_import(self, binding):
        """ Hook called at the end of the import """
        return


class ShippingZoneImportMapper(Component):
    _name = 'woo.shipping.zone.import.mapper'
    _inherit = 'woo.import.mapper'
    _apply_on = 'woo.shipping.zone'

    @mapping
    def name(self, record):
        if record['name']:
            rec = record['name']
            # print("nameeeeeeee", rec['name'])
            return {'name': rec['name']}

    @mapping
    def backend_id(self, record):
        print("---------", self.backend_record.id)
        return {'backend_id': self.backend_record.id}

    # @mapping
    # def parent_id(self, record):
    #     if record['args']:
    #         rec = record['args']
    #         if not rec['parent']:
    #             return
    #         binder = self.binder_for()
    #         # Get id of product.category model
    #         zone_id = binder.to_internal(rec['parent'], unwrap=True)
    #         # Get id of woo.product.category model
    #         woo_zone_id = binder.to_internal(rec['parent'])
    #         if zone_id is None:
    #             raise MappingError("The shipping zone with "
    #                                "woo id %s is not imported." %
    #                                rec['parent'])
    #         return {'parent_id': zone_id.id,
    #                 'woo_parent_id': woo_zone_id.id}

    # @mapping
    # def woo_image(self, record):
    #     image = record.get('image')
    #     if image:
    #         src = image.replace("\\", '')
    #         try:
    #             request = urllib.request.Request(src)
    #             binary = urllib.request.urlopen(request)
    #         except urllib.error.HTTPError as err:
    #             if err.code == 404:
    #                 # the image is just missing, we skip it
    #                 return
    #             else:
    #                 # we don't know why we couldn't download the image
    #                 # so we propagate the error, the import will fail
    #                 # and we have to check why it couldn't be accessed
    #                 raise
    #         else:
    #             return {'woo_image': base64.b64encode(binary.read())}

    # Required for export
    @mapping
    def sync_data(self, record):
        if record.get('res.country'):
            return {'sync_data': True}

    @mapping
    def woo_backend_id(self, record):
        return {'woo_backend_id': self.backend_record.id}
