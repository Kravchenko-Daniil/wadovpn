import os
from dataclasses import dataclass, field


PLANS = {
    "1m":  {"months": 1,  "label": "1 месяц"},
    "3m":  {"months": 3,  "label": "3 месяца"},
    "6m":  {"months": 6,  "label": "6 месяцев"},
    "12m": {"months": 12, "label": "12 месяцев"},
}


@dataclass
class Config:
    bot_token: str
    admin_ids: list[int]
    marzban_url: str
    marzban_user: str
    marzban_pass: str
    redirect_host: str
    redirect_port: int
    redirect_base_url: str
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
        redirect_host=os.environ.get("REDIRECT_HOST", "127.0.0.1"),
        redirect_port=int(os.environ.get("REDIRECT_PORT", "8081")),
        redirect_base_url=os.environ.get("REDIRECT_BASE_URL", "https://pay.wadovpn.online"),
        trial_days=int(os.environ.get("TRIAL_DAYS", "3")),
        default_data_limit_gb=int(os.environ.get("DATA_LIMIT_GB", "50")),
    )
