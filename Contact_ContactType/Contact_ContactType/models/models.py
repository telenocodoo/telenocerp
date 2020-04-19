# -*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([('Employee','Employee'),
                                     ('Vendor','Vendor'),
                                     ('Customer','Customer'),
                                     ])
