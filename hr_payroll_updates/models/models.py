# -*- coding: utf-8 -*-

from odoo import models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        res = super(HrPayslip, self).action_payslip_done()
        if self.move_id:
            for rec in self.move_id:
                if rec.line_ids:
                    for line in rec.line_ids:
                        if self.employee_id.address_home_id:
                            line.partner_id = self.employee_id.address_home_id.id
        return res
