from odoo import models, fields

TICKET_PRIORITY = [
    ('0', 'Low priority'),
    ('1', 'Medium priority'),
    ('2', 'High priority'),
    ('3', 'Urgent'),
]

class Request(models.Model):
    _name = 'request.request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'request.request'

    name = fields.Char("Title")
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0', tracking=True)
    description = fields.Html("Description")
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        ondelete='cascade',
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible',
        ondelete='set null'
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='State',
        default='draft',
        required=True,
    )
    creation_date = fields.Datetime(
        string='Creation Date',
        default=fields.Datetime.now,
        required=True,
    )
    validation_date = fields.Datetime(
        string='Validation Date'
    )

