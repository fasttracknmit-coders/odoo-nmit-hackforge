{
    "name": "Dayflow HR",
<<<<<<< HEAD
    "version": "1.0",
    "category": "Human Resources",
    "summary": "Dayflow Intelligent HR Management System",

    "depends": [
        "base",
        "hr",
    ],

    "data": [
        "security/ir.model.access.csv",
        "views/ai_views.xml",
    ],

    "installable": True,
    "application": True,
}
=======
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
'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/employee_views.xml',
        'views/payroll_views.xml',
        'reports/payroll_report.xml',  # <--- Add this line here
    ],
>>>>>>> origin/main
