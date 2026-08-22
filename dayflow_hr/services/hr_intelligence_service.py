from .rules_engine import generate_all_insights
from .insight_service import create_insight_records


def run_hr_intelligence(env):
    """
    Collect HR data from Odoo, run deterministic HR rules,
    and store generated insights in the Dayflow AI Insight model.
    """

    # ---------------------------------------------------------
    # Attendance
    # ---------------------------------------------------------

    attendance_records = []

    Attendance = env["hr.attendance"]

    attendances = Attendance.search([], limit=500)

    for attendance in attendances:
        if not attendance.employee_id:
            continue

        employee = attendance.employee_id
        late = False

        if attendance.check_in:
            calendar = employee.resource_calendar_id

            if calendar:
                check_in = attendance.check_in
                weekday = check_in.weekday()

                scheduled = calendar.attendance_ids.filtered(
                    lambda line:
                    int(line.dayofweek) == weekday
                    and line.hour_from is not False
                )

                if scheduled:
                    expected_hour = min(
                        scheduled.mapped("hour_from")
                    )

                    check_in_hour = (
                        check_in.hour
                        + check_in.minute / 60.0
                    )

                    late = check_in_hour > expected_hour

        attendance_records.append({
            "employee_id": employee.id,
            "employee_name": employee.name,
            "late": late,
        })

    # ---------------------------------------------------------
    # Leave
    # ---------------------------------------------------------

    leave_records = []

    Leave = env["hr.leave"]

    leaves = Leave.search([], limit=500)

    for leave in leaves:
        if not leave.employee_id:
            continue

        department = (
            leave.employee_id.department_id.name
            if leave.employee_id.department_id
            else None
        )

        if not department:
            continue

        leave_records.append({
            "employee_id": leave.employee_id.id,
            "department": department,
            "date": (
                leave.request_date_from.isoformat()
                if leave.request_date_from
                else None
            ),
            "status": leave.state,
        })

    # ---------------------------------------------------------
    # Payroll
    # ---------------------------------------------------------
    # Keep this compatible with the base HR module.
    # Actual payroll integration can be added later.

    payroll_records = []

    for attendance in attendances:
        if not attendance.employee_id:
            continue

        payroll_records.append({
            "employee_id": attendance.employee_id.id,
            "attendance_discrepancy": False,
            "leave_discrepancy": False,
        })

    # ---------------------------------------------------------
    # Run rules engine
    # ---------------------------------------------------------

    insights = generate_all_insights(
        attendance_records=attendance_records,
        leave_records=leave_records,
        payroll_records=payroll_records,
    )

    # ---------------------------------------------------------
    # Store insights in Odoo
    # ---------------------------------------------------------

    return create_insight_records(env, insights)