from odoo import fields, models


class ProjectProject(models.Model):
    _inherit = "project.project"

    binaryguard_site = fields.Char(
        string="Installation Site"
    )

    binaryguard_contract = fields.Char(
        string="Contract Reference"
    )

    binaryguard_customer = fields.Many2one(
        "res.partner",
        string="Customer"
    )

    binaryguard_project_manager = fields.Many2one(
        "res.users",
        string="Project Manager"
    )

    binaryguard_start_date = fields.Date(
        string="Installation Start"
    )

    binaryguard_end_date = fields.Date(
        string="Installation End"
    )

    binaryguard_status = fields.Selection(
        [
            ("planning", "Planning"),
            ("installation", "Installation"),
            ("testing", "Testing"),
            ("handover", "Client Handover"),
            ("completed", "Completed"),
        ],
        default="planning",
        string="Project Status",
    )
