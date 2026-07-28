from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class BinaryGuardCustomerPortal(CustomerPortal):

    def _customer_domain(self):
        partner = request.env.user.partner_id.commercial_partner_id
        return [
            ("customer_id", "child_of", [partner.id]),
        ]

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        domain = self._customer_domain()

        counter_models = {
            "binaryguard_asset_count": "binaryguard.asset",
            "binaryguard_contract_count": "binaryguard.service.contract",
            "binaryguard_ticket_count": "binaryguard.helpdesk.ticket",
            "binaryguard_card_count": "binaryguard.access.card",
            "binaryguard_maintenance_count": "binaryguard.maintenance.plan",
        }

        for counter, model_name in counter_models.items():
            if counter in counters:
                model = request.env[model_name]
                values[counter] = (
                    model.search_count(domain)
                    if model.has_access("read")
                    else 0
                )

        return values

    def _prepare_binaryguard_values(self, page_name):
        values = self._prepare_portal_layout_values()
        values["page_name"] = page_name
        return values

    @http.route(
        ["/my/binaryguard/assets"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_binaryguard_assets(self, **kwargs):
        values = self._prepare_binaryguard_values("binaryguard_assets")
        values["assets"] = request.env["binaryguard.asset"].search(
            self._customer_domain(),
            order="create_date desc",
        )
        return request.render(
            "binaryguard_portal.portal_binaryguard_assets",
            values,
        )

    @http.route(
        ["/my/binaryguard/contracts"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_binaryguard_contracts(self, **kwargs):
        values = self._prepare_binaryguard_values("binaryguard_contracts")
        values["contracts"] = request.env[
            "binaryguard.service.contract"
        ].search(
            self._customer_domain(),
            order="start_date desc",
        )
        return request.render(
            "binaryguard_portal.portal_binaryguard_contracts",
            values,
        )

    @http.route(
        ["/my/binaryguard/tickets"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_binaryguard_tickets(self, **kwargs):
        values = self._prepare_binaryguard_values("binaryguard_tickets")
        values["tickets"] = request.env[
            "binaryguard.helpdesk.ticket"
        ].search(
            self._customer_domain(),
            order="create_date desc",
        )
        return request.render(
            "binaryguard_portal.portal_binaryguard_tickets",
            values,
        )

    @http.route(
        ["/my/binaryguard/access-cards"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_binaryguard_access_cards(self, **kwargs):
        values = self._prepare_binaryguard_values(
            "binaryguard_access_cards"
        )
        values["access_cards"] = request.env[
            "binaryguard.access.card"
        ].search(
            self._customer_domain(),
            order="create_date desc",
        )
        return request.render(
            "binaryguard_portal.portal_binaryguard_access_cards",
            values,
        )

    @http.route(
        ["/my/binaryguard/maintenance"],
        type="http",
        auth="user",
        website=True,
    )
    def portal_binaryguard_maintenance(self, **kwargs):
        values = self._prepare_binaryguard_values(
            "binaryguard_maintenance"
        )
        values["maintenance_plans"] = request.env[
            "binaryguard.maintenance.plan"
        ].search(
            self._customer_domain(),
            order="next_service_date asc",
        )
        return request.render(
            "binaryguard_portal.portal_binaryguard_maintenance",
            values,
        )
