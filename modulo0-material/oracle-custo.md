# Guia de Licenciamento e Custos Oracle

Este guia foi escrito para apoiar decisão técnica e financeira no início de projetos com Oracle.

Importante:
- Este material é educacional e não substitui contrato, proposta comercial ou parecer jurídico.
- Regras de licenciamento e preços podem mudar.
- Sempre valide a decisão final com representante Oracle e com o time jurídico da empresa.

Data-base desta versão: 28/04/2026.

## 1. Como usar este guia
Use este documento em três momentos:
1. Na fase de estimativa inicial de arquitetura e orçamento.
2. Na comparação entre On-Premises, OCI e multicloud.
3. Na revisão de riscos antes de contratação.

## 2. Conceitos financeiros essenciais

### 2.1 CAPEX
Investimento em ativos, como servidor físico e licença perpétua.

Vantagem:
- Controle maior do ambiente e amortização de longo prazo.

Ponto de atenção:
- Exige caixa inicial alto e planejamento de capacidade futuro.

### 2.2 OPEX
Despesa operacional recorrente, típica de nuvem por consumo.

Vantagem:
- Ajuste de custo ao uso real.

Ponto de atenção:
- Sem governança, o custo mensal pode crescer silenciosamente.

### 2.3 TCO
TCO é o custo total de propriedade. Não inclui só licença.

Itens que entram no TCO:
- Licença e suporte.
- Infraestrutura e energia.
- Backup e recuperação.
- Equipe de operação.
- Segurança, auditoria e compliance.

## 3. Licenciamento On-Premises, visão prática

### 3.1 Métricas comuns
- `Processor`: custo baseado em capacidade de processamento.
- `Named User Plus (NUP)`: custo por usuário nomeado, não por concorrência.

### 3.2 Fórmula de Processor License
Fórmula didática:
`Processor Licenses = cores físicos x core factor`

Regra de arredondamento:
- Resultado fracionado deve ser arredondado para cima.

Exemplo:
- 16 cores físicos em processador x86 com fator 0,5.
- `16 x 0,5 = 8` licenças Processor.

### 3.3 Regra de NUP mínimo
Para Oracle Database Enterprise Edition, regra usada com frequência em estimativas:
- `NUP mínimo = Processor Licenses x 25`

Exemplo:
- 8 licenças Processor.
- `8 x 25 = 200` NUP mínimos.

Observação:
- Para cenários com Standard Edition 2, confira mínimos contratuais vigentes no momento da compra.

### 3.4 Suporte anual
Regra comum de referência:
- Suporte anual em torno de 22% do valor líquido licenciado.

O que o suporte cobre na prática:
- Atualizações de segurança.
- Correções.
- Abertura de chamados técnicos.

### 3.5 Preço de lista, cuidado necessário
Preço de lista não é preço final de contrato.

Preço final costuma depender de:
- Volume de licenças.
- Prazo do acordo.
- Programas comerciais e parceria.
- Escopo fechado de produtos adicionais.

## 4. Dimensionamento técnico antes do custo

Antes de falar em preço, licença ou cloud, é necessário estimar a carga real do ambiente. Um erro comum é dizer apenas "tenho 100 mil usuários". Esse número sozinho não define capacidade.

O que realmente muda o desenho e o custo:
- Quantas transações por minuto (`TPM`).
- Quantas queries por segundo (`QPS`).
- Percentual de leitura versus escrita.
- Complexidade das consultas e relatórios.
- Latência esperada.
- Pico de uso, sazonalidade e janela de batch.
- Retenção de dados, backup e recuperação.

### 4.1 Por que usuários simultâneos não bastam

`100 mil usuários logados` pode representar cenários muito diferentes:

| Situação | Leitura prática |
| :--- | :--- |
| Usuários logados com leitura eventual | Pode ser relativamente leve, se houver cache e poucas escritas. |
| Usuários fazendo checkout, pagamento e relatórios | Pode ser pesado, pois mistura escrita, transação crítica e consulta complexa. |
| Muitos usuários, mas baixa concorrência real | Pode exigir menos banco do que parece. |
| Poucos usuários, mas consultas analíticas pesadas | Pode exigir muita CPU, I/O e tuning. |

Por isso, em estimativa Oracle, a conversa precisa sair de "número de usuários" e ir para **volume transacional, concorrência real, I/O, SLA e criticidade**.

### 4.2 Matriz didática de capacidade e custo mensal

A matriz abaixo é apenas educacional. Os valores são faixas amplas para raciocínio inicial e podem variar muito por contrato, core factor, suporte, arquitetura, região cloud, add-ons e negociação comercial.

