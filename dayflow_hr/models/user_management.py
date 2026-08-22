from odoo import api, fields, models


class DayflowUserManagement(models.Model):
    _name = "dayflow.user.management"
    _description = "Dayflow User Management"

    user_id = fields.Many2one(
        "res.users",
        string="User",
        required=True,
        ondelete="cascade",
    )
    employee_id = fields.Many2one(
        "dayflow.employee",
        string="Employee",
        required=True,
        ondelete="cascade",
    )
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
    active = fields.Boolean(
        string="Active",
        default=True,
    )

    _sql_constraints = [
        (
            "unique_managed_user",
            "unique(user_id)",
            "Each user can have only one Dayflow user-management record.",
        ),
        (
            "unique_managed_employee",
            "unique(employee_id)",
            "Each employee can have only one Dayflow user-management record.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)

        for record in records:
            if record.user_id:
                record._apply_user_role()

        return records

    def write(self, vals):
        result = super().write(vals)

        if "role" in vals or "user_id" in vals:
            for record in self:
                if record.user_id:
                    record._apply_user_role()

        return result

    def _apply_user_role(self):
        role_groups = {
            "employee": "dayflow_hr.group_dayflow_employee",
            "hr": "dayflow_hr.group_dayflow_hr",
            "admin": "dayflow_hr.group_dayflow_admin",
        }

        group_xml_id = role_groups.get(self.role)

        if not group_xml_id:
            return

        group = self.env.ref(group_xml_id, raise_if_not_found=False)

        if not group:
            return

        all_dayflow_groups = self.env["res.groups"].search(
            [
                (
                    "id",
                    "in",
                    [
                        self.env.ref(
                            "dayflow_hr.group_dayflow_employee"
                        ).id,
                        self.env.ref(
                            "dayflow_hr.group_dayflow_hr"
                        ).id,
                        self.env.ref(
                            "dayflow_hr.group_dayflow_admin"
                        ).id,
                    ],
                )
            ]
        )

        self.user_id.groups_id = [
            (3, group_record.id)
            for group_record in all_dayflow_groups
            if group_record.id != group.id
        ]

        self.user_id.groups_id = [(4, group.id)]