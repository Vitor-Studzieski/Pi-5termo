# Inventário de dados - Grupo 2

**Fazenda:** Fazenda Boa Vista, Garça/SP. **Coleta:** 07/10/2026, entre 22:23 e 22:27 em `America/Sao_Paulo`. Consultas Q01-Q07 executadas em modo somente leitura nos serviços do Grupo 2. Timestamps históricos do MongoDB foram registrados em UTC; MQTT e Redis usam horário de São Paulo neste registro.

| Serviço e escopo | Conteúdo | Quantidade e período medidos | Pergunta de negócio | Consulta |
|---|---|---|---|---|
| MariaDB `grupo2` | Fazenda, talhões, culturas, safras, sensores, máquinas, funcionários, insumos, operações, estoque, clientes e vendas | 506 linhas em 12 tabelas. Operações: 07/12/2022-26/09/2026; vendas: 07/07/2023-23/09/2026. | Qual o custo por operação/talhão/safra e qual produtividade foi registrada? | Q01 e Q02 |
| MongoDB `grupo2.leituras` | Leituras históricas de sensores, valores variáveis, bateria, firmware e timestamp UTC | 81.155 documentos, 01/06/2026 00:00-29/09/2026 23:45 UTC. | Como umidade e clima variaram por talhão e dia? | Q03 |
| MongoDB `telemetria_maquinas` | Posições/estados de máquinas ligados a `operacao_id` | 9.200 documentos, 08/06/2026 10:00-26/09/2026 13:18 UTC; 10 IDs de operação distintos, todos encontrados no MariaDB. | Onde ocorreu uma operação e há vínculo com o cadastro? | Q03 e conferência somente leitura |
| MongoDB `alertas` | Alertas históricos | 175 documentos, 27/06/2026 01:00-17/09/2026 15:15 UTC. | Quais eventos requerem atenção? | Q03 |
| MongoDB `imagens` | Catálogo NDVI com talhão, data, NDVI médio, nuvem e chave do objeto | 48 documentos, 05/06/2026 13:30-25/09/2026 13:30 UTC. O campo temporal é `data`. | Qual mapa corresponde ao talhão e à data escolhidos? | Q03 |
| Redis `grupo2:*` | Estado recente por sensor/talhão, stream, alertas, ranking e contadores | 19 chaves. Stream com 5.005 itens, 07/10 10:33:20-22:27:38 BRT; 17 alertas na lista; ranking com 6 talhões. | O que está acontecendo agora e quais alertas estão recentes? | Q04 |
| MQTT `fazenda/grupo2/#` | Publicações ao vivo de sensores e status | Captura limitada a 30 s; 9 mensagens entre 07/10 22:24:16-22:24:38 BRT: 7 tópicos de sensores e 2 de status. Nenhum payload foi armazenado. | O que está sendo publicado neste momento? | Q05 |
| MinIO bucket `grupo2` | Imagens NDVI e laudo CSV de solo | 49 objetos, 3.281.590 bytes: 48 imagens PNG e um CSV. Modificação concentrada em 30/09/2026, por volta de 05:34:51 BRT. | Qual imagem ou laudo deve ser exibido para cada talhão? | Q06 |

## Resultados relacionais

Q01 contou as linhas diretamente em cada tabela do MariaDB:

| Tabela | Linhas |
|---|---:|
| `fazenda` | 1 |
| `talhao` | 6 |
| `cultura` | 5 |
| `safra` | 30 |
| `sensor` | 7 |
| `maquina` | 5 |
| `funcionario` | 10 |
| `insumo` | 13 |
| `operacao` | 121 |
| `estoque_movimento` | 258 |
| `cliente` | 6 |
| `venda` | 44 |
| **Total** | **506** |

Q02 encontrou 121 operações, com datas entre 07/12/2022 e 26/09/2026. Os custos usam o valor da coluna `custo_total`; não foi aplicada conversão de moeda:

| Tipo | Operações | Custo acumulado | Média por operação |
|---|---:|---:|---:|
| Adubação | 24 | 1.320.963,23 | 55.040,13 |
| Pulverização | 73 | 360.862,96 | 4.943,33 |
| Colheita | 24 | 167.489,59 | 6.978,73 |
| **Total** | **121** | **1.849.315,78** | - |

Na safra colhida 2025/26, a produtividade registrada foi:

| Talhão | Produtividade (kg/ha) |
|---|---:|
| T02 | 1.976,0 |
| T01 | 1.774,9 |
| T04 | 1.774,0 |
| T06 | 1.586,6 |
| T05 | 1.482,1 |
| T03 | 1.476,5 |

## MongoDB: leituras por sensor e firmware

| Sensor | Firmware | Leituras |
|---|---|---:|
| EST-01 | 3.2.1 | 10.994 |
| EST-01 | 3.3.0-beta | 673 |
| SS-01 | 2.4.0 | 11.659 |
| SS-02 | 2.4.0 | 11.653 |
| SS-03 | 2.4.0 | 11.662 |
| SS-04 | 5.1.3 | 11.197 |
| SS-05 | 2.4.0 | 11.654 |
| SS-06 | 5.1.3 | 11.663 |
| **Total** |  | **81.155** |

## Redis e objetos

No Redis foram observadas 14 hashes, uma lista, um stream, duas strings e um sorted set. O stream retém 5.005 eventos; os contadores retornaram 81.155 leituras históricas e 77.623 leituras ao vivo. O ranking tem seis membros. É uma fotografia transitória, não a série histórica.

O bucket MinIO contém oito imagens NDVI para cada um dos seis talhões, além de `laudos/analise_solo_2026.csv`. A soma de tamanhos retornada pelo inventário é 3.281.590 bytes.

## Registro das execuções

| ID | Data/hora (America/Sao_Paulo) | Serviço/escopo | Código | Resultado e interpretação |
|---|---|---|---|---|
| Q01 | 07/10/2026, 22:23-22:27 | MariaDB `grupo2` | `consultas/mariadb-q01-inventario.sql` | 506 linhas em 12 tabelas; `estoque_movimento` é a maior tabela, com 258 linhas. |
| Q02 | 07/10/2026, 22:23-22:27 | MariaDB `grupo2` | `consultas/mariadb-q02-operacoes.sql` | 121 operações; maior custo acumulado em adubação. T02 teve a maior produtividade observada e T03 a menor na safra 2025/26. |
| Q03 | 07/10/2026, 22:23-22:27 | MongoDB `grupo2` | `consultas/mongodb-q03-inventario.js` | Contagens e coberturas listadas acima. Datas em UTC; `imagens` usa `data` em vez de `ts`. |
| Q04 | 07/10/2026, 22:23-22:27 | Redis `grupo2:*` | `consultas/redis-q04-estado.py` | 19 chaves e 5.005 itens no stream; estado e alertas recentes variam com o tempo. |
| Q05 | 07/10/2026, captura de até 30 s | MQTT `fazenda/grupo2/#` | `consultas/mqtt-q05-amostra.py` | 9 mensagens, ocorridas entre 22:24:16 e 22:24:38; a captura é pontual e não descreve o histórico. Payloads não foram copiados. |
| Q06 | 07/10/2026, 22:23-22:27 | MinIO bucket `grupo2` | `consultas/minio-q06-inventario.py` | 49 objetos e 3.281.590 bytes; a consulta percorre todas as páginas do bucket. |
| Q07 | 07/10/2026, 22:23-22:27 | MongoDB `grupo2.leituras` | `consultas/mongodb-q07-qualidade.js` | 323 chaves duplicadas, 11 leituras fora da faixa, 480 slots faltantes estimados em SS-04 e sequências longas em SS-03. Regras e limitações estão em `qualidade-dados.md`. |