| Cenário Oracle | Carga estimada | Usuários simultâneos aprox. | Edição Oracle | Estratégia de escala | Infra típica Linux | Armazenamento | Custo mensal estimado USD | Perfil |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Médio porte** | 50k-150k TPM | 2k-8k | SE2 / EE | Vertical | 8-16 vCPU, 64-128 GB RAM | 1 TB SSD/NVMe | US$ 2k-8k | ERP, SaaS regional |
| **Grande porte** | 150k-500k TPM | 8k-40k | EE | Vertical + read replicas / Data Guard | 32-64 vCPU, 256-512 GB RAM | 1-4 TB NVMe + backup | US$ 8k-30k | E-commerce nacional, APIs pesadas |
| **Enterprise nacional** | 500k-2M TPM | 40k-150k | EE + RAC | Horizontal com RAC + vertical | 3-6 nós, cada nó 64-128 vCPU, 512 GB-1 TB RAM | SAN/NVMe distribuído | US$ 30k-120k+ | Bancos, telecom, missão crítica |
| **Missão crítica global** | 2M-10M+ TPM | 150k-1M+ | EE + RAC + Exadata | Horizontal massivo | Exadata / múltiplos clusters | Storage especializado + backup avançado | Muito variável / contrato enterprise | Grandes plataformas globais |

Notas:
- `TPM` significa `Transactions Per Minute`, ou transações por minuto.
- As faixas acima não substituem sizing técnico, benchmark, proposta comercial ou validação com Oracle.
- Licença Oracle pode variar drasticamente por métrica, core factor, suporte, options, RAC, Exadata, BYOL e contrato.

### 4.3 Escala vertical e horizontal em Oracle On-Premises

Em Oracle, a decisão de escala normalmente começa com **scale-up vertical** e só evolui para **scale-out horizontal** quando a carga, disponibilidade ou criticidade justificam a complexidade.

| Modelo de escala | Estrutura | Exemplo de hardware Linux | Escalabilidade | Vantagens | Desvantagens | Faixa típica de carga | Complexidade |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Vertical básico** | 1 servidor Oracle único | 16-32 vCPU, 64-128 GB RAM, SSD/NVMe | Aumenta CPU/RAM no mesmo host | Simples, menor custo inicial, fácil administrar | SPOF sem HA nativo, limite físico do servidor | Pequenas e médias cargas | Baixa |
| **Vertical robusto** | 1 servidor high-end + storage premium | 64-128 vCPU, 256-1024 GB RAM, NVMe/ASM | Scale-up agressivo | Excelente desempenho local, baixa latência | Muito dependente de uma máquina, upgrades caros | Alta carga transacional | Média |
| **Vertical + Standby** | Primário + standby com Data Guard | 2 servidores equivalentes | Escala principal vertical, HA por réplica | Disaster recovery, failover, segurança | Standby não escala escrita primária | Alta produção corporativa | Média/Alta |
| **Vertical + Active Data Guard** | Primário + réplicas de leitura | Primário robusto + nós de leitura | Escrita vertical, leitura parcialmente horizontal | Escala leitura, relatórios e DR | Escritas continuam centralizadas | Apps com leitura intensa | Alta |
| **RAC 2 nós** | 2 servidores compartilhando storage | 2x 32-64 vCPU, 256-512 GB RAM | Horizontal real | Alta disponibilidade, balanceamento | Licença alta, interconnect crítico | Grande porte | Alta |
| **RAC 4-8 nós** | Cluster RAC enterprise | 4-8 nós + SAN/ASM | Horizontal avançado | Alta resiliência, escala enterprise | Custo e administração muito altos | Bancos, telecom | Muito alta |
| **RAC + Exadata** | Oracle engineered systems | Exadata racks | Horizontal massivo + otimizações Oracle | Performance extrema, compressão, tuning integrado | Custo extremo | Missão crítica global | Extremamente alta |
| **Oracle Sharding** | Particionamento distribuído por região/domínio | Múltiplos clusters dedicados | Horizontal distribuído | Escala geográfica, segmentação por domínio | Arquitetura complexa | SaaS global / multi-região | Muito alta |

### 4.4 Conceito central: scale-up e scale-out

**Vertical (scale-up)** significa fortalecer uma máquina:
- Mais CPU.
- Mais RAM.
- Mais IOPS.
- Mais storage.
- Storage melhor, como NVMe, ASM ou SAN premium.

É o caminho mais comum para:
- Menor complexidade inicial.
- Primeira fase de operação.
- Ambientes SE2 e EE sem necessidade imediata de cluster.
- Cargas médias e até altas, dependendo do hardware.

