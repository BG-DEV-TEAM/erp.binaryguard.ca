from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    binaryguard_project = fields.Char(
        string="Project"
    )

    binaryguard_site = fields.Char(
        string="Site"
    )

    binaryguard_installer = fields.Char(
        string="Installer"
    )

    binaryguard_notes = fields.Text(
        string="Installation Notes"
    )
