from odoo import http
from odoo.http import request


class DayflowAIController(http.Controller):

    @http.route(
        "/dayflow/ai/chat",
        type="json",
        auth="user",
        methods=["POST"],
    )
    def ai_chat(self, message=None, **kwargs):

        if not message:
            return {
                "success": False,
                "reply": "Please enter a question."
            }

        message = message.lower().strip()

        Insight = request.env["dayflow.ai.insight"]

        # Attendance questions
        if any(word in message for word in [
            "attendance",
            "late",
            "check-in",
            "checkin",
        ]):
            records = Insight.search(
                [
                    ("insight_type", "=", "attendance"),
                    ("status", "=", "open"),
                ],
                limit=10,
            )

            if not records:
                reply = "No open attendance issues were found."

            else:
                lines = [
                    f"Found {len(records)} attendance issue(s):"
                ]

                for record in records:
                    employee = (
                        record.employee_id.name
                        if record.employee_id
                        else "Unknown employee"
                    )

                    lines.append(
                        f"- {record.name}: "
                        f"{employee} — "
                        f"{record.severity.upper()}"
                    )

                reply = "\n".join(lines)

            return {
                "success": True,
                "reply": reply,
            }

        # Leave questions
        if "leave" in message or "holiday" in message:
            records = Insight.search(
                [
                    ("insight_type", "=", "leave"),
                    ("status", "=", "open"),
                ],
                limit=10,
            )

            if not records:
                reply = "No open leave conflicts were found."

            else:
                lines = [
                    f"Found {len(records)} leave issue(s):"
                ]

                for record in records:
                    lines.append(
                        f"- {record.name}: "
                        f"{record.message}"
                    )

                reply = "\n".join(lines)

            return {
                "success": True,
                "reply": reply,
            }

        # Payroll questions
        if "payroll" in message or "salary" in message:
            records = Insight.search(
                [
                    ("insight_type", "=", "payroll"),
                    ("status", "=", "open"),
                ],
                limit=10,
            )

            if not records:
                reply = "No open payroll risks were found."

            else:
                lines = [
                    f"Found {len(records)} payroll issue(s):"
                ]

                for record in records:
                    employee = (
                        record.employee_id.name
                        if record.employee_id
                        else "Unknown employee"
                    )

                    lines.append(
                        f"- {record.name}: "
                        f"{employee} — "
                        f"{record.severity.upper()}"
                    )

                reply = "\n".join(lines)

            return {
                "success": True,
                "reply": reply,
            }

        # General HR summary
        if any(word in message for word in [
            "summary",
            "problem",
            "issues",
            "insights",
            "report",
        ]):
            records = Insight.search(
                [
                    ("status", "=", "open"),
                ],
                limit=20,
            )

            if not records:
                reply = "There are currently no open HR issues."

            else:
                attendance = sum(
                    1 for r in records
                    if r.insight_type == "attendance"
                )

                leave = sum(
                    1 for r in records
                    if r.insight_type == "leave"
                )

                payroll = sum(
                    1 for r in records
                    if r.insight_type == "payroll"
                )

                reply = (
                    "HR Action Center summary:\n"
                    f"- Attendance issues: {attendance}\n"
                    f"- Leave issues: {leave}\n"
                    f"- Payroll issues: {payroll}\n"
                    f"- Total open issues: {len(records)}"
                )

            return {
                "success": True,
                "reply": reply,
            }

        return {
            "success": True,
            "reply": (
                "I can help with HR insights. "
                "Try asking about attendance, "
                "leave, payroll, or give me an HR summary."
            ),
        }