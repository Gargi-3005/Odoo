from odoo import models, fields, api


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

   
    x_salary_pay_date = fields.Date(string="Salary Pay Date")

    x_total_working_days = fields.Float(
        string="Total Working Days",
        compute="_compute_days",
        store=True
    )
    x_paid_days = fields.Float(
        string="Paid Days",
        compute="_compute_days",
        store=True
    )
    x_paid_leave = fields.Float(
        string="Paid Leave",
        compute="_compute_days",
        store=True
    )
    x_unpaid_leave = fields.Float(
        string="Unpaid Leave",
        compute="_compute_days",
        store=True
    )
    x_leave_balance = fields.Float(
        string="Leave Balance",
        compute="_compute_days",
        store=True
    )

    carry_forward = fields.Float(string="Carry Forward Leaves")

    @api.depends(
        'worked_days_line_ids.number_of_days',
        'worked_days_line_ids.code',
        'carry_forward'
    )
    def _compute_days(self):
        for slip in self:
            total_days = 0.0
            paid_days = 0.0
            paid_leave = 0.0
            unpaid_leave = 0.0

            for line in slip.worked_days_line_ids:
                if line.code == 'WORK100':
                    total_days += line.number_of_days
                    paid_days += line.number_of_days

                elif line.code == 'LOP':
                    unpaid_leave += abs(line.number_of_days)

                elif line.code == 'PAID':
                    paid_leave += line.number_of_days

            monthly_leave = 1.0
            leaves_taken = unpaid_leave + paid_leave

            slip.x_total_working_days = total_days
            slip.x_paid_days = paid_days
            slip.x_paid_leave = paid_leave
            slip.x_unpaid_leave = unpaid_leave
            slip.x_leave_balance = slip.carry_forward + monthly_leave - leaves_taken

  
    @api.onchange('employee_id', 'date_from')
    def _onchange_employee_leave(self):
        for slip in self:
            if slip.employee_id and slip.date_from:
                last_slip = self.env['hr.payslip'].search(
                    [
                        ('employee_id', '=', slip.employee_id.id),
                        ('date_to', '<', slip.date_from)
                    ],
                    order='date_to desc',
                    limit=1
                )

                slip.carry_forward = last_slip.x_leave_balance if last_slip else 0.0