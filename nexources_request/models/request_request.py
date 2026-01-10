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
    _order = 'priority desc, deadline_date asc'

    name = fields.Char("Title")
    priority = fields.Selection(TICKET_PRIORITY, string='Priority', default='0', tracking=True)
    description = fields.Html("Description")
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        ondelete='cascade',
    )
    department_id = fields.Many2one(
        comodel_name='hr.department',
        string='Department',
        related='employee_id.department_id',
        store=True
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible',
        ondelete='set null'
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('in_progress', 'In Progress'),
            ('done', 'Done'),
            ('cancel', 'Cancelled'),
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
    deadline_date = fields.Datetime(
        string='Deadline Date'
    )
    validation_date = fields.Datetime(
        string='Validation Date'
    )

    def action_set_draft(self):
        print("Action : SET DRAFT")
        requests = self.filtered(lambda req: req.state in ['sent', 'cancel'])
        return requests.write({'state': 'draft'})

    def action_send(self):
        print("Action : SEND")
        self.write({'state': 'sent'})

    def action_in_progress(self):
        print("Action : IN PROGRESS")
        self.write({'state': 'in_progress'})

    def action_done(self):
        print("Action : DONE")
        self.write({'state': 'done'})

    def action_cancel(self):
        print("Action : CANCEL")
        self.write({'state': 'cancelled'})
