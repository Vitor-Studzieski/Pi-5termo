"""Captura no maximo 20 publicacoes/30 s e registra apenas metadados."""
import json
import os
import time
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import paho.mqtt.client as mqtt


ROOT = Path(__file__).resolve().parents[3]
env_file = ROOT / ".env"
if env_file.exists():
    for line in env_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("\"'"))

host = os.environ["MQTT_HOST"]
port = int(os.environ.get("MQTT_PORT", "1884"))
username = os.environ["MQTT_USERNAME"]
password = os.environ["MQTT_PASSWORD"]
counts = Counter()
payload_bytes = Counter()
connected = False
connection_error = None


def on_connect(client, userdata, flags, reason_code, properties):
    global connected, connection_error
    if reason_code == 0:
        connected = True
        client.subscribe("fazenda/grupo2/#", qos=0)
    else:
        connection_error = "broker recusou a conexão"


def on_message(client, userdata, message):
    counts[message.topic] += 1
    payload_bytes[message.topic] += len(message.payload)
    if sum(counts.values()) >= 20:
        client.disconnect()


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="p1-readonly-" + uuid.uuid4().hex[:8],
    protocol=mqtt.MQTTv311,
)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message
started = datetime.now(ZoneInfo("America/Sao_Paulo"))
monotonic_start = time.monotonic()
client.connect(host, port, keepalive=20)
client.loop_start()
while time.monotonic() - monotonic_start < 30 and sum(counts.values()) < 20 and connection_error is None:
    time.sleep(0.1)
ended = datetime.now(ZoneInfo("America/Sao_Paulo"))
client.disconnect()
client.loop_stop()
if connection_error:
    raise RuntimeError(connection_error)

print(json.dumps({
    "escopo": "fazenda/grupo2/#",
    "limite_segundos": 30,
    "limite_mensagens": 20,
    "inicio_brt": started.isoformat(timespec="seconds"),
    "fim_brt": ended.isoformat(timespec="seconds"),
    "total_mensagens": sum(counts.values()),
    "mensagens_por_topico": dict(sorted(counts.items())),
    "bytes_por_topico": dict(sorted(payload_bytes.items())),
    "payloads": "omitidos",
}, ensure_ascii=False, sort_keys=True))
