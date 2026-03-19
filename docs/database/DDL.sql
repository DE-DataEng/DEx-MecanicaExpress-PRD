-- =========================================================
-- PROJETO: OFICINA MECÂNICA
-- BANCO   : PostgreSQL
-- SCHEMA  : oficina
-- =========================================================

-- =========================================================
-- 1. CRIAÇÃO DO SCHEMA
-- =========================================================
CREATE SCHEMA IF NOT EXISTS oficina;

SET search_path TO oficina;

-- =========================================================
-- 2. FUNÇÃO PADRÃO PARA ATUALIZAR dt_atualizacao
-- =========================================================
CREATE OR REPLACE FUNCTION fn_set_dt_atualizacao()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.dt_atualizacao := CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

-- =========================================================
-- 3. TABELA: funcionarios
-- =========================================================
CREATE TABLE IF NOT EXISTS funcionarios (
    id_funcionario      BIGSERIAL PRIMARY KEY,
    nome                VARCHAR(150) NOT NULL,
    cpf                 VARCHAR(14) UNIQUE,
    telefone            VARCHAR(20),
    email               VARCHAR(150),
    cargo               VARCHAR(80),
    salario             NUMERIC(12,2),
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    dt_admissao         DATE,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE funcionarios IS 'Cadastro de colaboradores da oficina';
COMMENT ON COLUMN funcionarios.id_funcionario IS 'Identificador único do funcionário';
COMMENT ON COLUMN funcionarios.nome IS 'Nome completo do funcionário';
COMMENT ON COLUMN funcionarios.cpf IS 'CPF do funcionário';
COMMENT ON COLUMN funcionarios.cargo IS 'Cargo exercido na oficina';

-- =========================================================
-- 4. TABELA: usuarios
-- =========================================================
CREATE TABLE IF NOT EXISTS usuarios (
    id_usuario          BIGSERIAL PRIMARY KEY,
    id_funcionario      BIGINT,
    login               VARCHAR(60) NOT NULL UNIQUE,
    senha_hash          VARCHAR(255) NOT NULL,
    perfil              VARCHAR(30) NOT NULL,
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    dt_ultimo_login     TIMESTAMP,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_usuarios_funcionarios
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id_funcionario)
        ON DELETE SET NULL,
    CONSTRAINT ck_usuarios_perfil
        CHECK (perfil IN ('ADMIN', 'GERENTE', 'ATENDENTE', 'MECANICO'))
);

COMMENT ON TABLE usuarios IS 'Usuários de acesso ao sistema';
COMMENT ON COLUMN usuarios.senha_hash IS 'Hash da senha do usuário';
COMMENT ON COLUMN usuarios.perfil IS 'Perfil de acesso do usuário';

-- =========================================================
-- 5. TABELA: clientes
-- =========================================================
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente          BIGSERIAL PRIMARY KEY,
    nome                VARCHAR(150) NOT NULL,
    tipo_pessoa         VARCHAR(2) NOT NULL,
    cpf_cnpj            VARCHAR(18) UNIQUE,
    rg_ie               VARCHAR(20),
    telefone            VARCHAR(20),
    celular             VARCHAR(20),
    email               VARCHAR(150),
    cep                 VARCHAR(10),
    endereco            VARCHAR(150),
    numero              VARCHAR(20),
    complemento         VARCHAR(80),
    bairro              VARCHAR(80),
    cidade              VARCHAR(80),
    uf                  CHAR(2),
    observacoes         TEXT,
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_clientes_tipo_pessoa
        CHECK (tipo_pessoa IN ('PF', 'PJ')),
    CONSTRAINT ck_clientes_uf
        CHECK (uf IS NULL OR LENGTH(uf) = 2)
);

COMMENT ON TABLE clientes IS 'Cadastro de clientes da oficina';

