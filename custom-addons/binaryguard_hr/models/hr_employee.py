from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    binaryguard_employee_no = fields.Char(
        string="Employee ID"
    )

    binaryguard_department_code = fields.Char(
        string="Department Code"
    )

    binaryguard_security_clearance = fields.Selection(
        [
            ("none", "None"),
            ("basic", "Basic"),
            ("confidential", "Confidential"),
            ("secret", "Secret"),
        ],
        string="Security Clearance",
        default="basic",
    )

    binaryguard_certification = fields.Char(
        string="Primary Certification"
    )

    binaryguard_company_vehicle = fields.Boolean(
        string="Company Vehicle Assigned"
    )

    binaryguard_field_technician = fields.Boolean(
        string="Field Technician"
    )
