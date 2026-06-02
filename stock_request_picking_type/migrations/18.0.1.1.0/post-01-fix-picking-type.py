from odoo import SUPERUSER_ID, api
from odoo.addons.stock_request_picking_type.hooks import _ensure_stock_request_picking_type


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _ensure_stock_request_picking_type(env)
