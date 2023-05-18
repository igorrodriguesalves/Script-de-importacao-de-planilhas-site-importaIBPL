# Importar o módulo csv
import csv

# Criar uma lista com os nomes dos 27 arquivos csv
arquivos = ["TabelaIBPTaxAC23.1.E.csv", "TabelaIBPTaxAL23.1.E.csv", "TabelaIBPTaxAM23.1.E.csv", "TabelaIBPTaxAP23.1.E.csv", "TabelaIBPTaxBA23.1.E.csv", "TabelaIBPTaxCE23.1.E.csv", "TabelaIBPTaxDF23.1.E.csv", "TabelaIBPTaxES23.1.E.csv", "TabelaIBPTaxGO23.1.E.csv", "TabelaIBPTaxMA23.1.E.csv", "TabelaIBPTaxMG23.1.E.csv", "TabelaIBPTaxMS23.1.E.csv", "TabelaIBPTaxMT23.1.E.csv",
            "TabelaIBPTaxPA23.1.E.csv", "TabelaIBPTaxPB23.1.E.csv", "TabelaIBPTaxPE23.1.E.csv", "TabelaIBPTaxPI23.1.E.csv", "TabelaIBPTaxPR23.1.E.csv", "TabelaIBPTaxRJ23.1.E.csv", "TabelaIBPTaxRN23.1.E.csv", "TabelaIBPTaxRO23.1.E.csv", "TabelaIBPTaxRR23.1.E.csv", "TabelaIBPTaxRS23.1.E.csv", "TabelaIBPTaxSC23.1.E.csv", "TabelaIBPTaxSE23.1.E.csv", "TabelaIBPTaxSP23.1.E.csv", "TabelaIBPTaxTO23.1.E.csv"]

# Criar uma lista vazia para armazenar os valores das colunas
dados = []

# Percorrer cada arquivo da lista de arquivos
for arquivo in arquivos:
    # Abrir o arquivo csv em modo leitura
    with open(arquivo, "r", encoding='ansi') as f:
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
with open("scriptImportaIBPT.sql", "w") as f:
    # Percorrer cada tupla da lista de valores
    for tupla in dados:
        # Formatar a tupla como uma string separada por vírgulas
        valores_str = ",".join(tupla)
        # Concatenar a string com o comando SQL de inserção
        sql = f"INSERT INTO tabela (NCM,IMPOSTO_NACIONAL,IMPOSTO_IMPORTADO,IMPOSTO_ESTADUAL,IMPOSTO_MUNICIPAL, UF, ORIGEM) VALUES ({valores_str});\n"
        # Escrever o comando SQL no arquivo txt
        f.write(sql)

import os
#Abre o arquivo
file = open("scriptImportaIBPT.sql", "r")
#Verifica a quantidade de linhas e fecha o arquivo
lines = file.readlines()
file.close()
#Cria um limite de linhas para dividir o arquivo
lines_per_file = 120000 
num_files = 3
for i in range(num_files):
    new_file = open(f"part_{i+1}.sql", "w")
    new_file.writelines(lines[i*lines_per_file:(i+1)*lines_per_file])
    new_file.close()
#Apaga o arquivo
os.remove("scriptImportaIBPT.sql")
import logging 
logging.basicConfig(level=logging.WARNING) 
logging.warning("Script executado com sucesso")
