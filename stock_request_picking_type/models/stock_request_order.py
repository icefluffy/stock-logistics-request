# Copyright 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class StockRequestOrder(models.Model):
    _inherit = "stock.request.order"

    picking_type_id = fields.Many2one(
        comodel_name="stock.picking.type",
        string="Operation Type",
        compute="_compute_picking_type_id",
        required=True,
        store=True,
        readonly=False,
        precompute=True,
        check_company=True,
        domain="[('code', '=', 'stock_request_order'), ('company_id', '=', company_id), ('warehouse_id', '=', warehouse_id)]",
    )

    @api.depends("warehouse_id", "company_id")
    def _compute_picking_type_id(self):
        picking_type_obj = self.env["stock.picking.type"]
        for order in self:
            picking_type = False
            if order.warehouse_id and order.company_id:
                picking_type = picking_type_obj.search(
                    [
                        ("code", "=", "stock_request_order"),
                        ("warehouse_id", "=", order.warehouse_id.id),
                        ("company_id", "=", order.company_id.id),
                    ],
                    limit=1,
                )
            order.picking_type_id = picking_type
