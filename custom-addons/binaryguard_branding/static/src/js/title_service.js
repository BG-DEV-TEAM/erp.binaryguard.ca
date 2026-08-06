/** @odoo-module **/

import { registry } from "@web/core/registry";

const binaryGuardTitleService = {
    dependencies: ["title"],

    start(env, { title }) {
        title.setParts({
            zopenerp: "BinaryGuard ERP",
        });
    },
};

registry.category("services").add(
    "binaryguard_title",
    binaryGuardTitleService
);
