from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    binaryguard_project = fields.Char(
        string="Project Reference"
    )

    binaryguard_site = fields.Char(
        string="Installation Site"
    )

    binaryguard_client = fields.Char(
        string="Client"
    )

    binaryguard_requested_by = fields.Char(
        string="Requested By"
    )

    binaryguard_notes = fields.Text(
        string="Purchase Notes"
    )
