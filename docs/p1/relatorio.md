# P1 IAL214 - Estudo dos dados, arquitetura e escopo web

**Grupo 2 · Cooperativa Alta Paulista · Fazenda Boa Vista · Garça/SP**
**Projeto Integrador de Arquiteturas Cloud para Big Data · Semestre 2026.2**
**Relatório de entrega · resultados observados em 07/10/2026**

**Integrantes**

- Vitor Studzieski · RA 2591262422005
- Maria Fernanda Passos Françoso · RA 2591262422006
- Lauan Alves · RA 2591262422018
- Luan Martinhão · RA 2591262422017
- Simplicio José · RA 2591262422020

**Repositório:** [Pi-5termo](https://github.com/Vitor-Studzieski/Pi-5termo)

> As consultas Q01-Q07 foram executadas em modo somente leitura nos serviços do Grupo 2, entre 22:23 e 22:27 de 07/10/2026 (America/Sao_Paulo). As mensagens observadas por MQTT ocorreram entre 22:24:16 e 22:24:38, dentro do limite de captura de 30 segundos. O estado Redis e as mensagens MQTT são transitórios; os resultados representam o instante da coleta.

## 1. Grupo e fazenda

| Campo | Identificação | Perfil |
|---|---|---|
| Grupo | Grupo 2 | - |
| Fazenda | Fazenda Boa Vista, Garça/SP | - |
| Atividade agrícola | Café arábica | - |
| Área divulgada | 255 ha, em seis talhões | - |
| Integrante 1 | Vitor Studzieski · RA 2591262422005 | [Vitor-Studzieski](https://github.com/Vitor-Studzieski) |
| Integrante 2 | Maria Fernanda Passos Françoso · RA 2591262422006 | [MaferPassos](https://github.com/MaferPassos) |
| Integrante 3 | Lauan Alves · RA 2591262422018 | [lauan2004](https://github.com/lauan2004) |
| Integrante 4 | Luan Martinhão · RA 2591262422017 | [luanm4rtinhao](https://github.com/luanm4rtinhao) |
| Integrante 5 | Simplicio José · RA 2591262422020 | [S1mplicio-Jose](https://github.com/S1mplicio-Jose) |
| Repositório do projeto | [Pi-5termo](https://github.com/Vitor-Studzieski/Pi-5termo) | GitHub |

O projeto propõe um painel web para apoiar o gerente da Fazenda Boa Vista no acompanhamento de sensores, alertas, operações, custos e imagens NDVI. A P1 documenta os dados disponíveis e delimita a solução a ser implementada até a P2 de 17/11/2026. O conjunto didático é sintético e cobre o período histórico de 01/06/2026 a 29/09/2026; o broker MQTT continua publicando dados ao vivo.

## 2. Estudo dos dados

O sistema distribui os dados por finalidade: MariaDB mantém cadastros e transações; MongoDB, leituras históricas e documentos de telemetria; Redis, o estado recente; MQTT, mensagens ao vivo; MinIO, arquivos. A coleta do Grupo 2 confirmou 81.155 leituras de sensores, 9.200 pontos de GPS e 506 linhas SQL. O histórico de sensores termina em 29/09/2026; eventos posteriores recebidos por MQTT não são automaticamente incorporados ao MongoDB.

| Serviço e escopo | O que guarda | Quantidade/período observado | Perguntas de negócio |
|---|---|---|---|
| MariaDB `grupo2` | Fazenda, talhões, culturas, safras, sensores, máquinas, funcionários, insumos, operações, estoque, clientes e vendas | 506 linhas em 12 tabelas (Q01). As 121 operações cobrem 07/12/2022 a 26/09/2026; vendas, 07/07/2023 a 23/09/2026. | Qual talhão/safra concentra custo? Qual foi a produtividade registrada? Como estoque e venda se relacionam às operações e safras? |
| MongoDB `grupo2.leituras` | Leituras por sensor, timestamp UTC, campos variáveis em `valores`, bateria e firmware | 81.155 documentos, de 01/06/2026 00:00 a 29/09/2026 23:45 UTC (Q03). | Como umidade e condições meteorológicas variam por talhão e dia? Há lacunas ou anomalias? |
| MongoDB `telemetria_maquinas` | Pontos de GPS e estado de máquina ligados a `operacao_id` | 9.200 documentos, de 08/06/2026 10:00 a 26/09/2026 13:18 UTC. Os 10 IDs de operação distintos existem no MariaDB. | Onde a máquina operou e a telemetria pode ser associada a uma operação? |
| MongoDB `alertas` e `imagens` | Eventos de alerta e catálogo NDVI com talhão, data, média NDVI, nuvem e chave do objeto | 175 alertas (27/06 a 17/09 UTC) e 48 imagens (05/06 a 25/09 UTC). | Quais eventos requerem atenção? Qual mapa corresponde ao talhão e data escolhidos? |
| Redis `grupo2:*` | Último valor por sensor, stream curto de leituras, alertas recentes, ranking de produtividade e resumos | 19 chaves: stream com 5.005 entradas (07/10, 10:33-22:27 BRT), lista com 17 alertas e ranking com 6 talhões (Q04). | Qual é a leitura mais recente? Quais alertas e talhões aparecem no estado atual? |
| MQTT `fazenda/grupo2/#` | Publicações ao vivo de sensores, máquinas, alertas e status | 9 mensagens na captura de até 30 s; mensagens entre 22:24:16 e 22:24:38 BRT: uma de cada um dos 7 sensores e 2 de status. | O que está sendo publicado agora? Algum sensor ou máquina está online? |
| MinIO bucket `grupo2` | Imagens NDVI por talhão/data e laudo CSV de solo | 49 objetos (48 PNG e 1 CSV), 3.281.590 bytes no total (Q06). | Qual imagem ou resultado de solo pode ser consultado para um talhão? |

### Consultas e resultados

As fontes de consulta estão versionadas em `docs/p1/consultas/`. Os resultados abaixo foram coletados nos serviços do Grupo 2; valores monetários seguem a unidade da coluna `custo_total` no banco. Datas MongoDB foram registradas em UTC e as amostras ao vivo em `America/Sao_Paulo`.

**Q01 - MariaDB, linhas por tabela** (`mariadb-q01-inventario.sql`):

```sql
SELECT 'fazenda' AS tabela, COUNT(*) AS linhas FROM fazenda
UNION ALL SELECT 'talhao', COUNT(*) FROM talhao
UNION ALL SELECT 'cultura', COUNT(*) FROM cultura
UNION ALL SELECT 'safra', COUNT(*) FROM safra
UNION ALL SELECT 'sensor', COUNT(*) FROM sensor
UNION ALL SELECT 'maquina', COUNT(*) FROM maquina
UNION ALL SELECT 'funcionario', COUNT(*) FROM funcionario
UNION ALL SELECT 'insumo', COUNT(*) FROM insumo
UNION ALL SELECT 'operacao', COUNT(*) FROM operacao
UNION ALL SELECT 'estoque_movimento', COUNT(*) FROM estoque_movimento
UNION ALL SELECT 'cliente', COUNT(*) FROM cliente
UNION ALL SELECT 'venda', COUNT(*) FROM venda;
```

**Resultado Q01 (07/10/2026):** `fazenda` 1; `talhao` 6; `cultura` 5; `safra` 30; `sensor` 7; `maquina` 5; `funcionario` 10; `insumo` 13; `operacao` 121; `estoque_movimento` 258; `cliente` 6; `venda` 44. **Total: 506 linhas.**

**Q02 - MariaDB, custo e produtividade** (`mariadb-q02-operacoes.sql`):

```sql
SELECT tipo, COUNT(*) AS quantidade,
       ROUND(SUM(custo_total), 2) AS custo_total
FROM operacao GROUP BY tipo ORDER BY custo_total DESC;
```

Para cruzar o resultado agrícola na safra colhida 2025/26, Q02b consulta a produtividade registrada por talhão:

```sql
SELECT t.codigo AS talhao, c.nome AS cultura, s.produtividade_kg_ha
FROM safra s
JOIN talhao t ON t.id = s.talhao_id
JOIN cultura c ON c.id = s.cultura_id
WHERE s.ano_safra = '2025/26' AND s.status = 'colhida'
ORDER BY s.produtividade_kg_ha DESC;
```

**Resultado Q02 (07/10/2026):** adubação, 24 operações e 1.320.963,23; pulverização, 73 e 360.862,96; colheita, 24 e 167.489,59. Produtividade 2025/26 em kg/ha: T02 1.976,0; T01 1.774,9; T04 1.774,0; T06 1.586,6; T05 1.482,1; T03 1.476,5.

**Q03 - MongoDB, contagem e cobertura histórica** (`mongodb-q03-inventario.js`):

```javascript
for (const nome of ["leituras", "telemetria_maquinas", "alertas", "imagens"]) {
  const c = db.getCollection(nome);
  const campoData = nome === "imagens" ? "data" : "ts";
  printjson({colecao: nome, documentos: c.countDocuments({}),
    campo_data: campoData,
    cobertura_utc: c.aggregate([{$group: {_id: null,
      primeiro: {$min: `$${campoData}`}, ultimo: {$max: `$${campoData}`}}}]).toArray()});
}
```

**Q04 - Redis, chaves e janela recente** (`redis-q04-estado.py`):

```sh
python3 docs/p1/consultas/redis-q04-estado.py
```

**Q05 - MQTT, amostra ao vivo** (`mqtt-q05-amostra.py`):

```sh
python3 docs/p1/consultas/mqtt-q05-amostra.py
```

**Q06 - MinIO, objetos do bucket** (`minio-q06-inventario.py`):

```sh
python3 docs/p1/consultas/minio-q06-inventario.py
```

**Q07 - MongoDB, triagem de qualidade** (`mongodb-q07-qualidade.js`): a consulta completa mede duplicatas, lacunas, percentuais fora da faixa, sequências repetidas, distribuição por firmware e documentos fora da ordem natural. Exemplo da regra de duplicidade:

```javascript
db.leituras.aggregate([
  { $group: { _id: { sensor: "$sensor", ts: "$ts" }, n: { $sum: 1 } } },
  { $match: { n: { $gt: 1 } } },
  { $group: { _id: null, chaves_duplicadas: { $sum: 1 },
    linhas_excedentes: { $sum: { $subtract: ["$n", 1] } } } }
])
```

| Consulta | Execução (horário de São Paulo) | Resultado observado | Interpretação |
|---|---|---|---|
| Q01 | 07/10/2026, 22:23-22:27 | 506 linhas em 12 tabelas; `estoque_movimento` tem 258 e `operacao`, 121. | O inventário relacional observado coincide com as 506 linhas totais publicadas para o grupo; a distribuição por tabela foi medida diretamente. |
| Q02 | 07/10/2026, 22:23-22:27 | 121 operações, custo acumulado 1.849.315,78; adubação 1.320.963,23, pulverização 360.862,96 e colheita 167.489,59. Produtividade 2025/26: 1.476,5-1.976,0 kg/ha. | Adubação responde pela maior parcela do custo registrado. T02 teve maior produtividade e T03 a menor; o resultado é histórico e não mede a safra em curso. |
| Q03 | 07/10/2026, 22:23-22:27 | 81.155 leituras, 9.200 pontos de telemetria, 175 alertas e 48 imagens. Leituras: 01/06-29/09 UTC. | O histórico de sensores termina em 29/09/2026; a coleção `imagens` usa o campo `data`, não `ts`. |
| Q04 | 07/10/2026, 22:23-22:27 | 19 chaves; 14 hashes, 1 lista, 1 stream, 2 strings e 1 conjunto ordenado. Stream: 5.005 entradas; contador histórico 81.155 e ao vivo 77.623. | Redis serve a janela recente: o stream cobre 10:33:20-22:27:38 BRT e mantém cerca de 5 mil entradas, enquanto os contadores são acumulados. |
| Q05 | 07/10/2026, captura de até 30 s; mensagens entre 22:24:16-22:24:38 | 9 mensagens recebidas; 7 tópicos de sensores e 2 de status. Payloads não foram gravados. | Confirma atividade ao vivo durante a amostra; não representa taxa ou cobertura do histórico completo. |
| Q06 | 07/10/2026, 22:23-22:27 | 49 objetos e 3.281.590 bytes: 48 imagens NDVI e um laudo CSV. Objetos modificados em 30/09/2026, por volta de 05:34:51 BRT. | Há oito imagens por talhão em seis talhões e um arquivo de laudo; o catálogo MongoDB referencia as chaves NDVI. |
| Q07 | 07/10/2026, 22:23-22:27 | 323 chaves duplicadas (323 linhas excedentes), 11 leituras inválidas, 480 slots estimados sem leitura em SS-04 e 89 posições repetidas em sequências longas de SS-03. | Defeitos foram medidos sem alterar os dados. Os limiares de 15 min e 8 repetições são triagem; a ordem natural do Mongo é apenas um indicador físico. |

## 3. Qualidade dos dados

A documentação do conjunto informa que foram incluídos exemplos de duplicatas, intervalos sem leitura, valores impossíveis, sensores repetindo valores, alterações de unidade após mudança de firmware e documentos fora da ordem temporal. A consulta Q07 foi executada em 07/10/2026, entre 22:23 e 22:27 BRT, e as quantidades abaixo são do Grupo 2. Os limiares são critérios de triagem, não prova isolada de defeito físico.

| Problema e detecção | Quantidade afetada | Tratamento planejado |
|---|---|---|
| Duplicata: mesma chave lógica `(sensor, ts)` no MongoDB. Q07 agrupa a chave e conta linhas excedentes. | 323 chaves duplicadas, 323 linhas excedentes. | Deduplicar idempotentemente pela chave lógica ao ingerir; não contar duplicatas em médias. Manter trilha de auditoria. |
| Lacuna: intervalo entre duas leituras do mesmo sensor acima da cadência nominal histórica de 15 min. Q07 ordena por `ts` UTC e estima slots ausentes. | 480 slots ausentes estimados em SS-04. | Mostrar lacuna e intervalo sem dado; não interpolar silenciosamente. |
| Percentual impossível: umidade percentual ou bateria menor que 0 ou maior que 100. Q07 filtra os campos. | 11 leituras fora de `[0,100]` (0,0135% de 81.155), todas em SS-06; umidade a 10 cm varia de -1 a 999 nesses registros. | Excluir da agregação e dos alertas numéricos; preservar o valor bruto com indicador de qualidade. |
| Sensor possivelmente travado: oito ou mais valores consecutivos iguais no mesmo sensor. Q07 faz triagem com base na cadência de 15 min. | 89 posições após o 7º valor de uma sequência longa, em SS-03. | Sinalizar para análise; confirmar com status e firmware antes de excluir. O limiar é triagem, não prova de defeito. |
| Unidade/firmware: distribuição de versão e escala dos valores por sensor/período. Q03/Q07 comparam firmware e campos numéricos. | Foram observadas versões `3.2.1` e `3.3.0-beta` no EST-01; `2.4.0` em SS-01/02/03/05; `5.1.3` em SS-04/06. Não foi possível confirmar mudança de unidade apenas com a escala; SS-06 concentra os 11 extremos. | Converter para unidade canônica somente após confirmar a mudança; guardar unidade original e regra de conversão. |
| Ordem de chegada distinta da hora do evento: comparar sequência natural e `ts`. | 40.592 recuos de timestamp ao percorrer a ordem natural do Mongo, somados nos sensores; a consulta detalha a contagem por sensor. | Ordenar gráficos por hora do evento (`ts`), aceitar atrasos e tornar a gravação idempotente. A ordem natural é volátil e não prova sozinha atraso na rede. |
| Telemetria sem operação associada: comparar `operacao_id` MongoDB com `operacao.id` MariaDB. | 9.200 pontos, 10 IDs distintos; todos os 10 existem entre as 121 operações e nenhum ponto está sem `operacao_id`. | Exibir vínculo pela operação; sinalizar referências não encontradas caso apareçam em novas ingestões. |

Os limiares de triagem serão revistos com o cadastro e o firmware do sensor. O sistema manterá visível a diferença entre “sem leitura” e “leitura válida sem alteração”. Nenhuma limpeza será aplicada diretamente ao conjunto compartilhado da disciplina.

## 4. Arquitetura atual

O conjunto histórico é carregado nos serviços gerenciados da disciplina. No fluxo contínuo, o simulador publica mensagens no broker MQTT e atualiza o Redis. O broker também entrega as mensagens aos assinantes; a mensagem MQTT não se torna automaticamente um documento histórico do MongoDB. A consulta da página da disciplina indica que o stream Redis guarda aproximadamente as últimas 5.000 leituras e que as estruturas recentes são uma visão de curta duração.

![Arquitetura atual do conjunto do Grupo 2](arquitetura/atual.svg)

O MariaDB guarda cadastros e relações que exigem integridade; MongoDB suporta documentos de sensores e telemetria com campos variáveis e consultas por tempo; Redis atende leitura rápida do estado recente; MQTT desacopla publicação e assinatura do fluxo; MinIO guarda arquivos binários sem inflar os bancos transacionais. O catálogo de imagens fica no MongoDB e referencia a chave de objeto no MinIO. O diagrama editável Mermaid está em `arquitetura/atual.mmd`.

## 5. Escopo do sistema web

### Problema e persona

**Persona principal - gerente da Fazenda Boa Vista:** precisa verificar a condição dos seis talhões, reconhecer rapidamente quando a leitura está desatualizada ou suspeita, investigar alertas e relacionar a operação de campo a custos, telemetria, análise de solo e imagens NDVI. O painel reduz a troca entre ferramentas e deixa explícita a origem e a atualidade de cada informação.

### Requisitos funcionais

- RF01. Exibir resumo da fazenda, talhões, última leitura disponível, chuva/umidade disponível e data/hora da atualização.
- RF02. Permitir selecionar talhão e período para consultar leituras históricas por sensor.
- RF03. Exibir alertas recentes e indicar severidade, sensor/talhão e horário do evento.
- RF04. Consultar operações e custos agregados por tipo, talhão e safra.
- RF05. Abrir mapas NDVI e laudo de solo pelo catálogo e pela chave de objeto correspondente.
- RF06. Distinguir dado histórico, estado Redis e evento MQTT ao vivo; exibir atraso, ausência e qualidade da leitura.
- RF07. Disponibilizar indicação de saúde das conexões e horário da última atualização por serviço.

### Requisitos não funcionais

- RNF01. Credenciais permanecem no servidor/coletor; navegador recebe somente dados necessários à tela.
- RNF02. Usuário do banco tem privilégio mínimo; conexões externas usam TLS quando o serviço disponibilizar.
- RNF03. Tela principal responde em até 3 s para consultas típicas sob carga de laboratório (meta a validar; filtros e limites de período obrigatórios).
- RNF04. O painel degrada com mensagem clara se MQTT, Redis ou um banco estiver indisponível; falha de um serviço não bloqueia telas independentes.
- RNF05. Dados históricos são consultados em leitura; gravações ficam limitadas à persistência idempotente de novas mensagens pelo coletor, se aprovada na P2.
- RNF06. Layout responsivo e contraste legível em desktop/notebook; datas exibidas em `America/Sao_Paulo`, armazenadas/intercambiadas em UTC.

### Wireframes

Os traçados e valores de exemplo nos wireframes são ilustrativos e não representam medições nem alertas observados na Fazenda Boa Vista.

![Wireframe 1 - Visão geral](wireframes/01-visao-geral.svg)

![Wireframe 2 - Talhão e sensores](wireframes/02-talhao-sensores.svg)

![Wireframe 3 - Operações e custos](wireframes/03-operacoes-custos.svg)

![Wireframe 4 - NDVI e solo](wireframes/04-ndvi-solo.svg)

| Tela | Informação exibida | Origem |
|---|---|---|
| Visão geral | Nome, área, talhões, cultura e safra | MariaDB `fazenda`, `talhao`, `cultura`, `safra`; Redis `grupo2:fazenda`, `grupo2:talhao:*` para resumo recente |
| Visão geral | Última leitura e estado atual | Redis `grupo2:sensor:<codigo>`; se assinada, tópico MQTT `fazenda/grupo2/sensores/<SENSOR>`; status `fazenda/grupo2/status` |
| Visão geral | Alertas recentes | Redis `grupo2:alertas:recentes`; confirmação/histórico em MongoDB `alertas` |
| Talhão e sensores | Série histórica, umidade, temperatura, bateria, firmware | MongoDB `leituras`, filtrado por `sensor`, `talhao` e `ts`; cadastros MariaDB `sensor`, `talhao` |
| Operações e custos | Tipo, data, custo, funcionário, máquina, insumo e safra | MariaDB `operacao`, `funcionario`, `maquina`, `insumo`, `safra`, `talhao` |
| Operações e custos | Percurso/telemetria ligada à operação | MongoDB `telemetria_maquinas` por `operacao_id`; cadastro MariaDB `maquina` |
| NDVI e solo | Datas, NDVI médio, nuvem, caminho do objeto | MongoDB `imagens`; imagens em MinIO `grupo2/ndvi/<talhao>/<data>.png` |
| NDVI e solo | pH, matéria orgânica, nutrientes e profundidade | MinIO `grupo2/laudos/analise_solo_2026.csv`; metadados de talhão em MariaDB |

## 6. Arquitetura proposta e plano

### Decisão de arquitetura

Propomos um **monólito web modular**, acompanhado por um **container coletor MQTT** pequeno e independente. Com cinco integrantes e seis semanas até a P2, o monólito reduz o custo de deploy e de integração das telas; módulos internos isolam domínio, consultas e adaptadores. O coletor fica separado porque tem ciclo contínuo de consumo, reconexão e gravação, diferente do ciclo de requisição da interface. Essa divisão evita decompor cada função de tela em um serviço próprio.

O coletor assina `fazenda/grupo2/#`, valida esquema, sensor e timestamp, registra eventos tardios com a hora do evento e usa `(tópico, sensor, timestamp)` como chave idempotente. A proposta é gravar novas leituras aceitas em MongoDB e atualizar o estado recente em Redis. QoS 1, reconexão com backoff e confirmação somente após persistência reduzem perda; deduplicação cobre reentrega. A política de retenção, armazenamento de payload inválido e autorização de persistência devem ser confirmadas antes da implementação.

![Arquitetura proposta](arquitetura/proposta.svg)

### Containers, portas e credenciais

| Container | Função | Rede/porta planejada |
|---|---|---|
| `web` | Interface e API do monólito modular; conecta aos bancos no servidor | Porta interna 8000; porta externa planejada 8081, dentro da faixa reservada ao grupo. Não expõe credenciais ao navegador. |
| `mqtt-coletor` | Assina tópicos do Grupo 2, valida mensagens e persiste as novas leituras | Sem porta pública; conexões de saída ao MQTT, MongoDB e Redis. |
| Serviços gerenciados da disciplina | MariaDB, MongoDB, Redis, MQTT e MinIO | Não recriar nem publicar containers locais desses serviços para a aplicação do grupo. |

Credenciais entram como variáveis de ambiente no deploy pelo painel de containers. `.env.example` contém somente nomes e valores demonstrativos; `.env` permanece local/ignorado. O servidor recebe `MARIADB_*`, `MONGODB_URI`, `REDIS_URL`, `MINIO_*`; o coletor recebe `MQTT_*`, `MONGODB_URI` e `REDIS_URL`. Nenhum segredo vai para imagem, Git, log, HTML ou JavaScript do navegador. Os usuários dos serviços devem ter acesso restrito ao `grupo2`.

### Cronograma até a P2

| Período | Entrega intermediária |
|---|---|
| 08-11/10 | Medir consultas, fechar inventário, confirmar qualidade e registrar decisões. |
| 12-18/10 | Esqueleto do monólito, adaptadores read-only, navegação e credenciais de ambiente. |
| 19-25/10 | Implementar visão geral e tela de talhão; validar consultas históricas e datas/fuso. |
| 26/10-01/11 | Operações/custos, NDVI/laudo e rastreabilidade da tela às fontes. |
| 02-08/11 | Coletor MQTT, idempotência, estado Redis e tratamento de indisponibilidade/atraso. |
| 09-15/11 | Integração, revisão de qualidade, deploy de containers e roteiro/evidências de demonstração. |
| 16-17/11 | Correções finais, congelamento da versão, PDF/relatório final e entrega da P2. |

### Divisão de tarefas

| Integrante | Responsabilidade planejada |
|---|---|
| Vitor Studzieski · RA 2591262422005 | Coordenação, consultas MariaDB, custos/produtividade e integração das telas. |
| Maria Fernanda Passos Françoso · RA 2591262422006 | Consultas MongoDB, análise de qualidade e adaptador histórico. |
| Lauan Alves · RA 2591262422018 | Interface e wireframes, consultas Redis/MQTT e apresentação do estado recente. |
| Luan Martinhão · RA 2591262422017 | Containers, MinIO, deploy e documentação de operação/evidências. |
| Simplicio José · RA 2591262422020 | Validação integrada das consultas, indicadores de qualidade e evidências de validação/demonstração para a P2. |

Essa distribuição é o plano de trabalho sugerido para a equipe e deve ser validada pelo grupo antes da implementação. A arquitetura editável está em `arquitetura/proposta.mmd`; a decisão e suas consequências estão em `../decisoes/ADR-001-arquitetura.md`.

### Referências

- Atividade P1 IAL214: https://lapps.studio/disciplinas/projeto-integrador-arquiteturas-cloud/atividades/p1-estudo-dados-escopo/
- Conjunto de dados IAL214: https://lapps.studio/disciplinas/projeto-integrador-arquiteturas-cloud/dados/
- Guia de organização deste repositório: `../../instrucoes.md`.
