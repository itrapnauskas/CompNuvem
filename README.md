# Desafio de Banco de Dados na AWS

## Objetivo
Neste desafio, você aprenderá como criar e interagir com um banco de dados usando a AWS. O objetivo é conectar-se a um banco de dados na nuvem (Amazon RDS) e realizar operações básicas de CRUD (Create, Read, Update, Delete). Você poderá Python para interagir com o banco de dados e aprenderá a configurar e administrar bancos de dados relacionais na AWS.

## Passos para o Desafio

### 1. **Introdução**
Antes de começar, assista à aula onde explicamos os conceitos de banco de dados, os serviços da AWS e como trabalhar com Amazon RDS. O serviço RDS permite criar bancos de dados relacionais gerenciados, como MySQL, PostgreSQL, MariaDB, etc.

### 2. **Criação do Banco de Dados no Amazon RDS**
1. **Acesse o console da AWS:**
   - Vá para o [Console da AWS](https://aws.amazon.com/console/).
   - Faça login com sua conta ou crie uma conta nova, se necessário.

2. **Criar uma instância de banco de dados RDS:**
   - No painel da AWS, busque por **RDS** na barra de pesquisa e selecione **Amazon RDS**.
   - Clique em "Create database".
   - Selecione o mecanismo de banco de dados que você deseja usar (exemplo: MySQL ou PostgreSQL).
   - Configure os detalhes da instância:
     - Escolha a versão do banco de dados (exemplo: MySQL 8.0).
     - Defina a **identificação da instância**, **usuário administrador** e **senha**.
     - Selecione o tipo de instância que se encaixa no **AWS Free Tier** para que você não tenha custos adicionais.

3. **Conectar-se à instância do RDS:**
   - Após criar a instância, acesse as informações de **Endpoint** no painel da instância para usar no código.
   - Defina o grupo de segurança para permitir conexões do seu IP ou de qualquer IP (caso esteja usando um ambiente mais flexível).
   
---

### 3. **Criação do Banco de Dados e Tabelas**
Após criar a instância do RDS, você precisará conectar-se ao banco de dados e criar as tabelas para armazenar os dados de **clientes** e **produtos**. Use o seguinte código SQL para isso:

#### **Código SQL para MySQL:**
```sql
-- Criação do Banco de Dados
CREATE DATABASE LojaVirtual;

-- Tabela de Clientes
CREATE TABLE Clientes (
    ClienteID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100),
    Sobrenome VARCHAR(100),
    Email VARCHAR(100),
    Telefone VARCHAR(20),
    Endereco TEXT
);

-- Tabela de Produtos
CREATE TABLE Produtos (
    ProdutoID INT AUTO_INCREMENT PRIMARY KEY,
    Nome VARCHAR(100),
    Descricao TEXT,
    Preco DECIMAL(10, 2),
    Estoque INT
);
```

- **Clientes**: Nome, Sobrenome, Email, Telefone, Endereço.
- **Produtos**: Nome, Descrição, Preço, Estoque.

---

### 4. **Desenvolvendo o Código Python para Interagir com o Banco de Dados**
Agora, você vai escrever um código Python para interagir com o banco de dados e realizar as operações CRUD. Use a biblioteca `pymysql` para MySQL ou `psycopg2` para PostgreSQL.

#### **Código Python para Conexão e CRUD (MySQL):**
```python
import pymysql

# Conectar ao banco de dados RDS
connection = pymysql.connect(
    host='your-db-endpoint',  # Substitua pelo Endpoint do RDS
    user='your-username',     # Substitua pelo seu usuário
    password='your-password', # Substitua pela sua senha
    database='LojaVirtual'
)

# Criar um cursor
cursor = connection.cursor()

# Operações CRUD (exemplo para CREATE e READ)

# Create - Inserir um novo cliente
cursor.execute("INSERT INTO Clientes (Nome, Sobrenome, Email, Telefone, Endereco) VALUES ('João', 'Silva', 'joao@email.com', '123456789', 'Rua A')")
connection.commit()

# Read - Consultar clientes
cursor.execute("SELECT * FROM Clientes")
resultados = cursor.fetchall()
for row in resultados:
    print(row)

# Fechar a conexão
cursor.close()
connection.close()
```

#### **Requisitos do Código:**
- Instale o `pymysql` no seu ambiente:
  ```bash
  pip install pymysql
  ```

---

### 5. **Operações CRUD**
Aqui estão os detalhes das operações que você deve implementar:
- **Create**: Adicionar um novo cliente ou produto.
- **Read**: Consultar todos os clientes ou produtos inseridos.
- **Update**: Atualizar o telefone de um cliente ou o preço de um produto.
- **Delete**: Deletar um cliente ou produto específico.

Exemplo de **Update** em SQL:
```sql
UPDATE Clientes SET Telefone = '987654321' WHERE ClienteID = 1;
```

Exemplo de **Delete** em SQL:
```sql
DELETE FROM Clientes WHERE ClienteID = 1;
```

---

### 6. **Interação Entre Tabelas**
Você pode criar uma relação entre clientes e produtos utilizando uma tabela de **pedidos**. Isso pode ser feito com um **JOIN** SQL entre as tabelas, permitindo que você associe um cliente a um ou mais produtos comprados.

Exemplo de criação de uma tabela de pedidos:
```sql
CREATE TABLE Pedidos (
    PedidoID INT AUTO_INCREMENT PRIMARY KEY,
    ClienteID INT,
    DataPedido DATE,
    FOREIGN KEY (ClienteID) REFERENCES Clientes(ClienteID)
);
```

E consulta para relacionar clientes e pedidos:
```sql
SELECT Clientes.Nome, Pedidos.DataPedido
FROM Clientes
JOIN Pedidos ON Clientes.ClienteID = Pedidos.ClienteID;
```
---

## Recursos Adicionais
- **AWS RDS Documentation**: [Link](https://docs.aws.amazon.com/pt_br/AmazonRDS/latest/UserGuide/Welcome.html)
- **Python MySQL Documentation**: [Link](https://pymysql.readthedocs.io/)
- **AWS Free Tier**: [Link](https://aws.amazon.com/free/)
- **Faker Documentation**: [Link](https://faker.readthedocs.io/en/master/)

