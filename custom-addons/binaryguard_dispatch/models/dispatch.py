from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardDispatch(models.Model):
    _name = "binaryguard.dispatch"
    _description = "BinaryGuard Technician Dispatch"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, scheduled_start asc, create_date desc"

    name = fields.Char(
        string="Dispatch Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
    )

    title = fields.Char(
        string="Dispatch Title",
        required=True,
        tracking=True,
    )

    dispatch_type = fields.Selection(
        [
            ("emergency", "Emergency Call"),
            ("service", "Service Call"),
            ("installation", "Installation"),
            ("maintenance", "Preventive Maintenance"),
            ("inspection", "Inspection"),
            ("warranty", "Warranty Work"),
            ("project", "Project Work"),
            ("remote", "Remote Support"),
            ("other", "Other"),
        ],
        required=True,
        default="service",
        tracking=True,
    )

    priority = fields.Selection(
        [
            ("0", "Low"),
            ("1", "Medium"),
            ("2", "High"),
            ("3", "Emergency"),
        ],
        required=True,
        default="1",
        tracking=True,
    )

    state = fields.Selection(
        [
            ("draft", "Draft"),
            ("assigned", "Assigned"),
            ("accepted", "Accepted"),
            ("on_route", "On Route"),
            ("on_site", "On Site"),
            ("work_started", "Work Started"),
            ("work_completed", "Work Completed"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )

    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        tracking=True,
    )

    site_location = fields.Char(
        string="Site Location",
        required=True,
        tracking=True,
    )

    assigned_technician_id = fields.Many2one(
        "res.users",
        string="Primary Technician",
        domain=[("share", "=", False)],
        tracking=True,
    )

    dispatcher_id = fields.Many2one(
        "res.users",
        string="Dispatcher",
        default=lambda self: self.env.user,
        tracking=True,
    )

    scheduled_start = fields.Datetime(
        string="Scheduled Start",
        required=True,
        tracking=True,
    )

    scheduled_end = fields.Datetime(
        string="Scheduled End",
        tracking=True,
    )

    actual_start = fields.Datetime(
        string="Actual Start",
        readonly=True,
    )

    actual_end = fields.Datetime(
        string="Actual End",
        readonly=True,
    )

    estimated_hours = fields.Float(
        string="Estimated Hours",
        default=1.0,
    )

    dispatch_instructions = fields.Html(
        string="Dispatch Instructions",
    )

    technician_notes = fields.Html(
        string="Technician Notes",
    )

    completion_summary = fields.Html(
        string="Completion Summary",
    )

    follow_up_required = fields.Boolean(
        string="Follow-Up Required",
    )

    follow_up_notes = fields.Text(
        string="Follow-Up Notes",
    )

    active = fields.Boolean(default=True)

    _sql_constraints = [
        (
            "binaryguard_dispatch_name_unique",
            "unique(name)",
            "The dispatch number must be unique.",
        ),
    ]

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.dispatch"
                    )
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains("scheduled_start", "scheduled_end")
    def _check_schedule_dates(self):
        for record in self:
            if (
                record.scheduled_start
                and record.scheduled_end
                and record.scheduled_end < record.scheduled_start
            ):
                raise ValidationError(
                    "Scheduled end cannot be earlier than scheduled start."
                )

    def action_assign(self):
        for record in self:
            if not record.assigned_technician_id:
                raise ValidationError(
                    "Select a technician before assigning the dispatch."
                )
        self.write({"state": "assigned"})

    def action_accept(self):
        self.write({"state": "accepted"})

    def action_on_route(self):
        self.write({"state": "on_route"})

    def action_on_site(self):
        self.write({"state": "on_site"})

    def action_start_work(self):
        self.write({
            "state": "work_started",
            "actual_start": fields.Datetime.now(),
        })

    def action_complete_work(self):
        for record in self:
            if not record.completion_summary:
                raise ValidationError(
                    "Enter a completion summary before completing the job."
                )

        self.write({
            "state": "work_completed",
            "actual_end": fields.Datetime.now(),
        })

    def action_close(self):
        self.write({"state": "closed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_draft(self):
        self.write({
            "state": "draft",
            "actual_start": False,
            "actual_end": False,
        })
