from odoo import api, fields, models
from odoo.exceptions import ValidationError


class BinaryGuardHelpdeskTicket(models.Model):
    _name = "binaryguard.helpdesk.ticket"
    _description = "BinaryGuard Helpdesk Ticket"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "priority desc, create_date desc"

    name = fields.Char(
        string="Ticket Number",
        required=True,
        copy=False,
        readonly=True,
        default="New",
        index=True,
    )

    subject = fields.Char(
        string="Subject",
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
        string="Contact Person",
        tracking=True,
    )

    customer_email = fields.Char(
        string="Customer Email",
        related="contact_id.email",
        readonly=True,
    )

    customer_phone = fields.Char(
        string="Customer Phone",
        related="contact_id.phone",
        readonly=True,
    )

    site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    issue_category = fields.Selection(
        selection=[
            ("incident", "Incident"),
            ("service_request", "Service Request"),
            ("configuration", "Configuration Request"),
            ("maintenance", "Maintenance"),
            ("repair", "Repair"),
            ("access_request", "Access Request"),
            ("consultation", "Consultation"),
            ("other", "Other"),
        ],
        string="Issue Category",
        required=True,
        default="incident",
        tracking=True,
    )

    system_type = fields.Selection(
        selection=[
            ("access_control", "Access Control"),
            ("video_surveillance", "Video Surveillance"),
            ("intrusion", "Intrusion Detection"),
            ("intercom", "Intercom"),
            ("networking", "Networking"),
            ("server", "Server / Virtualization"),
            ("cloud", "Cloud Services"),
            ("microsoft_365", "Microsoft 365"),
            ("cybersecurity", "Cybersecurity"),
            ("other", "Other"),
        ],
        string="System Type",
        tracking=True,
    )

    priority = fields.Selection(
        selection=[
            ("0", "Low"),
            ("1", "Normal"),
            ("2", "High"),
            ("3", "Critical"),
        ],
        string="Priority",
        default="1",
        tracking=True,
    )

    state = fields.Selection(
        selection=[
            ("new", "New"),
            ("assigned", "Assigned"),
            ("in_progress", "In Progress"),
            ("waiting_customer", "Waiting for Customer"),
            ("waiting_parts", "Waiting for Parts"),
            ("scheduled", "Site Visit Scheduled"),
            ("resolved", "Resolved"),
            ("closed", "Closed"),
            ("cancelled", "Cancelled"),
        ],
        string="Status",
        default="new",
        required=True,
        tracking=True,
    )

    assigned_user_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
        domain=[("share", "=", False)],
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

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Related Equipment",
        tracking=True,
    )

    serial_number = fields.Char(
        string="Serial Number",
        tracking=True,
    )

    remote_support_required = fields.Boolean(
        string="Remote Support Required",
        tracking=True,
    )

    site_visit_required = fields.Boolean(
        string="Site Visit Required",
        tracking=True,
    )

    scheduled_date = fields.Datetime(
        string="Scheduled Service Date",
        tracking=True,
    )

    reported_date = fields.Datetime(
        string="Reported Date",
        default=fields.Datetime.now,
        readonly=True,
    )

    resolved_date = fields.Datetime(
        string="Resolved Date",
        readonly=True,
        tracking=True,
    )

    description = fields.Html(
        string="Issue Description",
        required=True,
    )

    diagnosis = fields.Html(
        string="Technical Diagnosis",
    )

    resolution = fields.Html(
        string="Resolution",
    )

    internal_notes = fields.Text(
        string="Internal Notes",
    )

    active = fields.Boolean(
        default=True,
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.helpdesk.ticket"
                    )
                    or "New"
                )
        return super().create(vals_list)

    def write(self, values):
        if values.get("state") == "resolved":
            values.setdefault("resolved_date", fields.Datetime.now())

        if values.get("state") not in ("resolved", "closed"):
            if "state" in values:
                values["resolved_date"] = False

        return super().write(values)

    @api.constrains("scheduled_date", "reported_date")
    def _check_scheduled_date(self):
        for ticket in self:
            if (
                ticket.scheduled_date
                and ticket.reported_date
                and ticket.scheduled_date < ticket.reported_date
            ):
                raise ValidationError(
                    "The scheduled service date cannot be earlier "
                    "than the reported date."
                )
