import httpx
import time
from config import Config

# GB to bytes
GB = 1024 ** 3


class MarzbanAPI:
    def __init__(self, cfg: Config):
        self.base = cfg.marzban_url
        self.user = cfg.marzban_user
        self.password = cfg.marzban_pass
        self.inbounds = cfg.inbounds
        self.data_limit = cfg.default_data_limit_gb * GB
        self._token: str | None = None
        self._token_exp: float = 0
        self._client = httpx.AsyncClient(base_url=self.base, verify=False, timeout=15)

    async def _ensure_token(self):
        if self._token and time.time() < self._token_exp:
            return
        resp = await self._client.post("/api/admin/token", data={
            "username": self.user,
            "password": self.password,
        })
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._token_exp = time.time() + 3600 * 23  # refresh daily

    @property
    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self._token}"}

    async def create_user(self, username: str, expire_ts: int) -> dict:
        await self._ensure_token()
        resp = await self._client.post("/api/user", headers=self._headers, json={
            "username": username,
            "inbounds": self.inbounds,
            "expire": expire_ts,
            "data_limit": self.data_limit,
            "data_limit_reset_strategy": "no_reset",
            "status": "active",
            "proxies": {
                "vless": {"flow": ""},
                "shadowsocks": {},
            },
        })
        resp.raise_for_status()
        return resp.json()

    async def get_user(self, username: str) -> dict | None:
        await self._ensure_token()
        resp = await self._client.get(f"/api/user/{username}", headers=self._headers)
        if resp.status_code == 404:
            return None
        resp.raise_for_status()
        return resp.json()

    async def update_user(self, username: str, **kwargs) -> dict:
        await self._ensure_token()
        resp = await self._client.put(
            f"/api/user/{username}", headers=self._headers, json=kwargs
        )
        resp.raise_for_status()
        return resp.json()

    async def delete_user(self, username: str) -> bool:
        await self._ensure_token()
        resp = await self._client.delete(
            f"/api/user/{username}", headers=self._headers
        )
        return resp.status_code == 200

    async def get_system_stats(self) -> dict:
        await self._ensure_token()
        resp = await self._client.get("/api/system", headers=self._headers)
        resp.raise_for_status()
        return resp.json()

    async def get_users(self, offset: int = 0, limit: int = 100) -> list[dict]:
        await self._ensure_token()
        resp = await self._client.get(
            "/api/users", headers=self._headers,
            params={"offset": offset, "limit": limit},
        )
        resp.raise_for_status()
        return resp.json().get("users", [])

    async def close(self):
        await self._client.aclose()
