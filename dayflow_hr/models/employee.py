from odoo import fields, models


class DayflowEmployee(models.Model):
    _name = "dayflow.employee"
    _description = "Dayflow Employee"
    _rec_name = "name"

    _sql_constraints = [
        (
            "unique_employee_id",
            "unique(employee_id)",
            "Employee ID must be unique.",
        ),
    ]

    name = fields.Char(string="Employee Name", required=True)
    employee_id = fields.Char(
        string="Employee ID",
        required=True,
        copy=False,
        index=True,
    )
    user_id = fields.Many2one(
        "res.users",
        string="User Account",
        ondelete="set null",
    )
    email = fields.Char(string="Email")
    phone = fields.Char(string="Phone")
    address = fields.Text(string="Address")
    job_title = fields.Char(string="Job Title")
    department = fields.Char(string="Department")
    joining_date = fields.Date(string="Joining Date")
    salary = fields.Float(string="Salary")
    profile_picture = fields.Image(string="Profile Picture")
    role = fields.Selection(
        [
            ("employee", "Employee"),
            ("hr", "HR Officer"),
            ("admin", "Admin"),
        ],
        string="Role",
        required=True,
        default="employee",
    )
    active = fields.Boolean(string="Active", default=True)