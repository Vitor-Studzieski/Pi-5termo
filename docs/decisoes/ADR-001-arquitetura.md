# ADR-001 - Monólito web modular com coletor MQTT

- **Estado:** proposta para a P1; confirmar com o grupo.
- **Data:** 07/10/2026.

## Contexto

O grupo precisa concluir até 17/11/2026 um painel que consulta cinco serviços de dados. A equipe esperada tem quatro integrantes. O fluxo MQTT exige uma rotina durável de assinatura, reconexão e persistência, enquanto as telas consultam dados sob demanda.

## Opções consideradas

1. Monólito único com telas, API e consumidor MQTT no mesmo processo.
2. Monólito web modular e um container de ingestão MQTT.
3. Microsserviços separados por cada tela ou banco.

## Decisão

Adotar a opção 2: um monólito web organizado por módulos de domínio e adaptadores por serviço, mais um coletor MQTT sem porta pública. Os serviços gerenciados da disciplina são dependências externas, não containers do projeto.

## Motivos

A opção mantém poucas unidades de deploy, reduz trabalho operacional e permite que a equipe implemente as telas em paralelo. O coletor separado tem ciclo de execução e política de retentativa próprios; separá-lo da interface evita acoplamento entre requisições HTTP e consumo contínuo. Separar um microsserviço por tela aumentaria coordenação e configuração sem necessidade demonstrada na P1.

## Consequências

- O monólito web compartilha um deploy, mas cada domínio deve depender de uma interface de acesso ao serviço.
- O coletor e o web podem escalar e reiniciar separadamente.
- A persistência MQTT requer idempotência por tópico/sensor/timestamp, tratamento de atraso e monitoramento de falhas.
- O custo, a disponibilidade e a latência dos serviços de laboratório dependem da infraestrutura compartilhada.
- O grupo deverá confirmar a porta pública atribuída, usuários de menor privilégio e limites de retenção antes do deploy.