-- =========================================================
-- 6. TABELA: veiculos
-- =========================================================
CREATE TABLE IF NOT EXISTS veiculos (
    id_veiculo          BIGSERIAL PRIMARY KEY,
    id_cliente          BIGINT NOT NULL,
    placa               VARCHAR(10) NOT NULL UNIQUE,
    chassi              VARCHAR(30),
    renavam             VARCHAR(20),
    marca               VARCHAR(60) NOT NULL,
    modelo              VARCHAR(80) NOT NULL,
    versao              VARCHAR(80),
    ano_fabricacao      INTEGER,
    ano_modelo          INTEGER,
    cor                 VARCHAR(40),
    combustivel         VARCHAR(20),
    quilometragem       INTEGER,
    observacoes         TEXT,
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_veiculos_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT,
    CONSTRAINT ck_veiculos_combustivel
        CHECK (
            combustivel IS NULL OR
            combustivel IN ('GASOLINA', 'ETANOL', 'FLEX', 'DIESEL', 'GNV', 'ELETRICO', 'HIBRIDO')
        ),
    CONSTRAINT ck_veiculos_quilometragem
        CHECK (quilometragem IS NULL OR quilometragem >= 0)
);

COMMENT ON TABLE veiculos IS 'Veículos vinculados aos clientes';

-- =========================================================
-- 7. TABELA: pecas
-- =========================================================
CREATE TABLE IF NOT EXISTS pecas (
    id_peca             BIGSERIAL PRIMARY KEY,
    codigo_interno      VARCHAR(50) UNIQUE,
    descricao           VARCHAR(150) NOT NULL,
    fabricante          VARCHAR(80),
    unidade             VARCHAR(10) NOT NULL DEFAULT 'UN',
    quantidade_estoque  NUMERIC(12,3) NOT NULL DEFAULT 0,
    valor_custo         NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_venda         NUMERIC(12,2) NOT NULL DEFAULT 0,
    estoque_minimo      NUMERIC(12,3) NOT NULL DEFAULT 0,
    ativo               BOOLEAN NOT NULL DEFAULT TRUE,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT ck_pecas_qtd_estoque
        CHECK (quantidade_estoque >= 0),
    CONSTRAINT ck_pecas_valor_custo
        CHECK (valor_custo >= 0),
    CONSTRAINT ck_pecas_valor_venda
        CHECK (valor_venda >= 0),
    CONSTRAINT ck_pecas_estoque_minimo
        CHECK (estoque_minimo >= 0)
);

COMMENT ON TABLE pecas IS 'Cadastro de peças e produtos';

-- =========================================================
-- 8. TABELA: orcamentos
-- =========================================================
CREATE TABLE IF NOT EXISTS orcamentos (
    id_orcamento        BIGSERIAL PRIMARY KEY,
    numero_orcamento    VARCHAR(20) NOT NULL UNIQUE,
    id_cliente          BIGINT NOT NULL,
    id_veiculo          BIGINT NOT NULL,
    id_funcionario      BIGINT,
    status              VARCHAR(20) NOT NULL DEFAULT 'ABERTO',
    valor_pecas         NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_servicos      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_desconto      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_total         NUMERIC(12,2) NOT NULL DEFAULT 0,
    observacoes         TEXT,
    dt_orcamento        TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_validade         DATE,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orcamentos_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT,
    CONSTRAINT fk_orcamentos_veiculos
        FOREIGN KEY (id_veiculo)
        REFERENCES veiculos(id_veiculo)
        ON DELETE RESTRICT,
    CONSTRAINT fk_orcamentos_funcionarios
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id_funcionario)
        ON DELETE SET NULL,
    CONSTRAINT ck_orcamentos_status
        CHECK (status IN ('ABERTO', 'APROVADO', 'REPROVADO', 'CANCELADO', 'FINALIZADO')),
    CONSTRAINT ck_orcamentos_valor_pecas
        CHECK (valor_pecas >= 0),
    CONSTRAINT ck_orcamentos_valor_servicos
        CHECK (valor_servicos >= 0),
    CONSTRAINT ck_orcamentos_valor_desconto
        CHECK (valor_desconto >= 0),
    CONSTRAINT ck_orcamentos_valor_total
        CHECK (valor_total >= 0)
);

COMMENT ON TABLE orcamentos IS 'Cabeçalho dos orçamentos';

