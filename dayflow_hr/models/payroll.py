from odoo import models, fields, api

class DayflowPayroll(models.Model):
    _name = 'dayflow.payroll'
    _description = 'Employee Payroll Record'

    employee_id = fields.Many2one('dayflow.employee', string="Employee", required=True)
    month = fields.Char(string="Month/Year", help="e.g., Aug-2026", required=True)
    
    basic_salary = fields.Float(string="Basic Salary", required=True, default=0.0)
    allowances = fields.Float(string="Allowances", default=0.0)
    deductions = fields.Float(string="Deductions", default=0.0)
    
    net_salary = fields.Float(string="Net Salary", compute='_compute_net_salary', store=True)
    
    status = fields.Selection([
        ('draft', 'Draft'),
        ('paid', 'Paid')
    ], string="Status", default='draft')

    @api.depends('basic_salary', 'allowances', 'deductions')
    def _compute_net_salary(self):
        for record in self:
            record.net_salary = record.basic_salary + record.allowances - record.deductions