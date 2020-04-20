# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    q_name = fields.Char('Quotation Name', size=50)

    # @api.constrains('q_name')
    # def _check_q_name(self):
    #     if len(self.q_name) > 50:
    #         raise UserError(_('Number Of Characters In Quotation Name Must Not Exceed 50'))
