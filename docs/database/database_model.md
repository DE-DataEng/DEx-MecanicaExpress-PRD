# 🚗 DEx CarCare - Modelagem de Banco de Dados (PostgreSQL)

## 📌 Visão Geral

Este documento descreve a modelagem do banco de dados do sistema **DEx CarCare**, voltado para gestão de oficinas mecânicas.

O modelo foi projetado para:

* Controle de clientes e veículos
* Gestão de orçamentos
* Execução de ordens de serviço
* Controle de peças e estoque
* Gestão de usuários e funcionários

---

## 🧱 Arquitetura de Dados

### Entidades principais

| Entidade            | Descrição                |
| ------------------- | ------------------------ |
| funcionarios        | Colaboradores da oficina |
| usuarios            | Acesso ao sistema        |
| clientes            | Clientes da oficina      |
| veiculos            | Veículos dos clientes    |
| pecas               | Produtos e peças         |
| orcamentos          | Propostas comerciais     |
| orcamento_itens     | Itens do orçamento       |
| ordens_servico      | Execução dos serviços    |
| ordem_servico_itens | Serviços executados      |
| ordem_servico_pecas | Peças utilizadas         |

---

## 📊 Modelo Relacional

### 🔹 clientes → veiculos

* Um cliente pode possuir vários veículos

### 🔹 funcionarios → usuarios

* Um funcionário pode possuir um usuário de acesso

### 🔹 clientes → orcamentos

* Um cliente pode possuir vários orçamentos

### 🔹 orcamentos → orcamento_itens

* Um orçamento possui vários itens

### 🔹 clientes → ordens_servico

* Um cliente pode possuir várias ordens de serviço

### 🔹 ordens_servico → itens / pecas

* Uma OS pode conter:

  * Serviços
  * Peças

---

## 🗂️ Estrutura das Tabelas

---

### 👨‍🔧 funcionarios

Armazena os colaboradores da oficina.

**Principais campos:**

* id_funcionario (PK)
* nome
* cpf
* cargo
* salario
* ativo

---

### 🔐 usuarios

Controle de acesso ao sistema.

**Relacionamento:**

* FK com funcionarios

**Principais campos:**

* login
* senha_hash
* perfil (ADMIN, MECANICO, etc)

---

### 👤 clientes

Cadastro de clientes PF/PJ.

**Principais campos:**

* nome
* tipo_pessoa (PF/PJ)
* cpf_cnpj
* telefone
* endereco

---

### 🚗 veiculos

Veículos vinculados ao cliente.

**Relacionamento:**

* FK com clientes

**Principais campos:**

* placa
* marca
* modelo
* ano
* quilometragem

---

### 🔩 pecas

Controle de peças e estoque.

**Principais campos:**

* descricao
* quantidade_estoque
* valor_custo
* valor_venda

---

### 📄 orcamentos

Propostas comerciais antes da execução.

**Relacionamentos:**

* cliente
* veiculo
* funcionario

**Status possíveis:**

* ABERTO
* APROVADO
* REPROVADO
* CANCELADO
* FINALIZADO

---

### 📋 orcamento_itens

Itens do orçamento.

**Tipos:**

* PECA
* SERVICO

---

### 🛠️ ordens_servico

Execução do serviço.

**Relacionamentos:**

* cliente
* veiculo
* orçamento (opcional)

**Status:**

* ABERTA
* EM_ANDAMENTO
* FINALIZADA
* ENTREGUE

---

### 🧰 ordem_servico_itens

Serviços realizados.

---

### 📦 ordem_servico_pecas

Peças utilizadas na OS.

---

## 🔄 Fluxo de Negócio

```text
Cliente → Veículo → Orçamento → Aprovação → Ordem de Serviço → Execução → Entrega
```

---

## ⚙️ Regras de Negócio

### ✔️ Separação de conceitos

| Conceito         | Descrição |
| ---------------- | --------- |
| Orçamento        | Proposta  |
| Ordem de Serviço | Execução  |

---

### ✔️ Itens separados

* Serviços ≠ Peças
* Permite:

  * Controle financeiro
  * Controle de estoque
  * Relatórios detalhados

---

### ✔️ Usuário vs Funcionário

| Tipo        | Função            |
| ----------- | ----------------- |
| funcionario | Pessoa física     |
| usuario     | Acesso ao sistema |

---

## 📈 Índices recomendados

```sql
clientes(nome)
veiculos(placa)
ordens_servico(status)
pecas(descricao)
```

---

## 🚀 Evoluções futuras

### Módulos recomendados

* 💳 Pagamentos
* 📦 Estoque avançado
* 🧾 Nota fiscal
* 📅 Agenda de serviços
* 📊 Dashboard (KPIs)
* 🔍 Auditoria (log)

---

## 🧠 Boas práticas adotadas

* Uso de `BIGSERIAL` para PK
* Uso de `CHECK` para status
* Separação de responsabilidades
* Normalização (3FN)
* Campos de auditoria (dt_criacao, dt_atualizacao)

---

## 📌 Padrões utilizados

| Item    | Padrão                  |
| ------- | ----------------------- |
| PK      | id_<tabela>             |
| FK      | id_<tabela_relacionada> |
| Datas   | dt_*                    |
| Boolean | ativo                   |

---

## 🏁 Conclusão

Este modelo atende:

✔ Oficinas pequenas
✔ Oficinas médias
✔ Escalável para ERP automotivo

---

## 📎 Próximo passo

Implementar:

* Script SQL completo
* API (FastAPI / Flask)
* Interface (Flet 0.28.3)
* Autenticação com Argon2

---
