# -*- coding: utf-8 -*-

from odoo import models


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    def action_payslip_done(self):
        # inherit payslip function and add partner in journal line
        res = super(HrPayslip, self).action_payslip_done()
        for record in self:
            if record.move_id:
                if record.employee_id.address_home_id:
                    record.move_id.partner_id = record.employee_id.address_home_id.id
                for rec in record.move_id:
                    if rec.line_ids:
                        for line in rec.line_ids:
                            if record.employee_id.address_home_id:
                                line.partner_id = record.employee_id.address_home_id.id
        return res
