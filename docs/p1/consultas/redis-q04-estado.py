"""Inventario somente de leitura das chaves Redis do Grupo 2."""
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import redis


ROOT = Path(__file__).resolve().parents[3]
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

r = redis.Redis.from_url(os.environ["REDIS_URL"], decode_responses=True,
                         socket_connect_timeout=8, socket_timeout=8)
r.ping()
keys = sorted(r.scan_iter(match="grupo2:*", count=250))
counts = {}
details = {}
for key in keys:
    kind = r.type(key)
    counts[kind] = counts.get(kind, 0) + 1
    if kind == "hash": length = r.hlen(key)
    elif kind == "list": length = r.llen(key)
    elif kind == "stream": length = r.xlen(key)
    elif kind == "zset": length = r.zcard(key)
    elif kind == "set": length = r.scard(key)
    elif kind == "string": length = len(r.get(key) or "")
    else: length = None
    details[key] = {"tipo": kind, "campos_itens_ou_caracteres": length}

first = r.xrange("grupo2:stream:leituras", "-", "+", count=1)
last = r.xrevrange("grupo2:stream:leituras", "+", "-", count=1)


def stream_time(entries):
    if not entries:
        return None
    milliseconds = int(entries[0][0].split("-", 1)[0])
    return datetime.fromtimestamp(milliseconds / 1000, timezone.utc).astimezone(
        ZoneInfo("America/Sao_Paulo")).isoformat(timespec="seconds")


print(json.dumps({
    "escopo": "grupo2:*",
    "total_chaves": len(keys),
    "por_tipo": counts,
    "estruturas": details,
    "stream_leituras": {
        "itens": r.xlen("grupo2:stream:leituras"),
        "primeiro_brt": stream_time(first),
        "ultimo_brt": stream_time(last),
    },
    "alertas_recentes": r.llen("grupo2:alertas:recentes"),
    "membros_ranking": r.zcard("grupo2:ranking:produtividade:2025-26"),
    "contador_historicas": r.get("grupo2:contador:leituras_historicas"),
    "contador_ao_vivo": r.get("grupo2:contador:leituras_ao_vivo"),
}, ensure_ascii=False, sort_keys=True))
