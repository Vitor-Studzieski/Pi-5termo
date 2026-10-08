#!/bin/sh
# Q05: amostra transitoria do broker, limitada a 20 mensagens ou 30 segundos.
# Configure MQTT_USERNAME e MQTT_PASSWORD no ambiente local; nao salve a saida
# bruta com credenciais nem faça publish em topicos da disciplina.
set -eu
: "${MQTT_HOST:=35.226.64.52}"
: "${MQTT_PORT:=1884}"
: "${MQTT_USERNAME:?Configure MQTT_USERNAME no ambiente local}"
: "${MQTT_PASSWORD:?Configure MQTT_PASSWORD no ambiente local}"
mosquitto_sub -h "$MQTT_HOST" -p "$MQTT_PORT" \
  -u "$MQTT_USERNAME" -P "$MQTT_PASSWORD" \
  -t 'fazenda/grupo2/#' -v -C 20 -W 30
