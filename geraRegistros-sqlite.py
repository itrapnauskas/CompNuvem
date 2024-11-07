import random
import argparse
from datetime import datetime, timedelta
import sqlite3
from faker import Faker

# Configuração de conexão com o banco de dados SQLite
conn = sqlite3.connect('LojaVirtual.db')
cursor = conn.cursor()

# Inicializando o Faker
fake = Faker('pt_BR')

def print_progresso(iteracao, total, nome_tarefa="Registros"):
    progresso = (iteracao / total) * 100
    print(f"\r{nome_tarefa}: {iteracao}/{total} ({progresso:.2f}%) concluído", end='')


# Criação das tabelas se ainda não existirem
def criar_tabelas():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Clientes (
            ClienteID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Sobrenome TEXT,
            Email TEXT,
            Telefone TEXT,
            Endereco TEXT,
            CEP TEXT,
            DataCadastro DATE DEFAULT CURRENT_DATE,
            Genero TEXT,
            DataNascimento DATE,
            Status TEXT,
            UltimaAtualizacao DATE,
            RendaAnual REAL,
            Profissao TEXT,
            Interesses TEXT,
            EstadoCivil TEXT,
            TotalGastos REAL,
            MetodoPagamentoPreferido TEXT,
            CategoriaCliente TEXT,
            PontuacaoSatisfacao INTEGER,
            NumeroInteracoesSuporte INTEGER,
            UltimaCompra DATE,
            PreferenciasComunicacao TEXT
        )
    """)
    conn.commit()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Produtos (
            ProdutoID INTEGER PRIMARY KEY AUTOINCREMENT,
            Nome TEXT NOT NULL,
            Descricao TEXT,
            Preco REAL NOT NULL,
            Estoque INTEGER DEFAULT 0,
            Fornecedor TEXT,
            Categoria TEXT,
            CodigoBarras TEXT UNIQUE,
            DataValidade DATE,
            DataCriacao DATE DEFAULT CURRENT_DATE,
            DataAtualizacao DATE,
            Disponivel BOOLEAN DEFAULT 1
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Pedidos (
            PedidoID INTEGER PRIMARY KEY AUTOINCREMENT,
            ClienteID INTEGER,
            DataPedido DATE,
            Status TEXT,
            DataEnvio DATE,
            DataEntrega DATE,
            MetodoPagamento TEXT,
            Total REAL,
            FOREIGN KEY (ClienteID) REFERENCES Clientes (ClienteID)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ItensPedido (
            ItemID INTEGER PRIMARY KEY AUTOINCREMENT,
            PedidoID INTEGER,
            ProdutoID INTEGER,
            Quantidade INTEGER,
            PrecoUnitario REAL,
            Desconto REAL,
            TotalItem REAL,
            FOREIGN KEY (PedidoID) REFERENCES Pedidos (PedidoID),
            FOREIGN KEY (ProdutoID) REFERENCES Produtos (ProdutoID)
        )
    """)
    conn.commit()

