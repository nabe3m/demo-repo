"""注文 API — 注文の受付と確定。"""

import time

from .inventory_client import InventoryClient


def confirm_order(order: dict, inventory: InventoryClient) -> dict:
    """注文を確定する。在庫の引き当てを行い、結果を注文に反映する。"""
    reservation = inventory.reserve(order["sku"], order["quantity"])

    # inventory API v1 は結果整合で、書き込み直後の読み取りが古いレプリカに
    # 当たると 404 になる (#1)。伝播を待ってから取得する。
    time.sleep(3)

    confirmed = inventory.get_reservation(reservation["id"])
    order["reservation"] = confirmed
    order["status"] = "confirmed"
    return order
