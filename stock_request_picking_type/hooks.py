from odoo import SUPERUSER_ID, api


def _ensure_stock_request_picking_type(env):
    warehouse = env.ref("stock.warehouse0", raise_if_not_found=False)
    sequence = env.ref("stock_request.seq_stock_request_order", raise_if_not_found=False)

    if not warehouse or not sequence:
        return

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

    imd = env["ir.model.data"].search(
        [
            ("module", "=", "stock_request_picking_type"),
            ("name", "=", "stock_request_order"),
            ("model", "=", "stock.picking.type"),
        ],
        limit=1,
    )

    imd_vals = {
        "module": "stock_request_picking_type",
        "name": "stock_request_order",
        "model": "stock.picking.type",
        "res_id": picking_type.id,
        "noupdate": True,
    }

    if imd:
        imd.write(imd_vals)
    else:
        env["ir.model.data"].create(imd_vals)


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _ensure_stock_request_picking_type(env)
