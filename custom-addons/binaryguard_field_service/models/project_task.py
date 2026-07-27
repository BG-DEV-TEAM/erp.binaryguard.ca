from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    binaryguard_customer = fields.Many2one(
        "res.partner",
        string="Customer"
    )

    binaryguard_site = fields.Char(
        string="Installation Site"
    )

    binaryguard_system = fields.Char(
        string="System"
    )

    binaryguard_technician = fields.Many2one(
        "res.users",
        string="Technician"
    )

    binaryguard_visit_date = fields.Datetime(
        string="Visit Date"
    )

    binaryguard_service_status = fields.Selection(
        [
            ("scheduled", "Scheduled"),
            ("travelling", "Travelling"),
            ("working", "Working"),
            ("testing", "Testing"),
            ("completed", "Completed"),
        ],
        default="scheduled",
        string="Service Status",
    )

    binaryguard_notes = fields.Text(
        string="Technician Notes"
    )
