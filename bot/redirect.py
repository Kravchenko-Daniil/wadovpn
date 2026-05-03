"""HTTP-редиректор custom-scheme deep-link'ов для импорта подписки в VPN-клиенты.

Зачем: Telegram пропускает в HTML-ссылках только http/https/tg, а нам нужно
тыкать пользователя в `happ://add/...`, `karing://install-config?...` и т.п.
Бот кладёт в сообщение HTTPS-ссылку https://<host>/open?app=happ&sub=<urlenc>,
браузер юзера открывает её, и эта страница делает window.location.replace
в нужную custom scheme — OS перехватывает и открывает приложение.
"""

import logging
from urllib.parse import quote

from aiohttp import web

log = logging.getLogger(__name__)


def _build_target(app_name: str, sub: str) -> str | None:
    sub_enc = quote(sub, safe="")
    schemes = {
        "happ":         f"happ://add/{sub_enc}",
        "karing":       f"karing://install-config?url={sub_enc}&name=Wado",
        "shadowrocket": f"sub://{sub}",
        "v2rayng":      f"v2rayng://install-sub/?url={sub_enc}%23Wado",
        "hiddify":      f"hiddify://import/{sub}#Wado",
    }
    return schemes.get(app_name)


async def _on_open(request: web.Request) -> web.Response:
    app_name = request.query.get("app", "")
    sub = request.query.get("sub", "")
    target = _build_target(app_name, sub) if sub else None
    if not target:
        return web.Response(status=400, text="Bad request")

    target_html = target.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")
    target_js = target.replace("\\", "\\\\").replace('"', '\\"')

    html = f"""<!DOCTYPE html>
<html lang="ru"><head><meta charset="utf-8">
<title>Открываем приложение…</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta http-equiv="refresh" content="0;url={target_html}">
<style>
body{{font-family:-apple-system,BlinkMacSystemFont,system-ui,sans-serif;
     text-align:center;padding:60px 24px;color:#222;background:#f7f8fa}}
h1{{font-size:18px;font-weight:500;margin:0 0 24px}}
a.btn{{color:#fff;background:#3390ec;text-decoration:none;font-size:16px;
      display:inline-block;padding:14px 28px;border-radius:10px;font-weight:500}}
p.hint{{color:#888;font-size:14px;margin-top:32px}}
</style></head><body>
<h1>Открываем приложение…</h1>
<a class="btn" href="{target_html}">Открыть вручную</a>
<p class="hint">Если приложение не открылось — установите его и нажмите ссылку ещё раз.</p>
<script>window.location.replace("{target_js}");</script>
</body></html>"""
    return web.Response(text=html, content_type="text/html")


async def _on_health(request: web.Request) -> web.Response:
    return web.Response(text="ok")


def build_app() -> web.Application:
    app = web.Application()
    app.router.add_get("/open", _on_open)
    app.router.add_get("/health", _on_health)
    return app


async def start(host: str, port: int) -> web.AppRunner:
    app = build_app()
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    log.info("Redirect server listening on %s:%s", host, port)
    return runner
