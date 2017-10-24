# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    access_group_ids = fields.Many2many(comodel_name='res.groups', string='Access Groups', help='Allowed groups to access this product')


class product_product(models.Model):
    _inherit = 'product.product'

    access_group_ids = fields.Many2many(comodel_name='res.groups', string='Access Groups', help='Allowed groups to access this product')
