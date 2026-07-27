from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardMaintenancePlan(models.Model):
    _name = "binaryguard.maintenance.plan"
    _description = "BinaryGuard Preventive Maintenance Plan"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "next_service_date, name"

    name = fields.Char(
        string="Plan Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
    )

    title = fields.Char(
        string="Maintenance Plan",
        required=True,
        tracking=True,
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        tracking=True,
    )

    contract_id = fields.Many2one(
        comodel_name="binaryguard.service.contract",
        string="Service Contract",
        tracking=True,
    )

    asset_ids = fields.Many2many(
        comodel_name="binaryguard.asset",
        relation="binaryguard_maintenance_asset_rel",
        column1="maintenance_plan_id",
        column2="asset_id",
        string="Covered Assets",
    )

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related Project",
        tracking=True,
    )

    assigned_technician_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
        domain=[("share", "=", False)],
        tracking=True,
    )

    maintenance_type = fields.Selection(
        selection=[
            ("inspection", "Inspection"),
            ("preventive", "Preventive Maintenance"),
            ("firmware", "Firmware Update"),
            ("cleaning", "Cleaning"),
            ("testing", "System Testing"),
            ("battery", "Battery Replacement"),
            ("license", "License Renewal"),
            ("other", "Other"),
        ],
        string="Maintenance Type",
        required=True,
        default="preventive",
        tracking=True,
    )

    frequency = fields.Selection(
        selection=[
            ("monthly", "Monthly"),
            ("quarterly", "Quarterly"),
            ("semiannual", "Every Six Months"),
            ("annual", "Annual"),
            ("custom", "Custom"),
        ],
        string="Frequency",
        required=True,
        default="quarterly",
        tracking=True,
    )

    interval_days = fields.Integer(
        string="Custom Interval in Days",
        default=90,
        tracking=True,
    )

    start_date = fields.Date(
        string="Plan Start Date",
        required=True,
        default=fields.Date.context_today,
        tracking=True,
    )

    last_service_date = fields.Date(
        string="Last Service Date",
        tracking=True,
    )

    next_service_date = fields.Date(
        string="Next Service Date",
        required=True,
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("active", "Active"),
            ("due", "Due"),
            ("in_progress", "In Progress"),
            ("completed", "Completed"),
            ("on_hold", "On Hold"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )

    estimated_hours = fields.Float(
        string="Estimated Hours",
        default=2.0,
        tracking=True,
    )

    site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    checklist = fields.Html(
        string="Maintenance Checklist",
    )

    service_notes = fields.Html(
        string="Service Notes",
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
                        "binaryguard.maintenance.plan"
                    )
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains("start_date", "next_service_date")
    def _check_dates(self):
        for plan in self:
            if (
                plan.start_date
                and plan.next_service_date
                and plan.next_service_date < plan.start_date
            ):
                raise ValidationError(
                    "The next service date cannot be earlier than the plan start date."
                )

    @api.constrains("interval_days", "estimated_hours")
    def _check_positive_values(self):
        for plan in self:
            if plan.interval_days < 1:
                raise ValidationError(
                    "The maintenance interval must be at least one day."
                )

            if plan.estimated_hours < 0:
                raise ValidationError(
                    "Estimated hours cannot be negative."
                )
