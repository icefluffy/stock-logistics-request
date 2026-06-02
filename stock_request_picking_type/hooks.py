from odoo import api


def _ensure_stock_request_picking_types(env):
    sequence = env.ref("stock_request.seq_stock_request_order", raise_if_not_found=False)
    if not sequence:
        return

    warehouses = env["stock.warehouse"].search([])

    for warehouse in warehouses:
        company = warehouse.company_id
        PickingType = env["stock.picking.type"].with_company(company)

        picking_type = PickingType.search(
            [
                ("code", "=", "stock_request_order"),
                ("warehouse_id", "=", warehouse.id),
                ("company_id", "=", company.id),
            ],
            limit=1,
        )

        vals = {
            "name": f"{warehouse.name}: Stock Requests",
            "sequence_id": sequence.id,
            "code": "stock_request_order",
            "sequence_code": "SRO",
            "warehouse_id": warehouse.id,
            "company_id": company.id,
        }

        if picking_type:
            picking_type.write(vals)
        else:
            picking_type = PickingType.create(vals)

        xmlid_name = f"stock_request_order_wh_{warehouse.id}"
        imd = env["ir.model.data"].search(
            [
                ("module", "=", "stock_request_picking_type"),
                ("name", "=", xmlid_name),
                ("model", "=", "stock.picking.type"),
            ],
            limit=1,
        )

        imd_vals = {
            "module": "stock_request_picking_type",
            "name": xmlid_name,
            "model": "stock.picking.type",
            "res_id": picking_type.id,
            "noupdate": True,
        }

        if imd:
            imd.write(imd_vals)
        else:
            env["ir.model.data"].create(imd_vals)


def post_init_hook(env):
    _ensure_stock_request_picking_types(env)
