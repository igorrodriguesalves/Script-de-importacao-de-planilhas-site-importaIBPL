# Importar o módulo csv
import csv

#Pergunta ao usuário qual letra precisa escolher
letra = input("Digite uma letra: ")
#Coloca a letra em maiúsculo
letra = letra.upper()

# Criar uma lista com os nomes dos 27 arquivos csv
arquivos =["TabelaIBPTaxAC23.1.F.csv", "TabelaIBPTaxAL23.1.F.csv", "TabelaIBPTaxAM23.1.F.csv", "TabelaIBPTaxAP23.1.F.csv", "TabelaIBPTaxBA23.1.F.csv", "TabelaIBPTaxCE23.1.F.csv", "TabelaIBPTaxDF23.1.F.csv", "TabelaIBPTaxES23.1.F.csv", "TabelaIBPTaxGO23.1.F.csv", "TabelaIBPTaxMA23.1.F.csv", "TabelaIBPTaxMG23.1.F.csv", "TabelaIBPTaxMS23.1.F.csv", "TabelaIBPTaxMT23.1.F.csv",
            "TabelaIBPTaxPA23.1.F.csv", "TabelaIBPTaxPB23.1.F.csv", "TabelaIBPTaxPE23.1.F.csv", "TabelaIBPTaxPI23.1.F.csv", "TabelaIBPTaxPR23.1.F.csv", "TabelaIBPTaxRJ23.1.F.csv", "TabelaIBPTaxRN23.1.F.csv", "TabelaIBPTaxRO23.1.F.csv", "TabelaIBPTaxRR23.1.F.csv", "TabelaIBPTaxRS23.1.F.csv", "TabelaIBPTaxSC23.1.F.csv", "TabelaIBPTaxSE23.1.F.csv", "TabelaIBPTaxSP23.1.F.csv", "TabelaIBPTaxTO23.1.F.csv"] 

# Criar uma lista vazia para armazenar os valores das colunas
dados = []
#Cria outra lista vazia
nova_lista = []
#Função que altera a letra do arquivo
for arquivo in arquivos: # Substituir a letra F pela letra digitada pelo usuário 
    novo_arquivo = arquivo.replace("F.csv", f"{letra}.csv")
    # Adicionar o novo arquivo à nova lista 
    nova_lista.append(novo_arquivo)

for arquivo in nova_lista:
    # Abrir o arquivo csv em modo leitura
    with open(novo_arquivo, "r", encoding='ansi') as f:
        # Criar um objeto leitor csv
        leitor = csv.DictReader(f, delimiter=';', restval=["codigo", "ex", "nacionalfederal", "importadosfederal", "estadual", "municipal"], dialect='excel')
        # Percorrer cada linha do arquivo csv
        for linha in leitor:
            # Extrair os valores das colunas desejadas
            uf = arquivo[12:14]
            str_uf = "'" + uf + "'"
            codigo = linha["codigo"]
            origem = linha["ex"]
            nacionalfederal = linha["nacionalfederal"]
            importadosfederal = linha["importadosfederal"]
            estadual = linha["estadual"]
            municipal = linha["municipal"]
            #Verifica se origem possui nulo e atribui o valor 0
            if origem is None or origem == "":
                origem += "0"
            # Verificar se algum dos valores é nulo ou vazio
            if codigo is None or codigo == "" or nacionalfederal is None or nacionalfederal == "" or importadosfederal is None or importadosfederal == "" or estadual is None or estadual == "" or municipal is None or municipal == "":
                # Ignorar a linha e continuar para a próxima
                continue
            # Formatar os valores como uma tupla
            tupla = (codigo, nacionalfederal, importadosfederal, estadual, municipal, str_uf, origem)
            # Adicionar a tupla à lista de valores
            dados.append(tupla)

# Abrir um arquivo sql em modo escrita
with open("scriptImportaIBPL.sql", "w") as f:
    # Percorrer cada tupla da lista de valores
    for tupla in dados:
        # Formatar a tupla como uma string separada por vírgulas
        valores_str = ",".join(tupla)
        # Concatenar a string com o comando SQL de inserção
        sql = f"INSERT INTO AVANTE_PRINCIPAL.CAD_IMPOSTO_IBPT (NCM,IMPOSTO_NACIONAL,IMPOSTO_IMPORTADO,IMPOSTO_ESTADUAL,IMPOSTO_MUNICIPAL, UF, ORIGEM) VALUES ({valores_str});\n"
        # Escrever o comando SQL no arquivo txt
        f.write(sql)

import os
file = open("scriptImportaIBPL.sql", "r")
lines = file.readlines()
file.close()
lines_per_file = 120000 
num_files = 3
for i in range(num_files):
    new_file = open(f"part_{i+1}.sql", "w")
    new_file.writelines(lines[i*lines_per_file:(i+1)*lines_per_file])
    new_file.close()
os.remove("scriptImportaIBPL.sql")
from tkinter import messagebox

messagebox.showinfo("Script executado com sucesso")
