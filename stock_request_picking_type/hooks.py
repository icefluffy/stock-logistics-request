# Copyright 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


def _get_or_create_sequence(env, warehouse):
    company = warehouse.company_id
    sequence_code = f"stock.request.order.{warehouse.id}"
    sequence_name = f"{warehouse.name}: Stock Request"
    prefix = f"SRO/{warehouse.code or warehouse.id}/"

    sequence = env["ir.sequence"].sudo().search(
        [
            ("code", "=", sequence_code),
            ("company_id", "=", company.id),
        ],
        limit=1,
    )
    if sequence:
        return sequence

    return env["ir.sequence"].sudo().create(
        {
            "name": sequence_name,
            "code": sequence_code,
            "prefix": prefix,
            "padding": 5,
            "company_id": company.id,
        }
    )


def _ensure_stock_request_picking_types(env):
    warehouses = env["stock.warehouse"].sudo().search([])

    for warehouse in warehouses:
        company = warehouse.company_id
        sequence = _get_or_create_sequence(env, warehouse)
        PickingType = env["stock.picking.type"].sudo().with_company(company)

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
            "sequence_code": sequence.code,
            "warehouse_id": warehouse.id,
            "company_id": company.id,
        }

        if picking_type:
            picking_type.write(vals)
        else:
            picking_type = PickingType.create(vals)

        xmlid_name = f"stock_request_order_wh_{warehouse.id}"
        imd = env["ir.model.data"].sudo().search(
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
            env["ir.model.data"].sudo().create(imd_vals)


def post_init_hook(env):
    _ensure_stock_request_picking_types(env)
