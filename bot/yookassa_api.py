import uuid
import logging
import httpx

from config import Config, PLANS

log = logging.getLogger(__name__)

YOOKASSA_API = "https://api.yookassa.ru/v3"


class YooKassaAPI:
    def __init__(self, cfg: Config):
        self.shop_id = cfg.yookassa_shop_id
        self.secret = cfg.yookassa_secret_key
        self.return_url = cfg.yookassa_return_url
        self._client = httpx.AsyncClient(
            base_url=YOOKASSA_API,
            auth=(self.shop_id, self.secret),
            timeout=20,
        )

    async def create_payment(self, tg_id: int, plan_key: str, email: str | None = None) -> dict:
        plan = PLANS[plan_key]
        amount = f"{plan['price']:.2f}"
        body = {
            "amount": {"value": amount, "currency": "RUB"},
            "capture": True,
            "confirmation": {
                "type": "redirect",
                "return_url": self.return_url,
            },
            "description": plan["description"],
            "metadata": {
                "tg_id": str(tg_id),
                "plan": plan_key,
            },
        }
        # Автоотправка чеков через ЮKassa пока не подключена → чеки бьются
        # вручную в «Мой налог». Когда подключишь в ЛК — раскомментируй блок.
        # if email:
        #     body["receipt"] = {
        #         "customer": {"email": email},
        #         "items": [{
        #             "description": plan["description"],
        #             "quantity": "1.00",
        #             "amount": {"value": amount, "currency": "RUB"},
        #             "vat_code": 1,
        #             "payment_mode": "full_payment",
        #             "payment_subject": "service",
        #         }],
        #     }
        headers = {"Idempotence-Key": str(uuid.uuid4())}
        resp = await self._client.post("/payments", json=body, headers=headers)
        if resp.status_code >= 400:
            log.error("YooKassa create_payment failed: %s %s", resp.status_code, resp.text)
        resp.raise_for_status()
        return resp.json()

    async def get_payment(self, payment_id: str) -> dict:
        resp = await self._client.get(f"/payments/{payment_id}")
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self._client.aclose()
