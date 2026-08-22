{
    "name": "Dayflow HR",
    "version": "19.0.1.0.0",
    "summary": "Human Resource Management System",
    "description": """
        Dayflow - Human Resource Management System
    """,
    "category": "Human Resources",
    "author": "FastTrack NMIT",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/employee_views.xml",
    ],
    "installable": True,
    "application": True,
}