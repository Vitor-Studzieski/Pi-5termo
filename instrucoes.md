# Guia do repositório do Projeto IAL214

**Grupo 2 · Fazenda Boa Vista · Garça/SP**

Este guia propõe uma estrutura de repositório para organizar a P1 e desenvolver o sistema web até a P2. A página da atividade é a fonte dos requisitos de entrega. O artigo anexado ajuda a justificar uma opção arquitetural, mas as decisões e os resultados do grupo devem ser documentados e verificados com consultas aos serviços do próprio grupo.

> **Escopo:** a entrega da P1 é o PDF do grupo com as seis seções indicadas abaixo. O restante deste guia recomenda como organizar o repositório e preparar a evolução até a P2; não significa que todo o sistema, código, testes ou materiais finais da P2 precisem ser entregues na P1.

## Estrutura sugerida

```text
.
├── README.md
├── .gitignore
├── .env.example
├── docs/
│   ├── p1/
│   │   ├── P1_IAL214_Grupo2.pdf
│   │   ├── inventario-dados.md
│   │   ├── qualidade-dados.md
│   │   ├── consultas/
│   │   ├── arquitetura/
│   │   └── wireframes/
│   ├── p2/
│   │   ├── roteiro-demonstracao.md
│   │   └── evidencias-validacao.md
│   ├── decisoes/
│   │   └── ADR-001-arquitetura.md
│   └── operacao.md
├── src/
│   ├── web/
│   └── coletor-mqtt/
├── infra/
│   ├── compose.yaml
│   └── README.md
├── scripts/
│   ├── consultas/
│   └── operacao/
└── tests/
    ├── unit/
    ├── integration/
    └── smoke/
```

A estrutura pode mudar conforme a implementação, desde que os materiais da atividade continuem fáceis de localizar. Evitem manter cópias divergentes do mesmo relatório ou diagrama.

## O que é obrigatório na P1

Entreguem um único PDF do grupo, nomeado `P1_IAL214_Grupo2.pdf`. Ele deve conter as seis seções descritas em `docs/p1/`. Cada aluno envia esse PDF individualmente, conforme a orientação da disciplina. O relatório também precisa incluir o link do repositório.

Na P1, o grupo **planeja** o sistema: apresenta escopo, wireframes, arquitetura proposta, containers/portas previstos, tratamento de credenciais, cronograma até 17/11/2026 e divisão de tarefas. Isso não exige que o sistema já esteja implementado ou no ar.

## O que é organização recomendada do repositório

A árvore de pastas, README de execução, `.env.example`, decisões de arquitetura e pastas para consultas são recomendações para manter o trabalho organizado e reproduzível. Não são entregas adicionais da P1 além do conteúdo exigido no PDF. Os arquivos-fonte das consultas, resultados medidos, diagramas e wireframes ajudam o grupo a sustentar e atualizar o relatório.

## O que fica para a evolução até a P2

As pastas `src/`, `infra/`, `tests/` e `docs/p2/` servem para organizar a implementação e a entrega final ao longo das semanas. Código executável, testes, implantação, vídeo e relatório final pertencem ao trabalho de desenvolvimento até a P2, conforme o cronograma combinado pelo grupo; não são exigidos prontos na entrega da P1.

## O que colocar em cada parte

### `README.md`

Deve permitir que um integrante novo entenda e execute o projeto. Incluam:

- objetivo do sistema, problema atendido e usuários previstos;
- identificação do grupo e da fazenda;
- integrantes, RAs e responsabilidades acordadas;
- funcionalidades incluídas e limites do escopo;
- arquitetura resumida e links para os diagramas em `docs/`;
- pré-requisitos, configuração local e comandos para iniciar/parar a aplicação;
- porta publicada do grupo e endereço de acesso ao sistema;
- variáveis necessárias, apontando para `.env.example` sem revelar valores secretos;
- links para a P1, decisões de arquitetura e instruções de operação.

### `docs/p1/`

A P1 deve ter as seis seções pedidas na atividade, nesta ordem:

