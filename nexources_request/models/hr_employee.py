from odoo import fields, models, api


class HREmployee(models.Model):
    _inherit = 'hr.employee'

    request_ids = fields.One2many(
        comodel_name='request.request',
        inverse_name='employee_id',
        string='Requests'
    )
    request_count = fields.Integer(
        string='Request Count',
        compute='_compute_request_count'
    )

    @api.depends('request_ids')
    def _compute_request_count(self):
        for employee in self:
            employee.request_count = len(employee.request_ids)

    def action_view_requests(self):
        self.ensure_one()
        if self.request_count == 1:
            return {
                'name': 'Request',
                'type': 'ir.actions.act_window',
                'res_model': 'request.request',
                'view_mode': 'form',
                'res_id': self.request_ids[0].id,
                'context': {'default_employee_id': self.id},
            }
        else:
            return {
                'name': 'Requests',
                'type': 'ir.actions.act_window',
                'res_model': 'request.request',
                'view_mode': 'list,form',
                'domain': [('employee_id', '=', self.id)],
                'context': {'default_employee_id': self.id},
            }