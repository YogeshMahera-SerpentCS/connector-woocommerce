# -*- coding: utf-8 -*-
#
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#

import logging
import xmlrpclib
from odoo import models, fields, api, _
from odoo.addons.connector.exception import IDMissingInBackend
from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class woo_sale_order_status(models.Model):
    _name = 'woo.sale.order.status'
    _description = 'WooCommerce Sale Order Status'

    name = fields.Char('Name')
    desc = fields.Text('Description')


class SaleOrder(models.Model):

    _inherit = 'sale.order'
    status_id = fields.Many2one('woo.sale.order.status',
                                'WooCommerce Order Status')


class WooSaleOrder(models.Model):
    _name = 'woo.sale.order'
    _inherit = 'woo.binding'
    _inherits = {'sale.order': 'odoo_id'}
    _description = 'Woo Sale Order'

    _rec_name = 'name'

    status_id = fields.Many2one('woo.sale.order.status',
                                'WooCommerce Order Status')

    odoo_id = fields.Many2one(comodel_name='sale.order',
                                 string='Sale Order',
                                 required=True,
                                 ondelete='cascade')
    woo_order_line_ids = fields.One2many(
        comodel_name='woo.sale.order.line',
        inverse_name='woo_order_id',
        string='Woo Order Lines'
    )
    backend_id = fields.Many2one(
        comodel_name='woo.backend',
        string='Woo Backend',
        store=True,
        readonly=False,
        required=True,
    )


class WooSaleOrderLine(models.Model):
    _name = 'woo.sale.order.line'
    _inherits = {'sale.order.line': 'odoo_id'}

    woo_order_id = fields.Many2one(comodel_name='woo.sale.order',
                                   string='Woo Sale Order',
                                   required=True,
                                   ondelete='cascade',
                                   index=True)

    odoo_id = fields.Many2one(comodel_name='sale.order.line',
                                 string='Sale Order Line',
                                 required=True,
                                 ondelete='cascade')

    backend_id = fields.Many2one(
        related='woo_order_id.backend_id',
        string='Woo Backend',
        readonly=True,
        store=True,
        required=False,
    )

    @api.model
    def create(self, vals):
        woo_order_id = vals['woo_order_id']
        binding = self.env['woo.sale.order'].browse(woo_order_id)
        vals['order_id'] = binding.odoo_id.id
        binding = super(WooSaleOrderLine, self).create(vals)
        return binding


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    woo_bind_ids = fields.One2many(
        comodel_name='woo.sale.order.line',
        inverse_name='odoo_id',
        string="WooCommerce Bindings",
    )


class SaleOrderAdapter(Component):
    _name = 'woo.sale.order.adapter'
    _inherit = 'woo.adapter'
    _apply_on = 'woo.sale.order'

    _woo_model = 'orders'

    def _call(self, method, arguments):
        try:
            return super(SaleOrderAdapter, self)._call(method, arguments)
        except xmlrpclib.Fault as err:
            # this is the error in the Woo API
            # when the customer does not exist
            if err.faultCode == 102:
                raise IDMissingInBackend
            else:
                raise

    def search(self, filters=None, from_date=None, to_date=None):
        """ Search records according to some criteria and return a
        list of ids

        :rtype: list
        """
        if filters is None:
            filters = {}
        WOO_DATETIME_FORMAT = '%Y/%m/%d %H:%M:%S'
        dt_fmt = WOO_DATETIME_FORMAT
        if from_date is not None:
            # updated_at include the created records
            filters.setdefault('updated_at', {})
            filters['updated_at']['from'] = from_date.strftime(dt_fmt)
        if to_date is not None:
            filters.setdefault('updated_at', {})
            filters['updated_at']['to'] = to_date.strftime(dt_fmt)

        return self._call('orders/list',
                          [filters] if filters else [{}])