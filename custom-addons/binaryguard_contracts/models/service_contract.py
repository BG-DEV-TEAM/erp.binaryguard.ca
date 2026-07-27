from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardServiceContract(models.Model):
    _name = "binaryguard.service.contract"
    _description = "BinaryGuard Service Contract"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_date desc, name desc"

    name = fields.Char(
        string="Contract Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
    )

    contract_title = fields.Char(
        string="Contract Title",
        required=True,
        tracking=True,
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        tracking=True,
    )

    contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer Contact",
        tracking=True,
    )

    contract_type = fields.Selection(
        selection=[
            ("amc", "Annual Maintenance Contract"),
            ("support", "Technical Support Contract"),
            ("preventive", "Preventive Maintenance Contract"),
            ("warranty", "Warranty Support"),
            ("managed_service", "Managed Service Contract"),
            ("other", "Other"),
        ],
        string="Contract Type",
        required=True,
        default="amc",
        tracking=True,
    )

    start_date = fields.Date(
        string="Start Date",
        required=True,
        tracking=True,
    )

    end_date = fields.Date(
        string="End Date",
        required=True,
        tracking=True,
    )

    renewal_date = fields.Date(
        string="Renewal Review Date",
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("on_hold", "On Hold"),
            ("expired", "Expired"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )

    billing_frequency = fields.Selection(
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("semiannual", "Semi-Annual"),
            ("annual", "Annual"),
            ("one_time", "One-Time"),
        ],
        string="Billing Frequency",
        default="annual",
        tracking=True,
    )

    contract_value = fields.Monetary(
        string="Contract Value",
        currency_field="currency_id",
        tracking=True,
    )

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )

    sale_order_id = fields.Many2one(
        comodel_name="sale.order",
        string="Related Sales Order",
        tracking=True,
    )

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related Project",
        tracking=True,
    )

    invoice_id = fields.Many2one(
        comodel_name="account.move",
        string="Related Invoice",
        domain=[("move_type", "in", ["out_invoice", "out_refund"])],
        tracking=True,
    )

    asset_ids = fields.Many2many(
        comodel_name="binaryguard.asset",
        relation="binaryguard_contract_asset_rel",
        column1="contract_id",
        column2="asset_id",
        string="Covered Assets",
    )

    assigned_manager_id = fields.Many2one(
        comodel_name="res.users",
        string="Contract Manager",
        domain=[("share", "=", False)],
        tracking=True,
    )

    response_time_hours = fields.Float(
        string="Response Time (Hours)",
        default=4.0,
        tracking=True,
    )

    resolution_time_hours = fields.Float(
        string="Target Resolution Time (Hours)",
        default=24.0,
        tracking=True,
    )

    preventive_visits_per_year = fields.Integer(
        string="Preventive Visits per Year",
        default=2,
        tracking=True,
    )

    remote_support_included = fields.Boolean(
        string="Remote Support Included",
        default=True,
        tracking=True,
    )

    site_visits_included = fields.Boolean(
        string="Site Visits Included",
        tracking=True,
    )

    parts_included = fields.Boolean(
        string="Replacement Parts Included",
        tracking=True,
    )

    after_hours_support = fields.Boolean(
        string="After-Hours Support",
        tracking=True,
    )

    scope_of_service = fields.Html(
        string="Scope of Service",
    )

    exclusions = fields.Html(
        string="Exclusions",
    )

    internal_notes = fields.Text(
        string="Internal Notes",
    )

    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.service.contract"
                    )
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains("start_date", "end_date")
    def _check_contract_dates(self):
        for contract in self:
            if (
                contract.start_date
                and contract.end_date
                and contract.end_date < contract.start_date
            ):
                raise ValidationError(
                    "The contract end date cannot be earlier than the start date."
                )

    @api.constrains(
        "response_time_hours",
        "resolution_time_hours",
        "preventive_visits_per_year",
    )
    def _check_positive_values(self):
        for contract in self:
            if contract.response_time_hours < 0:
                raise ValidationError(
                    "Response time cannot be negative."
                )

            if contract.resolution_time_hours < 0:
                raise ValidationError(
                    "Resolution time cannot be negative."
                )

            if contract.preventive_visits_per_year < 0:
                raise ValidationError(
                    "Preventive visits cannot be negative."
                )
