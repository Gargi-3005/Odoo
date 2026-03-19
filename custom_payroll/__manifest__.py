{
    'name': 'Custom Payroll',
    'version': '18.0.1.0.0',
    'depends': ['om_hr_payroll'],
    'data': [
        'views/payslip_view.xml',
        'views/report_payslip_inherit.xml',
    ],
    'installable': True,
    'application': True,
}