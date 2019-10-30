#===============================================
# PROJETO MINERACAO DE DADOS
# analise exploratoria e visualizacao de dados
#
# @claudioalvesmonteiro
#===============================================

# importar pacotes
import pandas as pd
from utils_functions import*

# importar dados
data = pd.read_csv('data/preprocessed_data.csv')
arq = pd.ExcelFile('data/raw_data.xlsx')
amb = arq.parse(2)

#==================================
# gerar tabelas para visualizacao
#==================================

pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 1000)

contaePorcent(amb, 'CID', save=True)
contaePorcent(data, 'Sexo',  save=True)
contaePorcent(data, 'Estado',  save=True)
contaePorcent(data, 'Bairro',  save=True)
contaePorcent(data, 'Cidade',  save=True)
contaePorcent(data, 'Idade',  save=True)

contaePorcent(amb, 'PROCEDIMENTO',  save=True)

contaAlvoPorcent(data, 'Sexo',  save=True)