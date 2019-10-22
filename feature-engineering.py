#=========================================
# PROJETO MINERACAO DE DADOS
# feature engineering
# tabela ambulatorio e internacao
#
# @claudioalvesmonteiro
#=========================================

# importar pacotes
import pandas as pd
from analise_exploratoria import contaePorcent

# importar dados
arq = pd.ExcelFile('data/filtered_data.xlsx')
paciente = arq.parse(0)
internacao = arq.parse(1)
amb = arq.parse(2)

#==========================
# TRATAMENTO
#==========================

# passar codigo para string
amb['Cod Integração'] = [str(x) for x in amb['Cod Integração']]
paciente['Cod Integração'] = [str(x) for x in paciente['Cod Integração']]
internacao['Cod Integração'] = [str(x) for x in internacao['Cod Integração']]

#===========================
# FEATURE ENGINEERING
#===========================

# ****** filtrar casos repetidos de procedimentos [**** ESPERAR POR RENAN ****]

#------------ quantidade de procedimentos por paciente

# agrupar n de procedimentos por paciente
qpro = contaePorcent(amb, 'Cod Integração')
qpro.columns = ['Cod Integração', 'numero_procedimentos', 'porcent']

# combinar com base de paciente
paciente = paciente.merge(qpro[['Cod Integração', 'numero_procedimentos']], on='Cod Integração')

#------------ diagnostico do ambulatorio

# capturar distribuicao da CID
cont_CID = contaePorcent(amb, 'CID')

# combinar com base de ambulatorio
amb = amb.merge(cont_CID, on='CID')

# criar coluna CID > 1%
amb['CID_sig'] = [amb['CID'][x] if amb['porcent'][x] >= 1 else 'OUTROS' for x in range(len(amb))]

# selecionar casos unicos do cod integracao e cid
uni_cid = amb[['Cod Integração', 'CID_sig']].drop_duplicates()

# combinar com base de pacientes
paciente = paciente.merge(uni_cid, on='Cod Integração')

# criar variaveis dummy para CID > %1 e combinar com a base
cidummy = pd.get_dummies(paciente['CID_sig'], prefix='CID')

paciente = pd.concat([paciente, cidummy], axis=1)

#------------ alvo [1 se internado na UTI, 0 caso contrario] [tabela internacao]

# internacao[['Unidade Nome', 'UTI=1']].groupby(['Unidade Nome', 'UTI=1']).size()

# filtrar casos UTI = 1 e remover duplicados
uti = internacao[internacao['UTI=1'] == 1]
uti = uti.drop_duplicates('Cod Integração')

# criar variavel de alvo e selecionar colunas
uti['ALVO'] = 1
uti = uti[['Cod Integração', 'ALVO']]

# criar base final
dataset = paciente.merge(uti, on='Cod Integração', how='left')

# atribuir 0 a nulos no ALVO
dataset['ALVO'] = [0 if pd.isnull(x) else x for x in dataset['ALVO'] ]

#------------ salvar base

dataset.to_csv('data/preprocessed_data.csv', index=False)