**Horizontal (scale-out)** significa adicionar múltiplos nós ou réplicas:
- RAC.
- Sharding.
- Data Guard / Active Data Guard.
- Réplicas para leitura e relatórios.

É indicado quando há necessidade de:
- Alta disponibilidade.
- Failover.
- Distribuição de leitura.
- Escala geográfica.
- Missão crítica.

### 4.5 Desenho mental de arquitetura

Modelo vertical simples:

```txt
App Servers -> Load Balancer -> Oracle Server monolítico
```

Modelo horizontal com RAC:

```txt
App Servers -> Load Balancer -> RAC Node 1
                                RAC Node 2
                                RAC Node 3
```

Regra prática em Oracle:

1. Primeiro, use **vertical forte**.
2. Depois, adicione **Data Guard / Active Data Guard** quando precisar de DR, failover ou leitura separada.
3. Só depois, quando necessário e justificável, avance para **RAC**, **Exadata** ou **Sharding**.

### 4.6 Leitura prática da matriz

- **SE2** costuma fazer sentido quando a carga é previsível e os recursos avançados de EE não são obrigatórios.
- **EE** entra quando há necessidade de recursos enterprise, maior flexibilidade, particionamento, segurança avançada, tuning e opções pagas.
- **RAC** aparece quando a disponibilidade horizontal e continuidade justificam custo e complexidade.
- **Exadata** faz sentido quando performance, consolidação, I/O e suporte integrado justificam um patamar premium.
- **Cloud** pode reduzir fricção operacional, mas não elimina governança de custo.

## 5. Simulações didáticas de custo

As simulações abaixo são educacionais. Objetivo é praticar estrutura de cálculo.

### 5.0 Visão rápida dos cenários

| Cenário | Contexto | Métrica principal | Resultado esperado |
| :--- | :--- | :--- | :--- |
| **A** | Empresa pequena com SE2 por NUP | NUP | Estimar licença inicial, suporte anual e custo em 3 anos |
| **B** | Empresa média com EE por Processor | Cores x Core Factor | Calcular Processor Licenses e NUP mínimo de referência |
| **C** | OCI com BYOL | ECPU ou OCPU + storage | Projetar custo mensal com consumo real de nuvem |

### 5.1 Cenário A, empresa pequena com SE2 por NUP

| Item | Valor / Fórmula |
| :--- | :--- |
| Premissa 1 | 60 usuários nomeados |
| Premissa 2 | SE2 por NUP com preço de lista de referência histórica |
| Passo 1 | `Licença inicial = NUP x preço unitário` |
| Passo 2 | `Suporte anual = 22% x licença inicial` |
| Passo 3 | `Custo em 3 anos = licença inicial + 3 x suporte anual` |

Leitura do cenário:
- Melhor para fixar a lógica de NUP e o peso do suporte no custo total.

### 5.2 Cenário B, empresa média com EE por Processor

| Item | Valor / Fórmula |
| :--- | :--- |
| Premissa 1 | 2 servidores, cada um com 16 cores físicos x86 |
| Premissa 2 | Core Factor = `0,5` |
| Passo 1 | `Cores totais = 32` |
| Passo 2 | `Processor Licenses = 32 x 0,5 = 16` |
| Passo 3 | `NUP mínimo de referência = 16 x 25 = 400` |
| Passo 4 | Comparar custo de `EE Processor` versus `EE NUP` |

Leitura do cenário:
- Mostra como o hardware impacta diretamente o custo de licenciamento.

### 5.3 Cenário C, nuvem OCI com BYOL

| Item | Valor / Regra de análise |
| :--- | :--- |
| Premissa 1 | Empresa já possui licença perpétua |
| Premissa 2 | Meta é migrar para serviço gerenciado com elasticidade |
| Custo 1 | Compute (`ECPU` ou `OCPU`) |
| Custo 2 | Storage de dados |
| Custo 3 | Backup storage |
| Custo 4 | Tráfego quando aplicável |
| Risco comum | Subestimar storage, backup e ambientes não produtivos |

Leitura do cenário:
- Bom para entender que BYOL reduz parte da licença, mas não elimina custo de operação em nuvem.

## 6. OCI e nuvem, pontos de decisão

### 6.1 License Included vs BYOL
- `License Included`: licença já embutida no preço do serviço.
- `BYOL`: aproveita licença existente, reduzindo parte do custo recorrente.

Quando BYOL costuma fazer sentido:
- Empresa com parque licenciado ativo e governança de ativos madura.