-- =========================================================
-- 9. TABELA: orcamento_itens
-- =========================================================
CREATE TABLE IF NOT EXISTS orcamento_itens (
    id_orcamento_item   BIGSERIAL PRIMARY KEY,
    id_orcamento        BIGINT NOT NULL,
    tipo_item           VARCHAR(10) NOT NULL,
    id_peca             BIGINT,
    descricao           VARCHAR(150) NOT NULL,
    quantidade          NUMERIC(12,3) NOT NULL DEFAULT 1,
    valor_unitario      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_total         NUMERIC(12,2) NOT NULL DEFAULT 0,
    observacoes         TEXT,
    CONSTRAINT fk_orcamento_itens_orcamentos
        FOREIGN KEY (id_orcamento)
        REFERENCES orcamentos(id_orcamento)
        ON DELETE CASCADE,
    CONSTRAINT fk_orcamento_itens_pecas
        FOREIGN KEY (id_peca)
        REFERENCES pecas(id_peca)
        ON DELETE SET NULL,
    CONSTRAINT ck_orcamento_itens_tipo_item
        CHECK (tipo_item IN ('PECA', 'SERVICO')),
    CONSTRAINT ck_orcamento_itens_quantidade
        CHECK (quantidade > 0),
    CONSTRAINT ck_orcamento_itens_valor_unitario
        CHECK (valor_unitario >= 0),
    CONSTRAINT ck_orcamento_itens_valor_total
        CHECK (valor_total >= 0)
);

COMMENT ON TABLE orcamento_itens IS 'Itens do orçamento: peças e serviços';

-- =========================================================
-- 10. TABELA: ordens_servico
-- =========================================================
CREATE TABLE IF NOT EXISTS ordens_servico (
    id_ordem_servico    BIGSERIAL PRIMARY KEY,
    numero_os           VARCHAR(20) NOT NULL UNIQUE,
    id_orcamento        BIGINT,
    id_cliente          BIGINT NOT NULL,
    id_veiculo          BIGINT NOT NULL,
    id_funcionario      BIGINT,
    status              VARCHAR(25) NOT NULL DEFAULT 'ABERTA',
    defeito_relatado    TEXT,
    diagnostico         TEXT,
    observacoes         TEXT,
    valor_pecas         NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_servicos      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_desconto      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_total         NUMERIC(12,2) NOT NULL DEFAULT 0,
    dt_abertura         TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_fechamento       TIMESTAMP,
    dt_criacao          TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dt_atualizacao      TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_os_orcamentos
        FOREIGN KEY (id_orcamento)
        REFERENCES orcamentos(id_orcamento)
        ON DELETE SET NULL,
    CONSTRAINT fk_os_clientes
        FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE RESTRICT,
    CONSTRAINT fk_os_veiculos
        FOREIGN KEY (id_veiculo)
        REFERENCES veiculos(id_veiculo)
        ON DELETE RESTRICT,
    CONSTRAINT fk_os_funcionarios
        FOREIGN KEY (id_funcionario)
        REFERENCES funcionarios(id_funcionario)
        ON DELETE SET NULL,
    CONSTRAINT ck_os_status
        CHECK (
            status IN (
                'ABERTA',
                'EM_ANDAMENTO',
                'AGUARDANDO_APROVACAO',
                'FINALIZADA',
                'ENTREGUE',
                'CANCELADA'
            )
        ),
    CONSTRAINT ck_os_valor_pecas
        CHECK (valor_pecas >= 0),
    CONSTRAINT ck_os_valor_servicos
        CHECK (valor_servicos >= 0),
    CONSTRAINT ck_os_valor_desconto
        CHECK (valor_desconto >= 0),
    CONSTRAINT ck_os_valor_total
        CHECK (valor_total >= 0)
);

COMMENT ON TABLE ordens_servico IS 'Cabeçalho das ordens de serviço';

