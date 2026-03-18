from odoo import models, fields

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    x_salary_pay_date = fields.Date(string="Salary Pay Date")
    x_total_working_days = fields.Float(string="Total Working Days")
    x_paid_days = fields.Float(string="Paid Days")
    x_paid_leave = fields.Float(string="Paid Leave")
    x_unpaid_leave = fields.Float(string="Unpaid Leave")
    x_leave_balance = fields.Float(string= "Leave Balance ")