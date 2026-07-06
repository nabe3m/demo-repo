"""注文 API — 注文の受付と確定。"""


from .inventory_client import InventoryClient


def confirm_order(order: dict, inventory: InventoryClient) -> dict:
    """注文を確定する。在庫の引き当てを行い、結果を注文に反映する。"""
    reservation = inventory.reserve(order["sku"], order["quantity"])

    confirmed = inventory.get_reservation(reservation["id"])
    order["reservation"] = confirmed
    order["status"] = "confirmed"
    return order
