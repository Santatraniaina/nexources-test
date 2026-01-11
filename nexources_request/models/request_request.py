from odoo import models, fields, _
from odoo.exceptions import UserError

PRIORITY = [
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


    name = fields.Char("Title", required=True, tracking=True)
    priority = fields.Selection(PRIORITY, string='Priority', default='1', tracking=True)
    description = fields.Html("Description")
    employee_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Employee',
        tracking=True,
        required=True,
        default=lambda self: self.env.user.employee_id.id
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
    manager_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Manager',
        related='employee_id.parent_id'
    )
    responsible_id = fields.Many2one(
        comodel_name='hr.employee',
        string='Responsible',
        tracking=True,
        help="Employee responsible for handling the request"
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
        tracking=True
    )
    deadline_date = fields.Datetime(
        string='Deadline Date',
        tracking=True
    )
    validation_date = fields.Datetime(
        string='Validation Date',
        tracking=True
    )

    def action_set_draft(self):
        requests = self.filtered(lambda req: req.state in ['sent', 'cancel'])
        return requests.write({'state': 'draft'})

    def action_send(self):
        self.write({'state': 'sent'})

    def action_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        self.write({
            'state': 'done',
            'validation_date': fields.Datetime.now()
        })

    def action_cancel(self):
        self.write({
            'state': 'cancel',
            'validation_date': False
        })

    def unlink(self):
        for request in self:
            if request.state not in ['draft', 'cancel']:
                raise UserError(_("You can only delete requests in Draft or Cancelled state."))
        return super(Request, self).unlink()