-- =========================================================
-- 11. TABELA: ordem_servico_itens
-- =========================================================
CREATE TABLE IF NOT EXISTS ordem_servico_itens (
    id_os_item          BIGSERIAL PRIMARY KEY,
    id_ordem_servico    BIGINT NOT NULL,
    descricao_servico   VARCHAR(150) NOT NULL,
    quantidade          NUMERIC(12,2) NOT NULL DEFAULT 1,
    valor_unitario      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_total         NUMERIC(12,2) NOT NULL DEFAULT 0,
    observacoes         TEXT,
    CONSTRAINT fk_os_itens_os
        FOREIGN KEY (id_ordem_servico)
        REFERENCES ordens_servico(id_ordem_servico)
        ON DELETE CASCADE,
    CONSTRAINT ck_os_itens_quantidade
        CHECK (quantidade > 0),
    CONSTRAINT ck_os_itens_valor_unitario
        CHECK (valor_unitario >= 0),
    CONSTRAINT ck_os_itens_valor_total
        CHECK (valor_total >= 0)
);

COMMENT ON TABLE ordem_servico_itens IS 'Serviços executados na ordem de serviço';

-- =========================================================
-- 12. TABELA: ordem_servico_pecas
-- =========================================================
CREATE TABLE IF NOT EXISTS ordem_servico_pecas (
    id_os_peca          BIGSERIAL PRIMARY KEY,
    id_ordem_servico    BIGINT NOT NULL,
    id_peca             BIGINT NOT NULL,
    quantidade          NUMERIC(12,3) NOT NULL DEFAULT 1,
    valor_unitario      NUMERIC(12,2) NOT NULL DEFAULT 0,
    valor_total         NUMERIC(12,2) NOT NULL DEFAULT 0,
    CONSTRAINT fk_os_pecas_os
        FOREIGN KEY (id_ordem_servico)
        REFERENCES ordens_servico(id_ordem_servico)
        ON DELETE CASCADE,
    CONSTRAINT fk_os_pecas_pecas
        FOREIGN KEY (id_peca)
        REFERENCES pecas(id_peca)
        ON DELETE RESTRICT,
    CONSTRAINT ck_os_pecas_quantidade
        CHECK (quantidade > 0),
    CONSTRAINT ck_os_pecas_valor_unitario
        CHECK (valor_unitario >= 0),
    CONSTRAINT ck_os_pecas_valor_total
        CHECK (valor_total >= 0)
);

COMMENT ON TABLE ordem_servico_pecas IS 'Peças utilizadas na ordem de serviço';

-- =========================================================
-- 13. ÍNDICES
-- =========================================================
CREATE INDEX IF NOT EXISTS idx_clientes_nome
    ON clientes (nome);

CREATE INDEX IF NOT EXISTS idx_clientes_cpf_cnpj
    ON clientes (cpf_cnpj);

CREATE INDEX IF NOT EXISTS idx_veiculos_cliente
    ON veiculos (id_cliente);

CREATE INDEX IF NOT EXISTS idx_veiculos_placa
    ON veiculos (placa);

CREATE INDEX IF NOT EXISTS idx_pecas_descricao
    ON pecas (descricao);

CREATE INDEX IF NOT EXISTS idx_orcamentos_cliente
    ON orcamentos (id_cliente);

CREATE INDEX IF NOT EXISTS idx_orcamentos_veiculo
    ON orcamentos (id_veiculo);

CREATE INDEX IF NOT EXISTS idx_orcamentos_status
    ON orcamentos (status);

CREATE INDEX IF NOT EXISTS idx_orcamento_itens_orcamento
    ON orcamento_itens (id_orcamento);

CREATE INDEX IF NOT EXISTS idx_os_cliente
    ON ordens_servico (id_cliente);

CREATE INDEX IF NOT EXISTS idx_os_veiculo
    ON ordens_servico (id_veiculo);

CREATE INDEX IF NOT EXISTS idx_os_status
    ON ordens_servico (status);

CREATE INDEX IF NOT EXISTS idx_os_itens_os
    ON ordem_servico_itens (id_ordem_servico);

CREATE INDEX IF NOT EXISTS idx_os_pecas_os
    ON ordem_servico_pecas (id_ordem_servico);

CREATE INDEX IF NOT EXISTS idx_os_pecas_peca
    ON ordem_servico_pecas (id_peca);

