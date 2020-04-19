# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project')
