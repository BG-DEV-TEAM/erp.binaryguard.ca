from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardClient(models.Model):
    _name = "binaryguard.client"
    _description = "BinaryGuard Client"
    _order = "name"

    name = fields.Char(
        string="Client Name",
        required=True,
        index=True,
    )

    organization = fields.Char(
        string="Organization",
    )

    email = fields.Char(
        string="Email",
    )

    phone = fields.Char(
        string="Phone",
    )

    active = fields.Boolean(
        default=True,
    )

    notes = fields.Text(
        string="Notes",
    )
    _name_unique = models.Constraint(
    "UNIQUE(name)",
    "A client with this name already exists.",

    )
    @api.constrains("email")
    def _check_email_format(self):
        for record in self:
            if record.email and "@" not in record.email:
                raise ValidationError("Enter a valid email address.")