-- =========================================================
-- 14. TRIGGERS PARA dt_atualizacao
-- =========================================================
DROP TRIGGER IF EXISTS trg_funcionarios_dt_atualizacao ON funcionarios;
CREATE TRIGGER trg_funcionarios_dt_atualizacao
BEFORE UPDATE ON funcionarios
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_usuarios_dt_atualizacao ON usuarios;
CREATE TRIGGER trg_usuarios_dt_atualizacao
BEFORE UPDATE ON usuarios
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_clientes_dt_atualizacao ON clientes;
CREATE TRIGGER trg_clientes_dt_atualizacao
BEFORE UPDATE ON clientes
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_veiculos_dt_atualizacao ON veiculos;
CREATE TRIGGER trg_veiculos_dt_atualizacao
BEFORE UPDATE ON veiculos
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_pecas_dt_atualizacao ON pecas;
CREATE TRIGGER trg_pecas_dt_atualizacao
BEFORE UPDATE ON pecas
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_orcamentos_dt_atualizacao ON orcamentos;
CREATE TRIGGER trg_orcamentos_dt_atualizacao
BEFORE UPDATE ON orcamentos
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

DROP TRIGGER IF EXISTS trg_ordens_servico_dt_atualizacao ON ordens_servico;
CREATE TRIGGER trg_ordens_servico_dt_atualizacao
BEFORE UPDATE ON ordens_servico
FOR EACH ROW
EXECUTE FUNCTION fn_set_dt_atualizacao();

-- =========================================================
-- 15. DADOS INICIAIS DE EXEMPLO
-- =========================================================

-- Funcionários
INSERT INTO funcionarios (
    nome, cpf, telefone, email, cargo, salario, ativo, dt_admissao
) VALUES
(
    'Administrador do Sistema',
    '000.000.000-00',
    '(44) 99999-0001',
    'admin@oficina.local',
    'GERENTE',
    5000.00,
    TRUE,
    CURRENT_DATE
),
(
    'João Mecânico',
    '111.111.111-11',
    '(44) 99999-0002',
    'joao@oficina.local',
    'MECANICO',
    3200.00,
    TRUE,
    CURRENT_DATE
)
ON CONFLICT (cpf) DO NOTHING;

-- Usuários
INSERT INTO usuarios (
    id_funcionario, login, senha_hash, perfil, ativo
)
SELECT
    f.id_funcionario,
    'admin',
    '$2b$12$EXEMPLOHASHADMIN',
    'ADMIN',
    TRUE
FROM funcionarios f
WHERE f.cpf = '000.000.000-00'
ON CONFLICT (login) DO NOTHING;

INSERT INTO usuarios (
    id_funcionario, login, senha_hash, perfil, ativo
)
SELECT
    f.id_funcionario,
    'joao',
    '$2b$12$EXEMPLOHASHJOAO',
    'MECANICO',
    TRUE
FROM funcionarios f
WHERE f.cpf = '111.111.111-11'
ON CONFLICT (login) DO NOTHING;

-- Clientes
INSERT INTO clientes (
    nome, tipo_pessoa, cpf_cnpj, telefone, celular, email, cep,
    endereco, numero, bairro, cidade, uf, ativo
) VALUES
(
    'Carlos Alberto Silva',
    'PF',
    '123.456.789-00',
    '(44) 3020-1000',
    '(44) 99999-1000',
    'carlos@email.com',
    '87000-000',
    'Rua Exemplo',
    '100',
    'Centro',
    'Maringá',
    'PR',
    TRUE
),
(
    'Transportadora Rota Sul LTDA',
    'PJ',
    '12.345.678/0001-99',
    '(44) 3020-2000',
    '(44) 99999-2000',
    'contato@rotasul.com.br',
    '87010-000',
    'Av. das Empresas',
    '500',
    'Zona 01',
    'Maringá',
    'PR',
    TRUE
)
ON CONFLICT (cpf_cnpj) DO NOTHING;

