import os
from dataclasses import dataclass, field


PLANS = {
    "1m":  {"months": 1,  "price": 99,  "label": "1 месяц",    "description": "Wado VPN — подписка на 1 месяц"},
    "3m":  {"months": 3,  "price": 249, "label": "3 месяца",   "description": "Wado VPN — подписка на 3 месяца"},
    "6m":  {"months": 6,  "price": 499, "label": "6 месяцев",  "description": "Wado VPN — подписка на 6 месяцев"},
    "12m": {"months": 12, "price": 899, "label": "12 месяцев", "description": "Wado VPN — подписка на 12 месяцев"},
}


@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]
    marzban_url: str
    marzban_user: str
    marzban_pass: str
    yookassa_shop_id: str
    yookassa_secret_key: str
    yookassa_return_url: str
    webhook_host: str
    webhook_port: int
    trial_days: int = 3
    default_data_limit_gb: int = 50
    inbounds: dict = None

    def __post_init__(self):
        if self.inbounds is None:
            self.inbounds = {
                "vless": ["VLESS_REALITY"],
                "shadowsocks": ["SHADOWSOCKS_TCP"],
            }


def load_config() -> Config:
    admin_ids_raw = os.environ.get("ADMIN_IDS", "")
    admin_ids = [int(x.strip()) for x in admin_ids_raw.split(",") if x.strip()]
    return Config(
        bot_token=os.environ["BOT_TOKEN"],
        admin_ids=admin_ids,
        marzban_url=os.environ.get("MARZBAN_URL", "https://127.0.0.1:8000"),
        marzban_user=os.environ.get("MARZBAN_USER", "admin"),
        marzban_pass=os.environ.get("MARZBAN_PASS", ""),
        yookassa_shop_id=os.environ.get("YOOKASSA_SHOP_ID", ""),
        yookassa_secret_key=os.environ.get("YOOKASSA_SECRET_KEY", ""),
        yookassa_return_url=os.environ.get("YOOKASSA_RETURN_URL", "https://t.me/wadovpn_bot"),
        webhook_host=os.environ.get("WEBHOOK_HOST", "127.0.0.1"),
        webhook_port=int(os.environ.get("WEBHOOK_PORT", "8081")),
        trial_days=int(os.environ.get("TRIAL_DAYS", "3")),
        default_data_limit_gb=int(os.environ.get("DATA_LIMIT_GB", "50")),
    )
