# Qualidade dos dados - Grupo 2

A pagina da disciplina informa que o conjunto sintetico inclui exemplos de duplicatas, lacunas, valores fisicamente impossiveis, leituras repetidas, mudanca de unidade/firmware e documentos fora de ordem temporal. Ela nao identifica os registros do Grupo 2. As consultas abaixo medem os defeitos no ambiente real; ate sua execucao, as quantidades permanecem pendentes.

| Defeito | Regra de deteccao | Quantidade medida | Tratamento planejado |
|---|---|---|---|
| Leituras duplicadas | Mongo Q07: mesma chave logica `(sensor, ts)`; contar linhas excedentes | PENDENTE | Deduplicar por chave logica no consumidor; nao somar duas vezes em agregacoes. Preservar o documento original para auditoria ate decidir a retencao. |
| Intervalos sem leitura | Mongo Q07: diferenca entre timestamps consecutivos do mesmo sensor; cadencia historica esperada de 15 min | PENDENTE | Mostrar lacuna no grafico e sinalizar periodo sem dado; nao interpolar silenciosamente. |
| Percentual fora da faixa | Mongo Q07: umidade percentual ou bateria fora de `[0,100]` | PENDENTE | Marcar leitura como invalida para medias/alertas; manter valor bruto e expor indicador de qualidade. |
| Valor repetido por longo periodo | Mongo Q07: sequencia de pelo menos 8 leituras identicas do mesmo sensor (triagem de 2 h na cadencia historica) | PENDENTE | Sinalizar possivel sensor travado; confirmar contra firmware e status antes de excluir. |
| Mudanca de unidade/firmware | Mongo Q03/Q07: comparar firmware e distribuicao/escala dos campos por sensor e periodo | PENDENTE | Normalizar para unidade canonica apenas depois de identificar a escala; manter unidade original/metadado da conversao. |
| Ordem de chegada diferente da hora do evento | Mongo Q07: comparar ordem natural de insercao com `ts` nos documentos | PENDENTE | Ordenar graficos por `ts`; tratar atraso/idempotencia pelo timestamp do evento, sem descartar mensagens tardias automaticamente. |
| Consistencia entre telemetria e operacao | Conferir `operacao_id` em Mongo contra MariaDB | PENDENTE | Exibir telemetria sem vinculacao com aviso e excluir de metricas por operacao ate corrigir a referencia. |

**Regra de interpretacao:** limiares de unidade, cadencia e repeticao sao criterios de triagem; devem ser confirmados com o tipo do sensor e firmware. As queries somente leem dados. A aplicacao nao altera o conjunto compartilhado da disciplina.
