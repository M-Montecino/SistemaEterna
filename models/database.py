import sqlite3

class Database:
    _instance = None

    def __init__(self, db_path="eterna.db"):
        self.coneccao = sqlite3.connect(db_path)
        self.coneccao.row_factory = sqlite3.Row
        self.coneccao.execute("PRAGMA foreign_keys = ON")
        self._criar_tabelas()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Database()
        return cls._instance

    def _criar_tabelas(self):
        cursor = self.coneccao.cursor()
        cursor.executescript("""
        CREATE TABLE IF NOT EXISTS pagamentos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            valor REAL NOT NULL,
            data_pagamento DATE NOT NULL,
            tipo_pagamento TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS responsaveis(
            cpf VARCHAR(11) PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone VARCHAR(11) NOT NULL,
            cep VARCHAR(8),
            numero INTEGER,
            email TEXT
        );

        CREATE TABLE IF NOT EXISTS falecidos(
            cpf VARCHAR(11) PRIMARY KEY,
            nome TEXT NOT NULL,
            data_nascimento DATE NOT NULL,
            data_falecimento DATE NOT NULL,
            causa_morte TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS tumulos(
            codigo INTEGER PRIMARY KEY,
            setor TEXT NOT NULL,
            numero INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            capacidade INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS concessoes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_pagamento INTEGER REFERENCES pagamentos(id),
            responsavel VARCHAR(11) REFERENCES responsaveis(cpf),
            responsavel2 VARCHAR(11) REFERENCES responsaveis(cpf),
            data_inicio DATE,
            data_fim DATE,
            status CHAR
        );

        CREATE TABLE IF NOT EXISTS sepultamentos(
            cpf_falecido VARCHAR(11) REFERENCES falecidos(cpf),
            tumulo INTEGER REFERENCES tumulos(codigo),
            id_concessao INTEGER REFERENCES concessoes(id),
            data_sepultamento DATE NOT NULL,
            ativo INTEGER,
            observacoes TEXT
        );

        CREATE TABLE IF NOT EXISTS exumacoes(
            codigo INTEGER PRIMARY KEY,
            data DATE NOT NULL,
            sepultamento VARCHAR(11) REFERENCES sepultamentos(cpf_falecido),
            destino TEXT NOT NULL,
            observacoes TEXT
        );

        CREATE TABLE IF NOT EXISTS manutencoes(
            codigoINTEGER PRIMARY KEY,
            tumulo INTEGER     REFERENCES tumulos(codigo),
            tipo_servico TEXT NOT NULL,
            data DATE NOT NULL,
            cpf_responsavel VARCHAR(11) REFERENCES responsaveis(cpf)
        );

        CREATE TABLE IF NOT EXISTS usuarios(
            cpf VARCHAR(11) PRIMARY KEY,
            nome  TEXT NOT NULL,
            cargo TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL
        );
        """)
        self._migrar_tabela_usuarios()
        self.coneccao.commit()

    def _migrar_tabela_usuarios(self):
        cursor = self.coneccao.cursor()
        colunas = {linha[1] for linha in cursor.execute("PRAGMA table_info(usuarios)").fetchall()}

        if "senha" in colunas:
            return

        if "senha_hash" in colunas:
            cursor.execute("ALTER TABLE usuarios RENAME COLUMN senha_hash TO senha")
            return

        if colunas:
            cursor.execute("ALTER TABLE usuarios ADD COLUMN senha TEXT")