# Função para criar clientes
def criar_clientes(qtd_clientes):
    clientes = []
    
    for i in range(qtd_clientes):
        nome = fake.first_name()
        sobrenome = fake.last_name()
        
        # Campos opcionais com possibilidade de serem vazios
        email = fake.email() if random.random() > 0.1 else None  # 10% chance de ser vazio
        telefone = fake.phone_number() if random.random() > 0.2 else None  # 20% chance de ser vazio
        endereco = fake.address().replace('\n', ', ') if random.random() > 0.1 else None  # 10% chance de ser vazio
        cep = fake.postcode() if random.random() > 0.15 else None  # 15% chance de ser vazio
        data_cadastro = fake.date_between(start_date='-5y', end_date='today')
        
        # Novos campos adicionados
        genero = random.choice(["Masculino", "Feminino", "Outro"]) if random.random() > 0.2 else None
        data_nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)
        status = random.choice(["Ativo", "Inativo", "Suspenso"]) if random.random() > 0.05 else "Ativo"
        ultima_atualizacao = fake.date_between(start_date=data_cadastro, end_date='today')
        renda_anual = round(random.uniform(15000, 150000), 2) if random.random() > 0.2 else None
        profissao = fake.job() if random.random() > 0.1 else None
        interesses = ", ".join(fake.words(nb=3, unique=True)) if random.random() > 0.2 else None
        estado_civil = random.choice(["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]) if random.random() > 0.1 else None
        total_gastos = round(random.uniform(100, 10000), 2) if random.random() > 0.3 else None
        metodo_pagamento_preferido = random.choice(["Cartão de Crédito", "Boleto", "PIX"]) if random.random() > 0.1 else None
        categoria_cliente = random.choice(["Premium", "Regular", "Ocasional"])
        pontuacao_satisfacao = random.randint(1, 5) if random.random() > 0.2 else None
        numero_interacoes_suporte = random.randint(0, 10)
        ultima_compra = fake.date_between(start_date='-1y', end_date='today') if random.random() > 0.5 else None
        preferencias_comunicacao = ", ".join(random.sample(["Email", "SMS", "Telefone"], random.randint(1, 3)))
        
        # Adiciona o cliente gerado à lista
        clientes.append((nome, sobrenome, email, telefone, endereco, cep, data_cadastro,
                         genero, data_nascimento, status, ultima_atualizacao, renda_anual, profissao, interesses,
                         estado_civil, total_gastos, metodo_pagamento_preferido, categoria_cliente, pontuacao_satisfacao,
                         numero_interacoes_suporte, ultima_compra, preferencias_comunicacao))
        
        if i % 1000 == 0:  # Exibe progresso a cada 1000 registros
            print_progresso(i + 1, qtd_clientes, "Clientes")
    
    cursor.executemany("""
        INSERT INTO Clientes (
            Nome, Sobrenome, Email, Telefone, Endereco, CEP, DataCadastro, Genero, DataNascimento, Status,
            UltimaAtualizacao, RendaAnual, Profissao, Interesses, EstadoCivil, TotalGastos, MetodoPagamentoPreferido,
            CategoriaCliente, PontuacaoSatisfacao, NumeroInteracoesSuporte, UltimaCompra, PreferenciasComunicacao
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, clientes)
    conn.commit()

# Função para criar produtos
def criar_produtos(qtd_produtos):
    produtos = []
    for i in range(qtd_produtos):
        nome = fake.word().capitalize() + " " + fake.word().capitalize()
        descricao = fake.sentence(nb_words=10)
        preco = round(random.uniform(10, 500), 2)
        estoque = random.randint(10, 100)
        
        # Dados adicionais com possibilidade de serem vazios
        fornecedor = fake.company() if random.random() > 0.2 else None  # 20% chance de ser vazio
        categoria = random.choice(['Eletrônicos', 'Alimentos', 'Vestuário', 'Móveis', 'Ferramentas']) if random.random() > 0.1 else None  # 10% chance de ser vazio
        codigo_barras = fake.unique.ean13()  # Gera um código de barras único
        data_validade = fake.date_between(start_date='today', end_date='+2y') if random.choice([True, False]) else None
        data_criacao = fake.date_between(start_date='-1y', end_date='today')
        data_atualizacao = fake.date_between(start_date=data_criacao, end_date='today')
        disponivel = random.choice([True, False])  # Definindo disponibilidade aleatória
        
        produtos.append((nome, descricao, preco, estoque, fornecedor, categoria, codigo_barras, data_validade, data_criacao, data_atualizacao, disponivel))
        
        if i % 1000 == 0:  # Exibe progresso a cada 1000 registros
            print_progresso(i + 1, qtd_produtos, "Produtos")

    cursor.executemany("""
        INSERT INTO Produtos (Nome, Descricao, Preco, Estoque, Fornecedor, Categoria, CodigoBarras, DataValidade, DataCriacao, DataAtualizacao, Disponivel)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, produtos)
    conn.commit()
    print(f"{qtd_produtos} produtos adicionados com sucesso.")

# Função para criar pedidos
def criar_pedidos(qtd_pedidos):
    cursor.execute("SELECT ClienteID FROM Clientes")
    clientes_ids = [cliente[0] for cliente in cursor.fetchall()]

    cursor.execute("SELECT ProdutoID, Preco FROM Produtos")
    produtos_info = cursor.fetchall()
    produtos_ids = [produto[0] for produto in produtos_info]
    produtos_precos = {produto[0]: produto[1] for produto in produtos_info}  # Mapeia ProdutoID para Preço

    pedidos = []
    itens_pedido = []

    for i in range(qtd_pedidos):
        cliente_id = random.choice(clientes_ids)
        data_pedido = fake.date_between(start_date='-1y', end_date='today')
        status = random.choice(['Pendente', 'Enviado', 'Entregue', 'Cancelado'])
        data_envio = fake.date_between(start_date=data_pedido, end_date='today') if status in ['Enviado', 'Entregue'] else None
        data_entrega = fake.date_between(start_date=data_envio, end_date='today') if status == 'Entregue' else None
        metodo_pagamento = random.choice(['Cartão de Crédito', 'Boleto', 'Pix'])
        
        # Inicializar total do pedido
        total_pedido = 0.0

        pedidos.append((cliente_id, data_pedido, status, data_envio, data_entrega, metodo_pagamento, total_pedido))

        if i % 1000 == 0:  # Exibe progresso a cada 1000 registros
            print_progresso(i + 1, qtd_pedidos, "Pedidos")

    cursor.executemany("""
        INSERT INTO Pedidos (ClienteID, DataPedido, Status, DataEnvio, DataEntrega, MetodoPagamento, Total)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, pedidos)
    conn.commit()

    # Re-obter os pedidos inseridos para gerar itens
    cursor.execute("SELECT PedidoID FROM Pedidos")
    pedidos_ids = [pedido[0] for pedido in cursor.fetchall()]

    for pedido_id in pedidos_ids:
        num_itens = random.randint(1, 5)  # Número aleatório de itens no pedido
        produtos = random.sample(produtos_ids, num_itens)

        for produto_id in produtos:
            quantidade = random.randint(1, 10)
            preco_unitario = produtos_precos[produto_id]
            desconto = round(random.uniform(0, 0.3), 2)  # Desconto entre 0% e 30%
            total_item = round(quantidade * preco_unitario * (1 - desconto), 2)

            # Adicionar o total do item ao total do pedido
            total_pedido += total_item
            
            itens_pedido.append((pedido_id, produto_id, quantidade, preco_unitario, desconto, total_item))

        # Atualizar o total do pedido na tabela Pedidos
        cursor.execute("UPDATE Pedidos SET Total = ? WHERE PedidoID = ?", (total_pedido, pedido_id))
    
    cursor.executemany("""
        INSERT INTO ItensPedido (PedidoID, ProdutoID, Quantidade, PrecoUnitario, Desconto, TotalItem)
        VALUES (?, ?, ?, ?, ?, ?)
    """, itens_pedido)
    conn.commit()
    print(f"{qtd_pedidos} pedidos e seus itens adicionados com sucesso.")


# Função principal para receber argumentos e executar funções
def main():
    parser = argparse.ArgumentParser(description="Gera registros aleatórios para o banco de dados.")
    parser.add_argument('--clientes', type=int, help='Quantidade de clientes a serem criados', default=1000)
    parser.add_argument('--produtos', type=int, help='Quantidade de produtos a serem criados', default=1000)
    parser.add_argument('--pedidos', type=int, help='Quantidade de pedidos a serem criados', default=1000)
    args = parser.parse_args()
    
    # Cria as tabelas se ainda não existirem
    criar_tabelas()

    # Executa as funções com base nos argumentos
    if args.clientes > 0:
        criar_clientes(args.clientes)
    if args.produtos > 0:
        criar_produtos(args.produtos)
    if args.pedidos > 0:
        criar_pedidos(args.pedidos)
    
    print("Todos os dados foram gerados com sucesso!")

# Executa o script
if __name__ == '__main__':
    main()
    cursor.close()
    conn.close()