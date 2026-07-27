from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardAccessCard(models.Model):
    _name = "binaryguard.access.card"
    _description = "BinaryGuard Access Card"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name desc"

    name = fields.Char(
        string="Record Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
    )

    card_number = fields.Char(
        string="Card Number",
        required=True,
        index=True,
        tracking=True,
    )

    facility_code = fields.Char(
        string="Facility Code",
        tracking=True,
    )

    card_format = fields.Char(
        string="Card Format",
        tracking=True,
    )

    card_type = fields.Selection(
        selection=[
            ("employee", "Employee Card"),
            ("contractor", "Contractor Card"),
            ("visitor", "Visitor Card"),
            ("temporary", "Temporary Card"),
            ("master", "Master Card"),
            ("other", "Other"),
        ],
        string="Card Type",
        required=True,
        default="employee",
        tracking=True,
    )

    ownership = fields.Selection(
        selection=[
            ("customer", "Customer Owned"),
            ("binaryguard", "BinaryGuard Owned"),
        ],
        string="Ownership",
        required=True,
        default="customer",
        tracking=True,
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        tracking=True,
    )

    cardholder_name = fields.Char(
        string="Cardholder Name",
        required=True,
        tracking=True,
    )

    employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Employee",
        tracking=True,
    )

    department = fields.Char(
        string="Department",
        tracking=True,
    )

    job_title = fields.Char(
        string="Job Title",
        tracking=True,
    )

    email = fields.Char(
        string="Email",
        tracking=True,
    )

    phone = fields.Char(
        string="Phone",
        tracking=True,
    )

    site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    building = fields.Char(
        string="Building",
        tracking=True,
    )

    access_level = fields.Char(
        string="Access Level",
        tracking=True,
    )

    issue_date = fields.Date(
        string="Issue Date",
        tracking=True,
    )

    activation_date = fields.Date(
        string="Activation Date",
        tracking=True,
    )

    expiry_date = fields.Date(
        string="Expiry Date",
        tracking=True,
    )

    return_date = fields.Date(
        string="Return Date",
        tracking=True,
    )

    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("requested", "Requested"),
            ("approved", "Approved"),
            ("active", "Active"),
            ("suspended", "Suspended"),
            ("expired", "Expired"),
            ("lost", "Lost"),
            ("stolen", "Stolen"),
            ("returned", "Returned"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )

    related_asset_id = fields.Many2one(
        comodel_name="binaryguard.asset",
        string="Related Asset",
        tracking=True,
    )

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related Project",
        tracking=True,
    )

    contract_id = fields.Many2one(
        comodel_name="binaryguard.service.contract",
        string="Service Contract",
        tracking=True,
    )

    helpdesk_ticket_id = fields.Many2one(
        comodel_name="binaryguard.helpdesk.ticket",
        string="Helpdesk Ticket",
        tracking=True,
    )

    assigned_by_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned By",
        domain=[("share", "=", False)],
        tracking=True,
    )

    approved_by_id = fields.Many2one(
        comodel_name="res.users",
        string="Approved By",
        domain=[("share", "=", False)],
        tracking=True,
    )

    notes = fields.Html(
        string="Notes",
    )

    active = fields.Boolean(default=True)

    _card_number_unique = models.Constraint(
        "UNIQUE(card_number)",
        "The card number must be unique.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.access.card"
                    )
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains(
        "issue_date",
        "activation_date",
        "expiry_date",
        "return_date",
    )
    def _check_card_dates(self):
        for card in self:
            if (
                card.issue_date
                and card.activation_date
                and card.activation_date < card.issue_date
            ):
                raise ValidationError(
                    "The activation date cannot be earlier than the issue date."
                )

            if (
                card.activation_date
                and card.expiry_date
                and card.expiry_date < card.activation_date
            ):
                raise ValidationError(
                    "The expiry date cannot be earlier than the activation date."
                )

            if (
                card.issue_date
                and card.return_date
                and card.return_date < card.issue_date
            ):
                raise ValidationError(
                    "The return date cannot be earlier than the issue date."
                )