1. Grupo, fazenda, integrantes com nome completo e RA, e link do repositório.
2. Inventário de MariaDB, MongoDB, Redis, MQTT e MinIO: o que guardam, quantidade, período, consulta usada e perguntas de negócio que respondem.
3. Qualidade: cada defeito encontrado, regra/consulta de detecção, quantidade afetada e tratamento planejado.
4. Arquitetura atual: diagrama próprio do fluxo e justificativa para a localização de cada tipo de dado.
5. Escopo web: persona, requisitos funcionais e não funcionais, de 3 a 6 wireframes e tabela tela → informação → serviço/coleção/tabela/chave/tópico.
6. Arquitetura proposta e plano: monólito ou microsserviços e justificativa, containers, portas, credenciais no ambiente, tratamento do MQTT, cronograma até 17/11/2026 e divisão de tarefas por integrante.

O PDF do grupo deve se chamar `P1_IAL214_Grupo2.pdf`. Cada integrante faz sua própria entrega conforme a instrução da disciplina.

### `docs/p1/consultas/`

Guardem o código de cada consulta em arquivo separado, numerado e identificado pelo serviço. Por exemplo:

```text
mariadb-q01-contagem-tabelas.sql
mariadb-q02-custos-por-operacao.sql
mongodb-q03-cobertura-leituras.js
redis-q04-estado-recente.txt
mqtt-q05-amostra-ao-vivo.py
minio-q06-inventario-objetos.py
```

Para cada consulta, registrem também em `inventario-dados.md` ou em um arquivo de resultados:

- pergunta de negócio;
- data/hora da execução e serviço consultado;
- comando ou consulta executada;
- resultado observado, incluindo unidade e intervalo de tempo;
- interpretação curta e limitações da amostra.

A atividade exige no mínimo cinco consultas reais, com código, resultado e interpretação. Não preencham resultados estimados a partir da página, do artigo ou de uma execução local diferente do banco do grupo. Diferenciem dados históricos de eventos MQTT ao vivo e anotem o fuso horário usado ao agrupar datas.

### `docs/p1/qualidade-dados.md`

Para cada problema, registrem a regra que o detecta e a quantidade medida. Investiguem, quando presentes, duplicatas, intervalos sem leitura, valores impossíveis, sensores repetindo o mesmo valor, mudanças de unidade/firmware e documentos fora de ordem temporal. Descrevam como a aplicação vai tratar cada caso, por exemplo: sinalizar lacunas, deduplicar pela chave lógica, excluir valores inválidos de agregações ou preservar e ordenar eventos pela hora do evento.

Não basta listar problemas possíveis: a tabela deve incluir consulta, quantidade afetada e comportamento previsto.

### `docs/p1/arquitetura/` e `docs/p1/wireframes/`

Guardem tanto os arquivos editáveis quanto as exportações usadas no PDF:

- diagrama próprio da arquitetura atual e justificativa dos cinco serviços;
- diagrama da arquitetura proposta e fluxo de dados;
- 3 a 6 wireframes legíveis, um por tela;
- tabela de rastreabilidade que liga cada informação da tela ao serviço e à coleção, tabela, chave ou tópico de origem.

Se usarem Mermaid, Draw.io, Figma ou Excalidraw, mantenham o arquivo-fonte junto da imagem exportada.

### `docs/decisoes/`

Registrem decisões importantes em notas curtas: contexto, opções consideradas, decisão, motivos e consequências. A escolha entre monólito, monólito modular e microsserviços deve refletir o tamanho da equipe, o prazo e as necessidades observadas. O artigo anexado pode ser citado como referência de discussão; não substitui a decisão do grupo.

### `src/`, `infra/`, `scripts/` e `tests/`