-- Veículos
INSERT INTO veiculos (
    id_cliente, placa, chassi, renavam, marca, modelo, versao,
    ano_fabricacao, ano_modelo, cor, combustivel, quilometragem, ativo
)
SELECT
    c.id_cliente,
    'ABC1D23',
    '9BWZZZ377VT004251',
    '12345678901',
    'Volkswagen',
    'Gol',
    '1.6',
    2018,
    2019,
    'Branco',
    'FLEX',
    85420,
    TRUE
FROM clientes c
WHERE c.cpf_cnpj = '123.456.789-00'
ON CONFLICT (placa) DO NOTHING;

INSERT INTO veiculos (
    id_cliente, placa, chassi, renavam, marca, modelo, versao,
    ano_fabricacao, ano_modelo, cor, combustivel, quilometragem, ativo
)
SELECT
    c.id_cliente,
    'DEF4G56',
    '8AFZZZ54ATJ123456',
    '10987654321',
    'Ford',
    'Ranger',
    'XLS 2.2',
    2020,
    2021,
    'Prata',
    'DIESEL',
    120300,
    TRUE
FROM clientes c
WHERE c.cpf_cnpj = '12.345.678/0001-99'
ON CONFLICT (placa) DO NOTHING;

-- Peças
INSERT INTO pecas (
    codigo_interno, descricao, fabricante, unidade,
    quantidade_estoque, valor_custo, valor_venda, estoque_minimo, ativo
) VALUES
(
    'PEC-0001',
    'Óleo 5W30 Sintético 1L',
    'Mobil',
    'UN',
    50,
    28.00,
    42.00,
    10,
    TRUE
),
(
    'PEC-0002',
    'Filtro de Óleo',
    'Tecfil',
    'UN',
    30,
    12.50,
    22.00,
    5,
    TRUE
),
(
    'PEC-0003',
    'Pastilha de Freio Dianteira',
    'Cobreq',
    'JG',
    12,
    65.00,
    110.00,
    2,
    TRUE
)
ON CONFLICT (codigo_interno) DO NOTHING;

-- Orçamento
INSERT INTO orcamentos (
    numero_orcamento,
    id_cliente,
    id_veiculo,
    id_funcionario,
    status,
    valor_pecas,
    valor_servicos,
    valor_desconto,
    valor_total,
    observacoes,
    dt_validade
)
SELECT
    'ORC-000001',
    c.id_cliente,
    v.id_veiculo,
    f.id_funcionario,
    'ABERTO',
    64.00,
    80.00,
    0.00,
    144.00,
    'Troca de óleo e filtro',
    CURRENT_DATE + INTERVAL '7 days'
FROM clientes c
JOIN veiculos v
    ON v.id_cliente = c.id_cliente
JOIN funcionarios f
    ON f.cpf = '000.000.000-00'
WHERE c.cpf_cnpj = '123.456.789-00'
  AND v.placa = 'ABC1D23'
ON CONFLICT (numero_orcamento) DO NOTHING;

-- Itens do orçamento
INSERT INTO orcamento_itens (
    id_orcamento, tipo_item, id_peca, descricao, quantidade, valor_unitario, valor_total, observacoes
)
SELECT
    o.id_orcamento,
    'PECA',
    p.id_peca,
    p.descricao,
    1,
    42.00,
    42.00,
    NULL
FROM orcamentos o
JOIN pecas p
    ON p.codigo_interno = 'PEC-0001'
WHERE o.numero_orcamento = 'ORC-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM orcamento_itens oi
      WHERE oi.id_orcamento = o.id_orcamento
        AND oi.tipo_item = 'PECA'
        AND oi.id_peca = p.id_peca
  );

INSERT INTO orcamento_itens (
    id_orcamento, tipo_item, id_peca, descricao, quantidade, valor_unitario, valor_total, observacoes
)
SELECT
    o.id_orcamento,
    'PECA',
    p.id_peca,
    p.descricao,
    1,
    22.00,
    22.00,
    NULL
FROM orcamentos o
JOIN pecas p
    ON p.codigo_interno = 'PEC-0002'