### 6.2 Métricas ECPU e OCPU
No OCI atual, muitos serviços de banco já trabalham com ECPU, enquanto alguns cenários ainda usam OCPU.

Recomendação operacional:
- Validar a métrica da página oficial do serviço antes da estimativa.

### 6.3 Always Free
No serviço Always Free de Autonomous AI Database, a documentação oficial cita:
- até 2 bancos Always Free.
- limite aproximado de 20 GB por banco.

### 6.4 Custos ocultos que precisam entrar no orçamento
- Ambientes de homologação e contingência.
- Retenção de backup acima do básico.
- Tráfego de dados entre regiões.
- Ferramentas de observabilidade e segurança.
- Horas internas de operação e sustentação.

## 7. Estratégia multicloud

### 7.1 Oracle Database@AWS
- Situação oficial: GA em 08/07/2025.
- Uso típico: manter banco Oracle com serviços AWS próximos da aplicação.

### 7.2 Oracle Database@Google Cloud
- Situação oficial: GA em 09/09/2024.
- Uso típico: integração nativa com serviços de dados e IA no Google Cloud.

### 7.3 Oracle em ecossistema Azure
Existem dois modelos importantes:
- Oracle Database Service for Azure, banco em OCI com experiência integrada Azure.
- Oracle AI Database@Azure, banco Oracle operando em data centers Azure.

## 8. Matriz de decisão rápida

| Cenário | Caminho mais comum | Motivo |
| :--- | :--- | :--- |
| Equipe pequena, ambiente de estudo | XE | Custo zero e simplicidade. |
| PME com carga previsível | SE2 | Menor custo inicial com governança básica. |
| Missão crítica com requisitos avançados | EE | Recursos avançados e flexibilidade maior. |
| Empresa com licença já adquirida e meta de cloud | OCI com BYOL | Preserva investimento já feito. |
| Projeto novo com foco em agilidade operacional | OCI License Included | Menos fricção na entrada e operação. |

## 9. Checklist antes de fechar contrato
1. Confirmar a edição correta para o requisito técnico real.
2. Estimar carga real: `TPM`, `QPS`, leituras, escritas, picos e latência esperada.
3. Confirmar métrica correta de licenciamento (Processor ou NUP).
4. Calcular NUP mínimo quando aplicável.
5. Validar core factor do hardware real.
6. Incluir suporte anual na projeção de 3 e 5 anos.
7. Incluir custos de DR, backup, monitoramento e segurança.
8. Validar regras de BYOL para o serviço cloud escolhido.
9. Revisar cláusulas com jurídico e compras.

## 10. Referências oficiais
Data de consulta dos links: 28/04/2026.

Licenciamento e contratos:
- [Oracle AI Database 26ai - Licensing](https://docs.oracle.com/en/database/oracle/oracle-database/26/licensing.html)
- [Oracle AI Database Licensing Information User Manual 26ai (PDF)](https://docs.oracle.com/en/database/oracle/oracle-database/26/dblic/database-licensing-information-user-manual.pdf)
- [Oracle Processor Core Factor Table (atualizada em 28/01/2026)](https://www.oracle.com/contracts/docs/processor-core-factor-table-070634.pdf)
- [Oracle Technology Global Price List, 01/03/2025 (PDF)](https://www.oracle.com/bz/a/ocom/docs/corporate/pricing/technology-price-list-070617.pdf)

Preços e estimativas em nuvem:
- [Oracle Cloud Cost Estimator](https://www.oracle.com/cloud/cost-estimator.html)
- [Oracle Base Database Service Pricing (Brasil)](https://www.oracle.com/br/database/base-database-service/pricing/)
- [Autonomous AI Lakehouse Pricing](https://www.oracle.com/autonomous-database/autonomous-data-warehouse/pricing/)
- [Always Free Autonomous AI Database](https://docs.oracle.com/en-us/iaas/autonomous-database-shared/doc/autonomous-always-free.html)

Multicloud:
- [Oracle Database@AWS GA Announcement, 08/07/2025](https://www.oracle.com/news/announcement/oracle-database-at-aws-now-generally-available-2025-07-08/)
- [Oracle Database@Google Cloud GA Announcement, 09/09/2024](https://blogs.oracle.com/cloud-infrastructure/post/general-availability-oracle-database-google-cloud)
- [Oracle Database Service for Azure](https://www.oracle.com/cloud/azure/oracle-database-for-azure/)
- [Oracle AI Database@Azure Pricing](https://www.oracle.com/cloud/azure/oracle-database-at-azure/pricing/)
