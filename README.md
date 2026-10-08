# Projeto IAL214 - Grupo 2

Sistema web de acompanhamento da Fazenda Boa Vista, em Garça/SP, para apoiar a consulta de leituras de sensores, operações agrícolas, custos, alertas e imagens NDVI. O recorte funcional será confirmado pelo grupo depois da validação das consultas aos cinco serviços.

## Grupo

- Fazenda: Fazenda Boa Vista, café arábica, 255 ha e seis talhões.
- Vitor Studzieski, RA 2591262422005 ([GitHub](https://github.com/Vitor-Studzieski))
- Maria Fernanda Passos Françoso, RA 2591262422006 ([GitHub](https://github.com/MaferPassos))
- Lauan Alves, RA 2591262422018 ([GitHub](https://github.com/lauan2004))
- Luan Martinhão, RA 2591262422017 ([GitHub](https://github.com/luanm4rtinhao))
- Simplicio José, RA 2591262422020 ([GitHub](https://github.com/S1mplicio-Jose))
- Repositório remoto: https://github.com/Vitor-Studzieski/Pi-5termo

### Responsabilidades planejadas

- Vitor: coordenação, consultas MariaDB, custos/produtividade e integração das telas.
- Maria Fernanda: consultas MongoDB históricas e adaptador histórico.
- Lauan: interface, wireframes, Redis/MQTT e estado recente.
- Luan: containers, MinIO, deploy e documentação operacional.
- Simplicio: validação integrada das consultas, indicadores de qualidade e evidências para a P2.

## Escopo da P1

A P1 planeja o sistema e documenta o estudo dos dados. O sistema ainda não está implementado neste repositório. A entrega da disciplina é um PDF do grupo, enviado individualmente por cada integrante.

## Documentacao

- [Relatorio P1 editavel](docs/p1/relatorio.md)
- [Inventario de dados e consultas](docs/p1/inventario-dados.md)
- [Qualidade dos dados](docs/p1/qualidade-dados.md)
- [Fontes dos diagramas](docs/p1/arquitetura/)
- [Wireframes](docs/p1/wireframes/)
- [Consultas reproduziveis](docs/p1/consultas/)
- [ADR-001 - arquitetura proposta](docs/decisoes/ADR-001-arquitetura.md)
- [Instrucoes de operacao](docs/operacao.md)

## Acessos e seguranca

Copie `.env.example` para `.env` e preencha localmente com a folha de acessos do Grupo 2. O `.env` é ignorado pelo Git. Nunca coloque senhas, tokens, URIs autenticadas ou a folha de acessos no repositório. As consultas listadas em `docs/p1/consultas/` são somente de leitura.

## Estado da entrega

O PDF em `docs/p1/P1_IAL214_Grupo2.pdf` é uma versão de trabalho até que o grupo execute as consultas nos serviços e confirme a divisão de tarefas e a porta pública. Resultados sem execução real não devem ser preenchidos por estimativa.
