# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # search for getting own contacts and my team contacts
        lst = []
        if self.sudo().env['ir.module.module'].search([('name', '=', 'hr')]).state == 'installed':
            # check if hr module installed or not
           employee_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)])
           if employee_user_id:
               # check if employee have parent or no
               parent = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).parent_id
               if not parent:
                   if self.env.user.is_allowed_to_view_own_contacts:
                       args += [('create_uid', '=', self.env.user.id)]
               else:
                   # get my contacts and my team
                   current_user_id = self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]).id
                   related_employee_id = self.env['hr.employee'].search([('parent_id.id', '=', current_user_id)])
                   for employee_id in related_employee_id:
                       lst.append(employee_id.user_id.id)
                   lst.append(self.env.user.id)
                   args += [('create_uid', 'in', lst)]
           else:
               if self.env.user.is_allowed_to_view_own_contacts:
                   args += [('create_uid', '=', self.env.user.id)]
        else:
            # get my own document if hr not installed
            if self.env.user.is_allowed_to_view_own_contacts:
                args += [('create_uid', '=', self.env.user.id)]
        return super(ResPartner, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def create(self, vals):
        # inherit create function and limit create for some users
        res = super(ResPartner, self).create(vals)
        if res.env.user.no_contact_create:
            raise UserError(_("You are not allowed to create"))
        return res

    def write(self, vals):
        # inherit write function and limit write for some users
        result = super(ResPartner, self).write(vals)
        for rec in self:
            user = rec.env.user
            if user.is_allowed_to_edit:
                raise UserError(_("You are not allowed to edit!!"))
            if user.is_allowed_to_view_own_contacts and self.create_uid != user:
                raise UserError(_("You are not manager to edit that record!!"))
        return result

    def unlink(self):
        # inherit delete function and limit delete for some users
        user = self.env.user
        if user.is_allowed_to_delete:
            raise UserError(_("You are not allowed to delete!!"))
        if user.is_allowed_to_view_own_contacts and self.create_uid != user:
            raise UserError(_("You are not manager to delete that record!!"))
        return super(ResPartner, self).unlink()


class ResUsers(models.Model):
    _inherit = 'res.users'

    no_contact_create = fields.Boolean(string='Create Contact')
    is_allowed_to_create = fields.Boolean()
    is_allowed_to_view_own_contacts = fields.Boolean(string='View Contact')
    is_allowed_to_edit = fields.Boolean(string='Edit Contact')
    is_allowed_to_delete = fields.Boolean(string='Delete Contact')
    is_allowed_to_import = fields.Boolean()
    is_allowed_to_export = fields.Boolean()
