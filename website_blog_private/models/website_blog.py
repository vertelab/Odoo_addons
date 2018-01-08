# -*- coding: utf-8 -*-

from datetime import datetime
import difflib
import lxml
import random

from openerp import tools
from openerp import SUPERUSER_ID
from openerp.tools.translate import _
from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)

class Blog(models.Model):
    _inherit = 'blog.blog'

    security_type = fields.Selection([('public','Public'),('private','Private')], string='Security type', default='public', required=True)
    group_ids = fields.Many2many(comodel_name='res.groups', string="Authorized Groups")

    def all_tags(self, cr, uid, ids, min_limit=1, context=None):
        user=self.pool.get('res.users').browse(cr, uid, uid, context=context)
        group_ids=[g.id for g in user.groups_id]
        req = """
            SELECT
                p.blog_id, count(*), r.blog_tag_id
            FROM
                blog_post_blog_tag_rel r
                    join blog_post p on r.blog_post_id=p.id
                    join blog_blog b on p.blog_id=b.id
            WHERE
                p.blog_id in %s AND
                (b.security_type = 'public' OR (b.security_type = 'private' AND b.id in (SELECT bg.blog_blog_id FROM blog_blog_res_groups_rel bg WHERE bg.res_groups_id IN %s ) ))

            GROUP BY
                p.blog_id,
                r.blog_tag_id
            ORDER BY
                count(*) DESC
        """
        cr.execute(req, [tuple(ids), tuple(group_ids)])
        tag_by_blog = {i: [] for i in ids}
        for blog_id, freq, tag_id in cr.fetchall():
            if freq >= min_limit:
                tag_by_blog[blog_id].append(tag_id)

        tag_obj = self.pool['blog.tag']
        for blog_id in tag_by_blog:
            tag_by_blog[blog_id] = tag_obj.browse(cr, uid, tag_by_blog[blog_id], context=context)
        return tag_by_blog


class BlogPost(models.Model):
    _inherit = 'blog.post'

    security_type = fields.Selection([('public','Public'),('private','Private')], string='Security type', default='public', required=True)
    group_ids = fields.Many2many('res.groups', string="Authorized Groups")

    @api.multi
    def check_access_group(self, user):
        self.ensure_one()
        if self.sudo().security_type == 'public':
            return True
        else:
            return True if len(user.sudo().commercial_partner_id.access_group_ids & self.sudo().group_ids) > 0 else False
