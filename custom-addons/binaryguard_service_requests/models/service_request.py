from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardServiceRequest(models.Model):
    _name = "binaryguard.service.request"
    _description = "BinaryGuard Service Request"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, create_date desc"

    name = fields.Char(
        string="Request Number",
        required=True,
        readonly=True,
        copy=False,
        default="New",
        index=True,
    )

    subject = fields.Char(
        string="Request Subject",
        required=True,
        tracking=True,
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        index=True,
        tracking=True,
    )

    contact_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer Contact",
        tracking=True,
    )

    request_type = fields.Selection(
        selection=[
            ("technical_support", "Technical Support"),
            ("remote_support", "Remote Support"),
            ("site_visit", "Site Visit"),
            ("installation", "New Installation"),
            ("maintenance", "Maintenance Request"),
            ("quotation", "Quotation Request"),
            ("inspection", "Inspection Request"),
            ("emergency", "Emergency Service"),
            ("other", "Other"),
        ],
        string="Request Type",
        required=True,
        default="technical_support",
        tracking=True,
    )

    system_category = fields.Selection(
        selection=[
            ("cctv", "CCTV / Video Surveillance"),
            ("access_control", "Access Control"),
            ("intercom", "Intercom"),
            ("intrusion", "Intrusion Detection"),
            ("network", "Network Infrastructure"),
            ("server", "Server / Virtualization"),
            ("cybersecurity", "Cybersecurity"),
            ("software", "Software / Application"),
            ("power", "UPS / Power"),
            ("general", "General IT"),
            ("other", "Other"),
        ],
        string="System Category",
        required=True,
        default="general",
        tracking=True,
    )

    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Urgent"),
            ("4", "Critical"),
        ],
        string="Priority",
        required=True,
        default="1",
        index=True,
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("submitted", "Submitted"),
            ("triage", "Technical Triage"),
            ("assigned", "Assigned"),
            ("in_progress", "In Progress"),
            ("waiting_customer", "Waiting for Customer"),
            ("resolved", "Resolved"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        required=True,
        default="draft",
        index=True,
        tracking=True,
    )

    description = fields.Html(
        string="Request Description",
        required=True,
    )

    site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    building = fields.Char(
        string="Building",
        tracking=True,
    )

    room_or_area = fields.Char(
        string="Room / Area",
        tracking=True,
    )

    contract_id = fields.Many2one(
        comodel_name="binaryguard.service.contract",
        string="Service Contract",
        tracking=True,
    )

    asset_id = fields.Many2one(
        comodel_name="binaryguard.asset",
        string="Affected Asset",
        tracking=True,
    )

    helpdesk_ticket_id = fields.Many2one(
        comodel_name="binaryguard.helpdesk.ticket",
        string="Helpdesk Ticket",
        tracking=True,
    )

    project_id = fields.Many2one(
        comodel_name="project.project",
        string="Related Project",
        tracking=True,
    )

    field_service_task_id = fields.Many2one(
        comodel_name="project.task",
        string="Field Service Task",
        tracking=True,
    )

    assigned_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
        domain=[("share", "=", False)],
        tracking=True,
    )

    requested_date = fields.Datetime(
        string="Requested Date",
        required=True,
        default=fields.Datetime.now,
        tracking=True,
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Service Date",
        tracking=True,
    )

    response_date = fields.Datetime(
        string="First Response Date",
        readonly=True,
        tracking=True,
    )

    completed_date = fields.Datetime(
        string="Completed Date",
        readonly=True,
        tracking=True,
    )

    estimated_hours = fields.Float(
        string="Estimated Hours",
        default=1.0,
        tracking=True,
    )

    remote_support_possible = fields.Boolean(
        string="Remote Support Possible",
        default=True,
        tracking=True,
    )

    site_visit_required = fields.Boolean(
        string="Site Visit Required",
        tracking=True,
    )

    contract_covered = fields.Boolean(
        string="Covered by Contract",
        tracking=True,
    )

    customer_reference = fields.Char(
        string="Customer Reference",
        tracking=True,
    )

    resolution_summary = fields.Html(
        string="Resolution Summary",
    )

    internal_notes = fields.Text(
        string="Internal Notes",
    )

    portal_visible = fields.Boolean(
        string="Visible in Customer Portal",
        default=True,
    )

    active = fields.Boolean(
        default=True,
    )

    _request_number_unique = models.Constraint(
        "UNIQUE(name)",
        "The service request number must be unique.",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.service.request"
                    )
                    or "New"
                )
        return super().create(vals_list)

    @api.constrains(
        "requested_date",
        "scheduled_date",
        "completed_date",
    )
    def _check_service_dates(self):
        for request_record in self:
            if (
                request_record.requested_date
                and request_record.scheduled_date
                and request_record.scheduled_date
                < request_record.requested_date
            ):
                raise ValidationError(
                    "The scheduled service date cannot be earlier "
                    "than the requested date."
                )

            if (
                request_record.requested_date
                and request_record.completed_date
                and request_record.completed_date
                < request_record.requested_date
            ):
                raise ValidationError(
                    "The completed date cannot be earlier "
                    "than the requested date."
                )

    @api.constrains("estimated_hours")
    def _check_estimated_hours(self):
        for request_record in self:
            if request_record.estimated_hours < 0:
                raise ValidationError(
                    "Estimated hours cannot be negative."
                )

    def action_submit(self):
        self.write({"state": "submitted"})

    def action_triage(self):
        self.write({
            "state": "triage",
            "response_date": fields.Datetime.now(),
        })

    def action_assign(self):
        for request_record in self:
            if not request_record.assigned_user_id:
                raise ValidationError(
                    "Select an assigned technician before assigning "
                    "the service request."
                )
        self.write({"state": "assigned"})

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_waiting_customer(self):
        self.write({"state": "waiting_customer"})

    def action_resolve(self):
        for request_record in self:
            if not request_record.resolution_summary:
                raise ValidationError(
                    "Enter a resolution summary before resolving "
                    "the service request."
                )

        self.write({
            "state": "resolved",
            "completed_date": fields.Datetime.now(),
        })

    def action_close(self):
        self.write({"state": "closed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_draft(self):
        self.write({
            "state": "draft",
            "completed_date": False,
        })