- `src/web/`: interface, rotas, módulos de domínio e adaptadores que consultam os serviços de dados no servidor.
- `src/coletor-mqtt/`: assinatura dos tópicos necessários, validação, retentativas e persistência do fluxo novo, se o sistema precisar manter histórico.
- `infra/`: Dockerfiles, `compose.yaml`, configuração de implantação e mapeamento de portas. Documentem quais containers expõem portas e quais ficam internos.
- `scripts/`: consultas e tarefas reproduzíveis; scripts de análise devem ser somente de leitura, salvo quando a operação estiver explicitamente documentada e autorizada.
- `tests/`: testes unitários, integração com dependências e verificações de disponibilidade/rotas. Não incluam credenciais reais nem dependam de alterar os dados compartilhados da disciplina.

A atividade informa que o fluxo MQTT ao vivo não é gravado automaticamente no histórico do MongoDB. Se o grupo decidir persistir novas mensagens, documentem o consumidor responsável, a política de duplicatas/atrasos e como o Redis representa o estado recente.

## Segredos, dados e Git

O acesso aos serviços da disciplina é sensível: usem somente os recursos do Grupo 2 e nunca coloquem a folha de acessos, senhas, tokens ou URLs com credenciais no repositório.

- Versionem `.env.example` apenas com nomes de variáveis e valores demonstrativos vazios.
- Mantenham `.env`, arquivos de segredo, dumps, logs com credenciais e saídas temporárias no `.gitignore`.
- Injete as credenciais nos containers em tempo de execução pelo ambiente de implantação; não as gravem no código, Dockerfile, imagem ou frontend.
- Não exponham credenciais ao navegador. As conexões aos bancos devem ser feitas no servidor/coletor.
- Não façam commit de cópias completas dos bancos ou arquivos baixados do MinIO. Versionem consultas e resultados agregados necessários para reproduzir a análise.
- Antes de publicar o PDF no GitHub, confirmem a visibilidade do repositório e que a divulgação de nomes e RAs está de acordo com a equipe e a disciplina.

Exemplo de variáveis para documentar em `.env.example` (sem valores reais):

```dotenv
APP_PORT=
MARIADB_HOST=
MARIADB_PORT=3307
MARIADB_DATABASE=grupo2
MARIADB_USER=
MARIADB_PASSWORD=
MONGODB_URI=
REDIS_URL=
MQTT_HOST=
MQTT_PORT=1884
MQTT_USERNAME=
MQTT_PASSWORD=
MINIO_ENDPOINT=
MINIO_BUCKET=grupo2
MINIO_ACCESS_KEY=
MINIO_SECRET_KEY=
```

Um ponto de partida para o `.gitignore`:

```gitignore
.env
.env.*
!.env.example
*.log
*.sql.gz
*.dump
__pycache__/
.DS_Store
node_modules/
dist/
build/
```

## Entrega até a P2

A P2 está prevista para **17/11/2026**. Até lá, mantenham no repositório o sistema executável, configuração de implantação sem segredos, instruções de operação, evidências das validações, roteiro do vídeo e relatório final solicitado na disciplina. Atualizem o README quando comandos, portas ou requisitos mudarem.

## Checklist antes de cada entrega

- [ ] O README explica como executar o projeto do zero.
- [ ] As consultas e os resultados correspondem ao banco do Grupo 2 e têm data/hora.
- [ ] Os defeitos de qualidade têm regra de detecção e quantidade medida.
- [ ] Diagramas e wireframes têm fonte editável e exportação legível.
- [ ] Cada tela aponta para dados existentes e para seu serviço de origem.
- [ ] Containers, portas e variáveis de ambiente estão documentados.
- [ ] Nenhum segredo, dump ou arquivo de acesso foi versionado.
- [ ] A P1 está em PDF com os integrantes e os RAs conferidos.
- [ ] A divisão de tarefas identifica responsabilidades de cada integrante.

## Referências da disciplina

- Atividade P1: <https://lapps.studio/disciplinas/projeto-integrador-arquiteturas-cloud/atividades/p1-estudo-dados-escopo/>
- Conjunto de dados IAL214: <https://lapps.studio/disciplinas/projeto-integrador-arquiteturas-cloud/dados/>
