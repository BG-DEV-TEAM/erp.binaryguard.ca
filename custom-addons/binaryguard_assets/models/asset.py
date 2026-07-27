from odoo import api, fields, models


class BinaryGuardAsset(models.Model):
    _name = "binaryguard.asset"
    _description = "BinaryGuard Asset"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "name"

    name = fields.Char(
        string="Asset Number",
        required=True,
        copy=False,
        readonly=True,
        default="New",
        index=True,
    )

    asset_name = fields.Char(
        string="Asset Name",
        required=True,
        tracking=True,
    )

    ownership = fields.Selection(
        selection=[
            ("company", "BinaryGuard Owned"),
            ("customer", "Customer Owned"),
            ("rental", "Rental"),
            ("demo", "Demo Equipment"),
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

    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        tracking=True,
    )

    asset_type = fields.Selection(
        selection=[
            ("camera", "Camera"),
            ("nvr", "NVR / Recorder"),
            ("reader", "Card Reader"),
            ("controller", "Access Controller"),
            ("access_card", "Access Card"),
            ("intercom", "Intercom"),
            ("intrusion", "Intrusion Device"),
            ("server", "Server"),
            ("workstation", "Workstation"),
            ("laptop", "Laptop"),
            ("switch", "Network Switch"),
            ("firewall", "Firewall"),
            ("ups", "UPS"),
            ("license", "Software License"),
            ("tool", "Tool"),
            ("other", "Other"),
        ],
        string="Asset Type",
        required=True,
        default="other",
        tracking=True,
    )

    manufacturer = fields.Char(
        string="Manufacturer",
        tracking=True,
    )

    model_number = fields.Char(
        string="Model Number",
        tracking=True,
    )

    serial_number = fields.Char(
        string="Serial Number",
        index=True,
        tracking=True,
    )

    asset_tag = fields.Char(
        string="Asset Tag",
        index=True,
        tracking=True,
    )

    site_location = fields.Char(
        string="Site Location",
        tracking=True,
    )

    installation_date = fields.Date(
        string="Installation Date",
        tracking=True,
    )

    warranty_start = fields.Date(
        string="Warranty Start",
        tracking=True,
    )

    warranty_end = fields.Date(
        string="Warranty End",
        tracking=True,
    )

    assigned_employee_id = fields.Many2one(
        comodel_name="hr.employee",
        string="Assigned Employee",
        tracking=True,
    )

    assigned_technician_id = fields.Many2one(
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

    helpdesk_ticket_id = fields.Many2one(
        comodel_name="binaryguard.helpdesk.ticket",
        string="Related Helpdesk Ticket",
        tracking=True,
    )

    ip_address = fields.Char(
        string="IP Address",
        tracking=True,
    )

    mac_address = fields.Char(
        string="MAC Address",
        tracking=True,
    )

    firmware_version = fields.Char(
        string="Firmware Version",
        tracking=True,
    )

    status = fields.Selection(
        selection=[
            ("draft", "Draft"),
            ("in_stock", "In Stock"),
            ("assigned", "Assigned"),
            ("installed", "Installed"),
            ("maintenance", "Under Maintenance"),
            ("repair", "Under Repair"),
            ("retired", "Retired"),
            ("lost", "Lost"),
            ("disposed", "Disposed"),
        ],
        string="Status",
        required=True,
        default="draft",
        tracking=True,
    )

    active = fields.Boolean(
        default=True,
    )

    notes = fields.Html(
        string="Technical Notes",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for values in vals_list:
            if values.get("name", "New") == "New":
                values["name"] = (
                    self.env["ir.sequence"].next_by_code(
                        "binaryguard.asset"
                    )
                    or "New"
                )
        return super().create(vals_list)
