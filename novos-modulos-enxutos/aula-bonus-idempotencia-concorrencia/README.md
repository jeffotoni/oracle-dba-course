# Aula bônus - Idempotência, concorrência e integridade transacional no Oracle

Esta aula bônus mostra como proteger operações transacionais contra duplicidade e inconsistência quando diferentes solicitações chegam ao mesmo tempo. O exemplo usa pagamentos, saldo bancário, Oracle, duas sessões concorrentes e pequenos programas em Go.

Ela pode começar ao final da Aula 3 - Módulo 2 e ser concluída em outro encontro, caso o tempo da aula principal termine.

## O que será compreendido

Ao terminar a aula, deve ser possível:

- explicar o conceito de idempotência;
- entender por que uma requisição pode ser processada duas vezes;
- identificar a função de uma chave de idempotência;
- explicar por que `SELECT COUNT(*)` antes do `INSERT` não garante exclusividade;
- usar uma constraint `UNIQUE` para proteger uma regra de negócio;
- observar o comportamento de duas sessões concorrentes;
- diferenciar idempotência de lock;
- usar `SELECT ... FOR UPDATE` para proteger uma alteração de saldo;
- usar `CHECK` para impedir um estado inválido no banco;
- organizar `COMMIT` e `ROLLBACK` dentro de uma transação;
- relacionar uma API, uma aplicação Go e uma restrição no Oracle.

## Relação com as aulas anteriores

O laboratório aproveita conceitos já trabalhados:

```text
Módulo 1 -> usuário, schema, tabela e conexão Oracle
Módulo 2 -> privilégios, operação da aplicação e validação
Go + Oracle -> aplicação acessando a mesma tabela
Módulo 4 -> concorrência, espera e locks como aprofundamento
```

## 1. O que é idempotência?

Uma operação é idempotente quando repetir a mesma solicitação não produz um novo efeito depois que ela já foi processada.

Exemplo:

```text
Pagamento: R$ 150,00

Primeira tentativa
    -> processado com sucesso

Segunda tentativa da mesma operação
    -> não deve gerar um segundo pagamento
```

Uma forma simples de representar a regra é:

```text
mesma operação
+
mesma chave de idempotência
=
um único efeito
```

Esse padrão aparece em:

- pagamentos;
- transferências;
- pedidos;
- emissão de documentos;
- criação de recursos;
- integrações entre sistemas;
- processamento de mensagens e eventos.

## 2. Por que a mesma operação pode chegar duas vezes?

Imagine uma aplicação enviando um pagamento:

```text
Aplicação
    -> API
        -> Oracle
```

O Oracle confirma a operação, mas a conexão cai antes que a resposta chegue ao cliente:

```text
Aplicação
    -> API
        -> Oracle
            -> COMMIT realizado
            -> conexão caiu antes da resposta
```

O cliente não sabe se o pagamento foi processado. Ele tenta novamente.

Sem proteção:

```text
tentativa 1 -> R$ 150,00
tentativa 2 -> R$ 150,00

total processado -> R$ 300,00
```

O problema não é necessariamente o Oracle ter falhado. O problema é a aplicação não conseguir distinguir uma nova operação de uma repetição da mesma operação.

## 3. Chave de idempotência

A aplicação envia uma chave única para identificar a solicitação lógica:

```text
idempotency_key = PAY-ABC-123
```

Se a mesma solicitação for reenviada, a chave permite localizar a operação original.

```text
PAY-ABC-123
    -> primeira chamada: processa
    -> repetição: identifica que já existe
```

A chave pode ser gerada pelo cliente, pela API ou por um serviço responsável pela operação. O importante é que a mesma operação use a mesma chave e operações diferentes usem chaves diferentes.

## 4. Proteção no banco

A aplicação pode ajudar a controlar o fluxo, mas a garantia final deve estar no banco. Todas as instâncias da aplicação podem chegar ao mesmo Oracle simultaneamente.

```text
Aplicação 1 ----\
Aplicação 2 -----> Oracle
Aplicação 3 ----/
```

Uma constraint `UNIQUE` transforma a regra de negócio em uma regra de integridade:

```text
uma idempotency_key
    -> no máximo um registro
```

A constraint não depende de uma única instância da API, de um `SELECT` anterior ou de um controle mantido somente em memória.

## 5. Idempotência e concorrência são problemas diferentes

Os conceitos se relacionam, mas respondem a perguntas diferentes:

```text
Idempotência -> esta operação lógica já foi processada?
Concorrência -> outra transação está alterando este registro agora?
```

As proteções também são diferentes:

| Problema | Proteção principal |
| :--- | :--- |
| Mesma operação repetida | `UNIQUE (idempotency_key)` |
| Duas sessões alterando o mesmo saldo | `SELECT ... FOR UPDATE` |
| Saldo ou estado inválido | `CHECK (balance >= 0)` |
| Estado parcial | Transação com `COMMIT` ou `ROLLBACK` |

Mapa mental:

```text
OPERAÇÃO FINANCEIRA
        |
        +--> mesma operação repetida?
        |        |
        |        +--> UNIQUE(idempotency_key)
        |
        +--> mesmo registro alterado por outra sessão?
        |        |
        |        +--> SELECT ... FOR UPDATE
        |
        +--> estado inválido persistido?
                 |
                 +--> CHECK(balance >= 0)
```

O `UNIQUE` evita duplicidade lógica. O `FOR UPDATE` coordena transações concorrentes. O `CHECK` impede que um estado inválido seja persistido.

## 6. Como usar este bônus

Execute o [laboratório passo a passo](./pratica.md) nesta ordem:

1. criar a tabela de pagamentos;
2. demonstrar a duplicidade sem proteção;
3. adicionar a constraint `UNIQUE`;
4. repetir a operação e observar o `ORA-00001`;
5. reproduzir a concorrência em duas sessões Oracle;
6. criar uma conta com saldo controlado;
7. proteger um débito com `SELECT ... FOR UPDATE`;
8. disparar dois débitos concorrentes com Go;
9. validar que somente um débito foi realizado.

## Resultado esperado

```text
mesma chave repetida
    -> 1 registro efetivo

dois débitos concorrentes
    -> 1 operação aceita
    -> 1 operação rejeitada por saldo insuficiente

saldo final consistente
    -> nenhuma regra inválida persistida
```

Nesta primeira versão, a segunda tentativa será rejeitada pelo banco. Em uma API real, a aplicação pode capturar a duplicidade e retornar a resposta já registrada na primeira tentativa.

Referências relacionadas:

- [Aula 1 - Fundamentos do Oracle](../aula-1-modulo1/README.md)
- [Aula 3 - Segurança e carga de dados](../aula-3-modulo2/README.md)
- [Exemplo Go + Oracle](../../repo/go.oracle/v1/README.md)
