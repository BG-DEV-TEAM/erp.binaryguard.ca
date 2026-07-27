from odoo import fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    binaryguard_client_type = fields.Selection(
        selection=[
            ("government", "Government Sector"),
            ("commercial", "Commercial"),
            ("residential", "Residential"),
            ("non_profit", "Non-Profit"),
            ("internal", "Internal"),
            ("other", "Other"),
        ],
        string="Client Type",
        tracking=True,
    )

    binaryguard_service_category = fields.Selection(
        selection=[
            ("access_control", "Access Control"),
            ("video_surveillance", "Video Surveillance"),
            ("intrusion_detection", "Intrusion Detection"),
            ("intercom", "Intercom"),
            ("networking", "Networking"),
            ("servers", "Servers and Virtualization"),
            ("cloud", "Cloud Services"),
            ("managed_it", "Managed IT Services"),
            ("cybersecurity", "Cybersecurity"),
            ("technical_support", "Technical Support"),
            ("other", "Other"),
        ],
        string="Service Category",
        tracking=True,
    )

    binaryguard_site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    binaryguard_contract_reference = fields.Char(
        string="Contract / Reference Number",
        copy=False,
        tracking=True,
    )

    binaryguard_system_type = fields.Char(
        string="Existing System / Platform",
        help="Example: Genetec, Avigilon, Axis, Microsoft 365, Proxmox or Nutanix.",
        tracking=True,
    )

    binaryguard_technician_id = fields.Many2one(
        comodel_name="res.users",
        string="Assigned Technician",
        domain=[("share", "=", False)],
        tracking=True,
    )

    binaryguard_follow_up_date = fields.Date(
        string="Next Follow-Up Date",
        tracking=True,
    )

    binaryguard_estimated_hours = fields.Float(
        string="Estimated Technical Hours",
    )

    binaryguard_remote_support = fields.Boolean(
        string="Remote Support Required",
    )

    binaryguard_site_visit = fields.Boolean(
        string="Site Visit Required",
    )

    binaryguard_technical_notes = fields.Text(
        string="Technical Assessment",
    )