WHERE o.numero_orcamento = 'ORC-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM orcamento_itens oi
      WHERE oi.id_orcamento = o.id_orcamento
        AND oi.tipo_item = 'PECA'
        AND oi.id_peca = p.id_peca
  );

INSERT INTO orcamento_itens (
    id_orcamento, tipo_item, id_peca, descricao, quantidade, valor_unitario, valor_total, observacoes
)
SELECT
    o.id_orcamento,
    'SERVICO',
    NULL,
    'Mão de obra - troca de óleo e filtro',
    1,
    80.00,
    80.00,
    NULL
FROM orcamentos o
WHERE o.numero_orcamento = 'ORC-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM orcamento_itens oi
      WHERE oi.id_orcamento = o.id_orcamento
        AND oi.tipo_item = 'SERVICO'
        AND oi.descricao = 'Mão de obra - troca de óleo e filtro'
  );

-- Ordem de serviço
INSERT INTO ordens_servico (
    numero_os,
    id_orcamento,
    id_cliente,
    id_veiculo,
    id_funcionario,
    status,
    defeito_relatado,
    diagnostico,
    observacoes,
    valor_pecas,
    valor_servicos,
    valor_desconto,
    valor_total
)
SELECT
    'OS-000001',
    o.id_orcamento,
    o.id_cliente,
    o.id_veiculo,
    f.id_funcionario,
    'EM_ANDAMENTO',
    'Cliente solicitou troca de óleo e revisão básica',
    'Necessária troca de óleo e filtro',
    'Serviço iniciado',
    64.00,
    80.00,
    0.00,
    144.00
FROM orcamentos o
JOIN funcionarios f
    ON f.cpf = '111.111.111-11'
WHERE o.numero_orcamento = 'ORC-000001'
ON CONFLICT (numero_os) DO NOTHING;

-- Itens de serviço da OS
INSERT INTO ordem_servico_itens (
    id_ordem_servico, descricao_servico, quantidade, valor_unitario, valor_total, observacoes
)
SELECT
    os.id_ordem_servico,
    'Troca de óleo e filtro',
    1,
    80.00,
    80.00,
    'Executar conforme especificação do fabricante'
FROM ordens_servico os
WHERE os.numero_os = 'OS-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM ordem_servico_itens osi
      WHERE osi.id_ordem_servico = os.id_ordem_servico
        AND osi.descricao_servico = 'Troca de óleo e filtro'
  );

-- Peças da OS
INSERT INTO ordem_servico_pecas (
    id_ordem_servico, id_peca, quantidade, valor_unitario, valor_total
)
SELECT
    os.id_ordem_servico,
    p.id_peca,
    1,
    42.00,
    42.00
FROM ordens_servico os
JOIN pecas p
    ON p.codigo_interno = 'PEC-0001'
WHERE os.numero_os = 'OS-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM ordem_servico_pecas osp
      WHERE osp.id_ordem_servico = os.id_ordem_servico
        AND osp.id_peca = p.id_peca
  );

INSERT INTO ordem_servico_pecas (
    id_ordem_servico, id_peca, quantidade, valor_unitario, valor_total
)
SELECT
    os.id_ordem_servico,
    p.id_peca,
    1,
    22.00,
    22.00
FROM ordens_servico os
JOIN pecas p
    ON p.codigo_interno = 'PEC-0002'
WHERE os.numero_os = 'OS-000001'
  AND NOT EXISTS (
      SELECT 1
      FROM ordem_servico_pecas osp
      WHERE osp.id_ordem_servico = os.id_ordem_servico
        AND osp.id_peca = p.id_peca
  );

-- =========================================================
-- 16. CONSULTAS ÚTEIS DE TESTE
-- =========================================================

-- SELECT * FROM oficina.clientes;
-- SELECT * FROM oficina.veiculos;
-- SELECT * FROM oficina.pecas;
-- SELECT * FROM oficina.orcamentos;
-- SELECT * FROM oficina.orcamento_itens;
-- SELECT * FROM oficina.ordens_servico;
-- SELECT * FROM oficina.ordem_servico_itens;
-- SELECT * FROM oficina.ordem_servico_pecas;

-- =========================================================
-- FIM
-- =========================================================