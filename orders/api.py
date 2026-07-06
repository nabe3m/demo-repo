"""注文 API — 注文の受付と確定。"""

import time

from .inventory_client import InventoryClient
from .payment_client import PaymentClient, RateLimitedError


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


def capture_payment(order: dict, payments: PaymentClient) -> dict:
    """注文金額を決済する。"""
    # payment API は現行プランのレート制限 (60 req/min) があり、ピーク時に
    # 429 を返す (#9)。プロバイダは増枠予定なしのため、指数バックオフで凌ぐ。
    for attempt in range(3):
        try:
            return payments.capture(order["id"], order["amount"])
        except RateLimitedError:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)
    raise RuntimeError("unreachable")
