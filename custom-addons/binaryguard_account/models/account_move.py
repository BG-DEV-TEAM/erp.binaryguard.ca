from odoo import fields, models


class AccountMove(models.Model):
    _inherit = "account.move"

    binaryguard_project = fields.Char(
        string="Project"
    )

    binaryguard_contract = fields.Char(
        string="Contract Reference"
    )

    binaryguard_site = fields.Char(
        string="Site"
    )

    binaryguard_service_ticket = fields.Char(
        string="Service Ticket"
    )

    binaryguard_po_number = fields.Char(
        string="Customer PO"
    )
