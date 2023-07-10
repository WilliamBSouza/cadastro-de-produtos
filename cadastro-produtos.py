import sqlite3
import os

def limpa_terminal():
    if os.name == 'nt':
        os.system('cls')

    else:
        os.system('clear')

conexao = sqlite3.connect('produtos.db')
cursor = conexao.cursor()

# Cria a tabela
#cursor.execute('CREATE TABLE produtos (ID INT PEIMARY KEY, DESCRIÇÃO VARCHAR(45), QTD_ESTOQUE FLOAT, VALOR_VENDA FLOAT, VALOR_COMPRA FLOAT, PORCENTAGEM_BRUTA FLOAT)')

def add_produtos():

    #limpa o terminal
    limpa_terminal()
    print("-" * 50)
    codigo_produto = input("Digite o código do produto: ")
    descrição = input("Digite a descrição do produto: ")
    qtd_estoque = input("Digite a quantidade em estoque: ")
    valor_venda = float(input("Digite o valor de venda em R$: "))
    valor_compra = float(input("Digite o valor de compra em, R$: "))
    porcentagem_bruta =  round(((valor_venda / valor_compra) - 1) * 100, 2)

    cursor.execute('INSERT INTO produtos VALUES(?,?,?,?,?,?)', (codigo_produto, descrição, qtd_estoque, valor_venda, valor_compra, porcentagem_bruta))

    # Confirma as alterações
    conexao.commit()

    print("Cliente adicionado com sucesso!")
    print("-" * 50)

def delete_produto(id):
    # Limpa o terminal
    limpa_terminal()

    print("-" * 50)

    conexao = sqlite3.connect('produtos.db')
    cursor = conexao.cursor()

    # Verifica se o ID existe na tabela
    cursor.execute('SELECT ID FROM produtos WHERE id = ?', (id,))
    result = cursor.fetchone()

    if result is None:
        # ID não encontrado
        print("O produto com o código fornecido não existe.")
    else:
        # Executa a instrução DELETE
        cursor.execute('DELETE FROM produtos WHERE id = ?', (id,))

        # Confirma as alterações
        conexao.commit()

        print("Produto deletado com sucesso.")

    # Fecha a conexão
    conexao.close()

def exibir_produtos():
    
    #limpa o terminal
    limpa_terminal()
    print("ID, Descrição, Estoque, Valor Venda, Valor Compra, Porcebtagem Bruta.")
    print("*" * 50)
    # Executa a consulta SELECT em ordem crescente por id ORDER BY
    cursor.execute('SELECT * FROM produtos ORDER BY id ASC')

    # Recupera todos os registros
    registros = cursor.fetchall()

    # Exibe os registros
    for registro in registros:
        print(registro)
    
    print("*" * 50)

def editar_produto(id_produto):
    print("-" * 50)

    # Solicita o campo a ser editado
    campo = input("""Digite a informação a ser editada:
                   [1] ID
                   [2] Descrição
                   [3] Qtd_estoque
                   [4] Valor Venda 
                   [5] Valor Compra 
                   [6] Porcentagem Bruta (conta manual)
                   Opção: """)

    if campo == "1":
        campo = "ID"
    elif campo == "2":
        campo = "DESCRIÇÃO"
    elif campo == "3":
        campo = "QTD_ESTOQUE"
    elif campo == "4":
        print("EDITAR MANUALMENTE O CAMPO PORCENTAGEM BRUTA!")
        campo = "VALOR_VENDA"
    elif campo == "5":
        print("EDITAR MANUALMENTE O CAMPO PORCENTAGEM BRUTA!")
        campo = "VALOR_COMPRA"
    elif campo == "6":
        print("EDITAR MANUALMENTE O CAMPO VALOR DE VENDA OU VALOR DE COMPRA!")
        campo = "PORCENTAGEM_BRUTA"
    else:
        print("Opção inválida. Saindo...")
        return

    print("Você está editando o campo:", campo)
    novo_valor = input("Digite o novo valor: ")

    conexao = sqlite3.connect('produtos.db')
    cursor = conexao.cursor()

    # Executa a instrução UPDATE
    cursor.execute(f'UPDATE produtos SET {campo} = ? WHERE ID = ?', (novo_valor, id_produto))

    # Confirma as alterações
    conexao.commit()

    # Fecha a conexão
    conexao.close()
    print("Produto atualizado com sucesso!")

    print("-" * 50)



while True:
    
    selecao = input("""
                    [1] Adicionar Produto
                    [2] Editar Produto
                    [3] Deletar Produto
                    [4] Exibir Produtos
                    [5] Sair
                    Digite a opção:  """)
    
    print("-" * 50)

    if selecao == "1":
        add_produtos()

    if selecao == '2':
        id_para_alterar = input("Digite o código do produto a ser alterado: ")
        print("*" * 50)
        cursor.execute(f'SELECT * FROM produtos WHERE id = {id_para_alterar}')
        produto_alterando = cursor.fetchone()  # Recupera o primeiro registro para mostrar os dados no print. 

        if produto_alterando:
            print("Você está alterando estes dados:")
            print(produto_alterando)
            print("*" * 50)
            editar_produto(id_para_alterar)

        else:
            print("produto não encontrado.")
            print("*" * 50)
    
    if selecao == "3":
        id_produto_a_deletar = input("Digite o código do produto a ser deletado: ")
        delete_produto(id_produto_a_deletar)
    
    if selecao == "4":
        print(" ID ,  Descrição  ,  Estoque  ,  Valor Venda  , Valor Compra  , Porcebtagem Bruta.")
        exibir_produtos()
    
    elif selecao == "5":
        break
# Fecha a conexão
conexao.close()