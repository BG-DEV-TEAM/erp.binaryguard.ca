from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    binaryguard_project = fields.Char(
        string="Project"
    )

    binaryguard_customer_po = fields.Char(
        string="Customer PO"
    )

    binaryguard_installation_date = fields.Date(
        string="Installation Date"
    )

    binaryguard_assigned_technician = fields.Many2one(
        "res.users",
        string="Assigned Technician"
    )

    binaryguard_installation_status = fields.Selection(
        [
            ("pending", "Pending"),
            ("scheduled", "Scheduled"),
            ("installed", "Installed"),
            ("completed", "Completed"),
        ],
        default="pending",
        string="Installation Status",
    )
