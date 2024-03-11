"""在庫サービス (inventory API) クライアント。"""

import httpx

BASE_URL = "https://inventory.internal.example.com/api/v1"


class InventoryClient:
    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(base_url=BASE_URL, timeout=10)

    def reserve(self, sku: str, quantity: int) -> dict:
        response = self._client.post("/reservations", json={"sku": sku, "quantity": quantity})
        response.raise_for_status()
        return response.json()

    def get_reservation(self, reservation_id: str) -> dict:
        response = self._client.get(f"/reservations/{reservation_id}")
        response.raise_for_status()
        return response.json()
