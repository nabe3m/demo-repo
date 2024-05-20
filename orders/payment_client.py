"""決済サービス (payment API) クライアント。"""

import httpx

BASE_URL = "https://payments.internal.example.com/api/v1"


class RateLimitedError(Exception):
    """レート制限 (HTTP 429) を受けた。"""


class PaymentClient:
    def __init__(self, client: httpx.Client | None = None) -> None:
        self._client = client or httpx.Client(base_url=BASE_URL, timeout=10)

    def capture(self, order_id: str, amount: int) -> dict:
        response = self._client.post(
            "/captures", json={"order_id": order_id, "amount": amount}
        )
        if response.status_code == 429:
            raise RateLimitedError(response.headers.get("Retry-After", ""))
        response.raise_for_status()
        return response.json()
