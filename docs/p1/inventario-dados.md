# Inventario de dados - Grupo 2

**Fazenda:** Fazenda Boa Vista, Garca/SP. **Janela historica divulgada:** 01/06/2026 a 29/09/2026. Os timestamps de MongoDB estao em UTC; agregacoes por dia devem converter para `America/Sao_Paulo`.

Os numeros abaixo sao resultados a coletar dos servicos autenticados do Grupo 2. A pagina publica da disciplina informa como referencia de consistencia 81.155 leituras de sensores, 9.200 pontos de GPS e 506 linhas SQL para o Grupo 2; esses totais publicados nao substituem as consultas executadas pelo grupo nem identificam a distribuicao por tabela/colecao.

A consulta Q07 (`consultas/mongodb-q07-qualidade.js`) mede separadamente os defeitos descritos em `qualidade-dados.md`; ela complementa o inventario e nao substitui as seis consultas por servico.

| Servico | Conteudo esperado | Quantidade e periodo medidos | Pergunta de negocio | Consulta |
|---|---|---|---|---|
| MariaDB `grupo2` | Cadastro da fazenda, seis talhoes, culturas, safras, sensores, maquinas, funcionarios, insumos, operacoes, estoque, clientes e vendas | A preencher com Q01 e Q02; janela por coluna de data observada | Qual o custo por operacao/talhao/safra e qual produtividade foi registrada? | `consultas/mariadb-q01-inventario.sql`, `mariadb-q02-operacoes.sql` |
| MongoDB `grupo2.leituras` | Leituras historicas de sensores, valores variaveis por tipo, bateria, firmware e timestamp UTC | A preencher com Q03; menor e maior `ts` observados | Como umidade e clima variaram por talhao e dia? | `consultas/mongodb-q03-inventario.js` |
| MongoDB `telemetria_maquinas`, `alertas`, `imagens` | Posicoes/estados de maquinas, alertas e catalogo das imagens NDVI | A preencher com Q03 | Onde ocorreu uma operacao, quais alertas foram emitidos e como evoluiu o vigor do talhao? | Q03 |
| Redis `grupo2:*` | Ultimo estado dos sensores, stream curto, alertas recentes, ranking de produtividade e metadados | A preencher com Q04; representa estado recente, nao o historico completo | O que esta acontecendo agora e quais alertas recentes estao ativos? | `consultas/redis-q04-estado.txt` |
| MQTT `fazenda/grupo2/#` | Publicacoes ao vivo de sensores, maquinas, alertas e status | Amostra ao vivo Q05, com instante e duracao da captura; nao e contagem historica | O que esta sendo publicado neste momento? | `consultas/mqtt-q05-amostra.sh` |
| MinIO bucket `grupo2` | Imagens NDVI por talhao/data e laudo CSV de solo | A preencher com Q06; registrar objetos, bytes e datas | Qual imagem ou laudo deve ser exibido para cada talhao? | `consultas/minio-q06-inventario.py` |

## Registro de execucao

Preencher uma linha por consulta depois de executa-la. Nao copiar valores de outro grupo, de uma execucao local simulada ou de uma pagina de referencia como se fossem resultado observado.

| ID | Data/hora (America/Sao_Paulo) | Servico e escopo | Comando/arquivo | Resultado e unidade | Interpretacao e limitacoes |
|---|---|---|---|---|---|
| Q01 | PENDENTE | MariaDB `grupo2` | `mariadb-q01-inventario.sql` | PENDENTE | PENDENTE |
| Q02 | PENDENTE | MariaDB `grupo2` | `mariadb-q02-operacoes.sql` | PENDENTE | PENDENTE |
| Q03 | PENDENTE | MongoDB `grupo2` | `mongodb-q03-inventario.js` | PENDENTE | PENDENTE |
| Q04 | PENDENTE | Redis `grupo2:*` | `redis-q04-estado.txt` | PENDENTE | PENDENTE |
| Q05 | PENDENTE | MQTT `fazenda/grupo2/#` | `mqtt-q05-amostra.sh` | PENDENTE | Amostra ao vivo e transitoria; nao descreve o historico |
| Q06 | PENDENTE | MinIO bucket `grupo2` | `minio-q06-inventario.py` | PENDENTE | PENDENTE |
