# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class product_template(models.Model):
    _inherit = 'product.template'

    access_group_ids = fields.Many2many(comodel_name='res.groups', string='Access Groups', help='Allowed groups to access this product')

    @api.multi
    def check_access_group(self,user):
        self.ensure_one()
        if self.sudo().access_group_ids:
            return True if len(user.sudo().commercial_partner_id.access_group_ids & self.sudo().access_group_ids) > 0 else False
        else:
            return True

    @api.model
    def search_access_group(self,domain, limit=100000, offset=0, order=''):
        access_group_ids = self.env['res.users'].sudo().browse(self.env.uid).commercial_partner_id.access_group_ids
        return self.env['product.template'].search(domain, order=order).filtered(lambda p: not p.sudo().access_group_ids or access_group_ids & p.sudo().access_group_ids)[offset:offset+limit]

    @api.model
    def browse_access_group(self,ids):
        access_group_ids = self.env['res.users'].sudo().browse(self.env.uid).commercial_partner_id.access_group_ids
        return self.env['product.template'].browse(ids).filtered(lambda p: not p.sudo().access_group_ids or access_group_ids & p.sudo().access_group_ids)


class product_product(models.Model):
    _inherit = 'product.product'

    access_group_ids = fields.Many2many(comodel_name='res.groups', string='Access Groups', help='Allowed groups to access this product')

    @api.multi
    def check_access_group(self,user):
        self.ensure_one()
        if self.sudo().access_group_ids:
            return True if len(user.sudo().commercial_partner_id.access_group_ids & self.sudo().access_group_ids) > 0 else False
        else:
            return True

    @api.model
    def search_access_group(self,domain, limit=0, offset=0, order=''):
        access_group_ids = self.env['res.users'].sudo().browse(self.env.uid).commercial_partner_id.access_group_ids
        return self.env['product.product'].search(domain, limit=limit, offset=offset, order=order).filtered(lambda p: not p.sudo().access_group_ids or access_group_ids & p.sudo().access_group_ids)

    @api.model
    def browse_access_group(self,ids):
        access_group_ids = self.env['res.users'].sudo().browse(self.env.uid).commercial_partner_id.access_group_ids
        return self.env['product.product'].browse(ids).filtered(lambda p: not p.sudo().access_group_ids or access_group_ids & p.sudo().access_group_ids)


class res_partner(models.Model):
    _inherit = "res.partner"

    access_group_ids = fields.Many2many(comodel_name='res.groups', string='Access Groups', help='Allowed groups to access products in webshop')
